---
title: "Aggregation von Prüfergebnissen mit drei Zuständen"
description: "PASS / FAIL / UNKNOWN statt Bestanden/Nicht bestanden: Exit-Code-Verträge, fail-closed-Aggregation, Alarme bei ausbleibendem Signal und warum das Durchsuchen von Fließtext nach einem Urteil irgendwann ein rotes System als grün meldet."
level: 3
source_sha256: 0460b5c7e53060dc5e655f5465299af96d34ee3294c311649ace92a97a23500c
translation: machine
translated_at: '2026-10-24'
---
# Aggregation von Prüfergebnissen mit drei Zuständen {#three-state-check-aggregation}

Ein Prüfmechanismus muss drei Ergebnisse unterscheiden, nicht zwei. Das Zusammenfassen des dritten Zustands mit dem ersten ist der eigentliche Fehler: **ein ausbleibendes Signal wird von Gesundheit nicht mehr unterscheidbar**. Der Fehler fällt immer auf die gefährliche Seite, weil eine nicht ausgeführte Prüfung genauso aussieht wie ein ausbleibender Fehler.

| Zustand | Bedeutung | Aktion des Verbrauchers |
|---|---|---|
| `PASS` | Ausgeführt, entspricht der Erwartung | Fortfahren |
| `FAIL` | Ausgeführt, entspricht nicht der Erwartung | System korrigieren |
| `UNKNOWN` | **Nicht ausgeführt oder keine Entscheidung möglich** | Nicht grün. Ursache klären, warum die Prüfung nicht lief |

## Exit-Code-Vertrag {#exit-code-contract}

Der maschinelle Kanal ist der Exit-Status. Gedruckter Text ist für Menschen gedacht und driftet in dem Moment ab, in dem jemand eine Meldung umformuliert.

```python
# Convention, declared in a manifest - never guessed by the consumer.
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_UNKNOWN = 2   # could not run: missing dependency, no credentials, target unreachable
```

```python
import sys

def main() -> int:
    if not tool_available():
        print("check NOT performed (this is not a success): tool missing")
        return EXIT_UNKNOWN
    return EXIT_PASS if probe_matches() else EXIT_FAIL

if __name__ == "__main__":
    sys.exit(main())   # never `main()` alone - a falling-off-the-end return of None exits 0
```

Der Code `UNKNOWN` muss **deklariert** werden, nicht erraten. Ein Verbraucher, der schließt, „2 bedeutet vermutlich übersprungen“, betreibt Textsuche mit zusätzlichen Schritten. Trage ihn im Manifest ein, das der Aggregator liest:

```json
{
  "checks": [
    {"id": "schema", "cmd": ["python", "checks/schema.py"], "timeout_sec": 120},
    {"id": "smoke",  "cmd": ["python", "checks/smoke.py"],  "timeout_sec": 300}
  ],
  "unknown_exit_codes": [2]
}
```

## Fail-closed-Aggregation {#fail-closed-aggregation}

Grün wird nur ausgegeben, wenn **jede** erwartete Prüfung ausgeführt wurde und bestanden hat. Ein einziges `UNKNOWN` reicht, um Grün zurückzuhalten. Ein Ergebnis, das nie eingetroffen ist, ist `UNKNOWN`, nicht „nichts zu melden“.

```python
import json, subprocess

def run_check(spec, unknown_codes):
    try:
        proc = subprocess.run(spec["cmd"], capture_output=True, text=True,
                              timeout=spec.get("timeout_sec", 300), encoding="utf-8")
    except FileNotFoundError:
        return "UNKNOWN", "executable not found"
    except subprocess.TimeoutExpired:
        return "UNKNOWN", "timeout"
    rc = proc.returncode
    if rc in unknown_codes:
        return "UNKNOWN", f"declared unknown exit {rc}"
    if rc < 0:
        return "UNKNOWN", f"killed by signal {-rc}"     # not a failed assertion
    return ("PASS", "") if rc == 0 else ("FAIL", f"exit {rc}")

def aggregate(manifest_path):
    m = json.loads(open(manifest_path, encoding="utf-8").read())
    unknown_codes = set(m.get("unknown_exit_codes", [2]))
    results = {}
    for spec in m["checks"]:
        results[spec["id"]] = run_check(spec, unknown_codes)

    # every declared check must have produced a result
    for spec in m["checks"]:
        results.setdefault(spec["id"], ("UNKNOWN", "no result recorded"))

    if any(v[0] == "FAIL" for v in results.values()):
        return 1, results
    if any(v[0] == "UNKNOWN" for v in results.values()):
        return 2, results          # fail closed: not green
    return 0, results
```

Drei Eigenschaften leisten die Arbeit: Das Urteil stammt aus dem Rückgabecode, ein Absturz oder Timeout landet in `UNKNOWN` statt verloren zu gehen, und ein fehlendes Ergebnis wird als `UNKNOWN` materialisiert, statt im Bericht übersprungen zu werden.

## Ausbleibendes Signal ist ein Alarm {#absence-of-signal-is-an-alarm}

Ein Monitor, der aufhört zu melden, sieht von außen genauso aus wie ein ruhiges System.

- **Immer feuernder Watchdog.** Eine Regel, die unbedingt feuert (`vector(1)` in Prometheus), belegt, dass die gesamte Pipeline (Regel-Engine, Alertmanager, Empfänger) lebt. Wird sie still, ist die Stille *selbst* der Alarm.
- **Fehlende Zeitreihe.** `absent()` / `absent_over_time(metric[15m])` macht „keine Daten“ zu einer auslösenden Bedingung. Ohne sie ist ein abgestürzter Exporter ein flaches, ruhiges Dashboard.
- **Stille des Reporters.** Ein Supervisor, der sich innerhalb von `SILENCE_MINUTES` nicht gemeldet hat, löst seinen eigenen Alarm aus. Ein toter Watchdog darf nicht gesund aussehen können.

