---
title: "Negativkontrollen für Verifikation"
description: "Ein grüner Check beweist nichts, solange nicht gezeigt wurde, dass er auch rot werden kann. Hide-the-subject-Protokoll, Must-fail-Fixtures, Mutationstests als Restrisiko-Messung und das Anti-Pattern des selbstzertifizierenden Beweises."
level: 3
source_sha256: f2f1eed6fdc0c882cf3e76f32aa8553503b9d9e755872d3d067ed6f80c01e9fb
translation: machine
translated_at: '2026-10-24'
---
# Negativkontrollen für Verifikation {#negative-controls-for-verification}

Jedes Prüfinstrument braucht einen Fall, der **zwingend** rot ausgeben muss. Ohne einen solchen
Fall trägt ein grünes Ergebnis keine Information: Es ist gleichermaßen mit „das System ist
korrekt“ und mit „das Instrument kann nichts erkennen“ vereinbar. Ein Test ohne Assertion kann
nicht fehlschlagen; ein Gate, das die falsche Datei liest, kann nicht fehlschlagen; ein Beweis,
der seinen Gegenstand nie berührt, kann nicht fehlschlagen.

## Die Messung: Gegenstand verbergen, Rot erzwingen {#the-measurement-hide-the-subject-demand-red}

Das Protokoll ist eine Zeile lang und klärt die Frage mechanisch.

1. Benennen Sie, worum es in der Prüfung geht (den *Gegenstand*), und fixieren Sie ihn per Digest.
2. Entfernen, verfälschen oder ersetzen Sie den Gegenstand.
3. Führen Sie die Prüfung aus. Sie **muss** einen Wert ungleich null zurückgeben.
4. Bleibt sie grün, ist das Instrument kaputt – nicht das System.

```python
import hashlib, json, shutil, subprocess, tempfile
from pathlib import Path

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def gate(manifest_path: Path) -> int:
    """Refuse to accept a proof that cannot go red when its subject disappears."""
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    subject, check = Path(m["subject"]), m["check"]

    if digest(subject) != m["subject_sha256"]:
        print("subject changed since the manifest was written")
        return 1

    green = subprocess.run(check, capture_output=True).returncode
    if green != 0:
        print("check fails on the intact subject")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        stash = Path(tmp) / subject.name
        shutil.move(subject, stash)                 # hide the subject
        try:
            red = subprocess.run(check, capture_output=True).returncode
        finally:
            shutil.move(stash, subject)             # always restore

    if red == 0:
        print("NEGATIVE CONTROL FAILED: check is green without its subject")
        return 1
    return 0
```

**Gemessene Basislinie aus einem Audit von 18 Beweisskripten:** 16 blieben grün in einer Welt, die
nur das Skript selbst enthielt – 6 prüften nichts, 10 verifizierten Artefakte, die sie gerade
selbst geschrieben hatten, 1 griff über den eigenen Geltungsbereich hinaus, 1 war nicht
reproduzierbar. Ihre Exit-Codes änderten sich nicht, als das Objekt gelöscht wurde, das sie
angeblich bewiesen.

## Must-fail-Fixtures im Selbsttest {#must-fail-fixtures-in-the-self-test}

Ein Instrument wird mit einer eigenen Testsuite ausgeliefert, und diese Suite braucht Fälle, die
konstruktionsbedingt rot sind. Am wertvollsten ist die Fixture, die **Erfolg ausgibt und trotzdem
einen Exit-Code ungleich null liefert**, weil sie unterscheidet, ob das Instrument den Text oder
den Status liest.

```python
FIXTURES = [
    ("intact",        0),   # subject present, check correct
    ("no_manifest",   1),   # nothing declares what is being proved
    ("empty_check",   1),   # check asserts nothing
    ("prints_pass",   1),   # prints "PASS", exits 1 - status wins over prose
    ("wrong_digest",  1),   # subject differs from the pinned digest
    ("unknown_flag",  2),   # cannot run -> UNKNOWN, never green
]

def self_test() -> int:
    bad = [name for name, want in FIXTURES if run_fixture(name) != want]
    if bad:
        print("self-test failed on:", ", ".join(bad))
        return 1
    return 0
```

Führen Sie den Selbsttest in der CI bei jeder Änderung am Instrument aus. Ein Instrument ohne
Selbsttest ist eine ungeprüfte Behauptung über Verifikation.

## Mutationstests: die allgemeine Form {#mutation-testing-the-general-form}

Negativkontrollen lassen sich zu Mutationstests erweitern. Injizieren Sie eine kleine semantische
Änderung in den zu prüfenden Code und führen Sie die Suite erneut aus:

- **Getöteter Mutant** – mindestens ein Test ist fehlgeschlagen. Die Suite erkennt diese Fehlerklasse.
- **Überlebender Mutant** – alle Tests liefen mit falschem Code durch. Das ist **Restrisiko**,
  gemessen statt angenommen.

```bash
# Python: mutmut / cosmic-ray. JS/TS: Stryker. Java: PIT.
mutmut run --paths-to-mutate src/pricing.py
mutmut results          # survivors are the report; coverage percentage is not
```

Zeilenabdeckung kann dies nicht ersetzen. Code, der von einem Test ohne Assertion ausgeführt wird,
ist zu 100 % abgedeckt und zu 0 % verifiziert – genau diese Form lässt alle Mutanten überleben.

Wenden Sie dieselbe Idee auf jedes Gate an, nicht nur auf Unit-Tests: Ändern Sie die eigene Logik
der Prüfung so, dass sie brechen sollte (falsches Feld lesen, gegen eine Konstante vergleichen,
Vergleichsoperator vertauschen), und bestätigen Sie, dass sich das Urteil ändert. Mutationen, die
das Verhalten nachweislich nicht verändern können, sind *äquivalente Mutanten*; erfassen Sie sie
als solche, statt sie als Erkennungsfehler zu zählen.

## Der selbstzertifizierende Beweis {#the-self-certifying-proof}

Das wiederkehrende Anti-Pattern: ein Skript, das ein Artefakt schreibt und dann genau das gerade
geschriebene Artefakt verifiziert.

```python
# WRONG - proves the script can write a file, nothing about the system
out = run_pipeline()
Path("evidence.json").write_text(json.dumps(out))
assert json.loads(Path("evidence.json").read_text())["status"] == "ok"
```

Es ist auf einem Rechner grün, auf dem der Gegenstand gar nicht existiert. Die Lösung besteht
darin, den Beweis von etwas abhängig zu machen, das er nicht selbst erzeugt hat: einem fixierten
Eingabe-Digest, einer Antwort des echten Dienstes, einem Artefakt aus einem anderen Schritt oder
einer Datei, deren Fehlen er nicht überdecken kann.

```python
# RIGHT - the proof is bound to an external subject it cannot fabricate
manifest = json.loads(Path("proof.manifest.json").read_text(encoding="utf-8"))
subject = Path(manifest["subject"])                      # produced elsewhere
assert digest(subject) == manifest["subject_sha256"]     # cannot pass if it is missing
assert probe_real_endpoint(manifest["endpoint"]).status_code == 200
```

## Wo grüne Suiten blind werden {#where-green-suites-go-blind}

Eine bestandene Suite ist Evidenz über die Fälle, die jemand bedacht hat. Sie sagt nichts über
Fälle aus, die niemand aufgezählt hat.

- Ein Guard, der gegen eine Liste von Schreibweisen geschrieben wurde, deckt genau diese Liste ab.
  Ein gemessener Fall: Ein Fix schloss einen Umgehungspfad, die eigene Probe bestätigte das, 32
  Tests liefen durch – und ein unabhängiger Reviewer fand 18 weitere Varianten derselben
  Konstruktion, 15 davon live.
- Der Autor eines Befunds ist der schlechteste Prüfer seines Fixes: Die Probe teilt den blinden
  Fleck, der den Defekt erzeugt hat. Wer den Fix schreibt, sollte die Klasse nicht als geschlossen
  zertifizieren.
- Bevorzugen Sie eine *kausale* Prüfung (eine Eigenschaft, die alle Varianten verletzen müssen)
  gegenüber einer Prüfung, die Schreibweisen aufzählt.

## Fallstricke {#gotchas}

- **Problem:** Ein Gate wird hinzugefügt, ist sofort grün und wird von da an vertraut – war aber
  schon grün, bevor das Feature existierte. -> **Lösung:** Führen Sie vor dem Merge jedes Gates
  einen bewusst fehlerhaften Input aus und verlangen Sie Rot. Ein Gate, dessen erstes Ergebnis grün
  ist, hat seine Funktionsfähigkeit nicht nachgewiesen.
- **Problem:** Die Prüfung durchsucht das eigene Log nach einem Erfolgswort, sodass eine
  Umformulierung der Meldung das Urteil stillschweigend kippt. -> **Lösung:** Urteilen Sie anhand
  des Exit-Status oder strukturierter Ausgabe; siehe [[three-state-check-aggregation]].
- **Problem:** Hohe Zeilenabdeckung dient als Qualitätsmetrik, während die Assertions dünn sind.
  Alle Mutanten überleben, und niemand bemerkt es. -> **Lösung:** Berichten Sie überlebende
  Mutanten statt Abdeckungsprozente und behandeln Sie die Überlebenden als Arbeitsliste.
- **Problem:** Der Negativkontroll-Lauf lässt den Gegenstand verschoben zurück, weil die Prüfung
  mitten im Lauf abstürzte. -> **Lösung:** Stellen Sie den Gegenstand in einem `finally`-Block
  wieder her (oder arbeiten Sie auf einer Kopie) und prüfen Sie vor dem Beenden, dass er wieder
  an Ort und Stelle ist.
- **Problem:** Ein „Verifikations“-Schritt führt den Generator erneut aus und vergleicht ihn mit
  sich selbst, sodass beide Seiten gemeinsam wandern und Abweichungen unmöglich sind. ->
  **Lösung:** Fixieren Sie eine Seite per Digest oder vergleichen Sie mit einem Artefakt eines
  unabhängigen Erzeugers.
- **Problem:** Die Fixture-Suite enthält nur Must-pass-Fälle, sodass ein kaputtes Instrument, das
  immer mit 0 endet, seinen eigenen Selbsttest besteht. -> **Lösung:** Mindestens eine Fixture, die
  ein Erfolgswort ausgibt und trotzdem als rot beurteilt werden muss.

## Siehe auch {#see-also}

- [[three-state-check-aggregation]] – PASS / FAIL / UNKNOWN und fail-closed Aggregation
- [[test-architecture]] – wo Gates in der Suite angesiedelt sind
- [[ci-cd-test-automation]] – Selbsttests und Mutationsläufe in der Pipeline ausführen
- [[pytest-fundamentals]] – Assertion-Stile, die tatsächlich fehlschlagen
- [[chaos-engineering-and-testing]] – Fault Injection als Negativkontrolle auf Systemebene
- [[agent-evaluation]] – dasselbe Problem für Bewerter von Agenten-Ausgaben