```yaml
# Prometheus: the two rules that make silence visible
groups:
  - name: meta
    rules:
      - alert: Watchdog                 # must always fire; its absence is the signal
        expr: vector(1)
        labels: {severity: none}
      - alert: ExporterGone
        expr: absent_over_time(up{job="worker"}[15m])
        for: 5m
        labels: {severity: page}
```

## Unterdrückte Wiederholung ist keine Gesundheit {#suppressed-repeat-is-not-health}

Deduplizierung und Wiederholungsunterdrückung sind korrektes Verhalten und zugleich eine häufige Ursache für lügende Logs: Ein bereits zugestellter Alarm wird nicht erneut gesendet, und der Reporter gibt „alles grün“ aus, weil er in diesem Zyklus keinen *neuen* Alarm gesehen hat.

Protokolliere die beiden Situationen unterschiedlich:

```text
all green: 0 findings
suppressed: 16 findings still open, alarms already delivered (no new alerts this cycle)
```

Ein Supervisor, der 72 aufeinanderfolgende Zyklen lang „alles grün“ ausgab, während 16 Befunde offen standen, log nicht über die Befunde. Er log über die *Form seines eigenen Schweigens*.

## Strukturierte Ergebnisse statt Fließtext {#structured-results-not-prose}

CI-Berichtsformate (JUnit XML, TAP, CTRF) existieren, weil Fließtext kein Vertrag ist. Ein Zusammenfassungsschritt liest das strukturierte Ergebnis oder den Rückgabecode; er sucht nie nach einem Wort.

```bash
# WRONG - the verdict depends on which word this month's author chose
python run_checks.py | grep -c "FAIL" && echo "red" || echo "green"

# RIGHT - the pipeline preserves the failing status, the verdict is the code
set -o pipefail
python run_checks.py --junit-xml results.xml | tee run.log
rc=$?
case "$rc" in
  0) echo "PASS" ;;
  2) echo "UNKNOWN - not green" ; exit 2 ;;
  *) echo "FAIL" ; exit 1 ;;
esac
```

Ohne `set -o pipefail` meldet die Pipeline den Exit-Code von `tee`, sodass jeder Fehler hinter einer Pipe als Erfolg erscheint.

## Fallstricke {#gotchas}

- **Problem:** Der Aggregator durchsucht stdout nach `FAIL`, und eine später geschriebene Prüfung gibt „MISMATCH“ oder ein lokalisiertes Wort aus. Die Suite wird grün, obwohl echte Defekte darin stecken. ->
  **Lösung:** Nach Exit-Code oder strukturiertem Bericht urteilen; gedruckten Text nur als menschenlesbar behandeln. Das Vereinheitlichen der Formulierung behebt eine Runde und bricht bei der nächsten Autorin.
- **Problem:** `sys.exit(main())`, wobei `main()` ohne `return` enden und `None` zurückgeben kann. `None` beendet mit 0, also meldet jeder Fehlerpfad Erfolg. ->
  **Lösung:** Jeder Zweig gibt einen expliziten Code zurück; der Rückgabetyp wird in einem Test geprüft.
- **Problem:** Eine Prüfung, die nicht laufen konnte (fehlendes Binary, keine Zugangsdaten, nicht erreichbares Ziel), wird stillschweigend aus dem Bericht weggelassen, sodass die Zusammenfassung nur Bestandene zeigt. ->
  **Lösung:** Jede deklarierte Prüfung wird materialisiert; ein fehlendes Ergebnis ist `UNKNOWN` und blockiert Grün.
- **Problem:** Eine Probe antwortet über das falsche Ziel. Die Queue wird an einem Port gelesen, während der neu zu startende Container auf einem anderen lauscht, und die falsche Antwort hat dieselbe Form wie die richtige. ->
  **Lösung:** Die Probe gibt die Identität dessen zurück, was sie gemessen hat (Endpunkt, Container-ID, Revision), und der Verbraucher prüft genau diese Identität.
- **Problem:** Timeouts und Signale werden in `FAIL` gefaltet. Ein instabiles Infrastrukturproblem ist dadurch nicht von einem echten Assertion-Fehler zu unterscheiden und wird durch Wiederholen „repariert“. ->
  **Lösung:** Timeout, Signal-Kill und Startfehler sind `UNKNOWN`; nur ein vollständig abgeschlossener Lauf, der der Erwartung widersprach, ist `FAIL`.
- **Problem:** Ein Alarm wiederholt sich endlos bei einem bekannten blockierten Zustand, sodass der Kanal von seinen Lesern stummgeschaltet wird. Ein Kanal, an den man sich gewöhnt hat, ihn zu ignorieren, ist schlechter als gar kein Kanal. ->
  **Lösung:** Die Wiederholung unterdrücken, aber den laufenden Zählerstand im periodischen Bericht sichtbar halten.

## Siehe auch {#see-also}

- [[negative-controls-for-verification]] - Nachweis, dass eine Prüfung überhaupt auf rot springen kann
- [[ci-cd-test-automation]] - wo der Exit-Code-Vertrag verbraucht wird
- [[monitoring-and-observability]] - Watchdog- und Absence-Alarmierung in der Praxis
- [[observability-query-languages]] - `absent_over_time` und Verwandte
- [[sre-incident-management]] - Alarmmüdigkeit und Unterdrückungsrichtlinie
- [[test-architecture]] - Berichtsebenen und Ergebnisformate
- [[winhttp-async-client]] - Timeout als dritter Zustand im Client-Code
