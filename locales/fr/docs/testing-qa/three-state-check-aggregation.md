---
title: "Agrégation de vérifications à trois états"
description: "PASS / FAIL / UNKNOWN au lieu de réussite-échec : contrats de code de sortie, agrégation fail-closed, alarmes d'absence de signal, et pourquoi chercher un verdict dans du texte finit par afficher vert sur un système en panne."
level: 3
source_sha256: 0460b5c7e53060dc5e655f5465299af96d34ee3294c311649ace92a97a23500c
translation: machine
translated_at: '2026-10-24'
---
# Agrégation de vérifications à trois états {#three-state-check-aggregation}

Un mécanisme de vérification doit distinguer trois issues, et non deux. Fusionner la troisième
avec la première constitue le défaut : **l'absence de signal devient indiscernable d'un bon
état de santé**, et l'erreur tombe toujours du côté dangereux, car une vérification non
exécutée ressemble exactement à une défaillance absente.

| État | Signification | Action du consommateur |
|---|---|---|
| `PASS` | Exécutée, conforme à l'attendu | Continuer |
| `FAIL` | Exécutée, non conforme | Corriger le système |
| `UNKNOWN` | **Non exécutée, ou impossible à trancher** | Pas de vert. Déterminer pourquoi elle n'a pas été exécutée |

## Contrat de code de sortie {#exit-code-contract}

Le canal machine est le statut de sortie. Le texte affiché est destiné aux humains et dérive
dès qu'un message est reformulé.

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

Le code `UNKNOWN` doit être **déclaré**, et non déduit. Un consommateur qui conclut que « 2
signifie probablement ignorée » fait de la recherche dans le texte, avec des étapes en plus.
Déclarez-le dans le manifeste que lit l'agrégateur :

```json
{
  "checks": [
    {"id": "schema", "cmd": ["python", "checks/schema.py"], "timeout_sec": 120},
    {"id": "smoke",  "cmd": ["python", "checks/smoke.py"],  "timeout_sec": 300}
  ],
  "unknown_exit_codes": [2]
}
```

## Agrégation fail-closed {#fail-closed-aggregation}

Le vert n'est émis que si **chaque** vérification attendue a été exécutée et a réussi. Un
seul `UNKNOWN` suffit à retenir le vert. Un résultat qui n'est jamais arrivé est `UNKNOWN`,
et non « rien à signaler ».

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

Trois propriétés assurent ce comportement : le verdict provient du code de retour, un
plantage ou un dépassement de délai aboutit à `UNKNOWN` au lieu d'être perdu, et un résultat
manquant est matérialisé en `UNKNOWN` au lieu d'être omis du rapport.

## L'absence de signal est une alerte {#absence-of-signal-is-an-alarm}

Un moniteur qui cesse de remonter des données ressemble, de l'extérieur, exactement à un
système calme.

- **Watchdog toujours déclenché.** Une règle qui se déclenche sans condition (`vector(1)`
  dans Prometheus) prouve que toute la chaîne (moteur de règles, alertmanager, récepteur) est
  vivante. Lorsqu'elle se tait, le silence *est* l'alarme.
- **Série manquante.** `absent()` / `absent_over_time(metric[15m])` transforme « aucune donnée »
  en condition déclenchante. Sans cela, un exporter planté donne un tableau de bord plat et
  silencieux.
- **Silence du rapporteur.** Un superviseur qui ne s'est pas manifesté dans les
  `SILENCE_MINUTES` déclenche sa propre alarme. Un watchdog mort ne doit pas pouvoir paraître
  en bonne santé.

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

## Une répétition supprimée n'est pas un signe de bonne santé {#suppressed-repeat-is-not-health}

La déduplication et la suppression des répétitions sont un comportement correct, et une source
fréquente de journaux trompeurs : une alerte déjà livrée n'est pas renvoyée, et le rapporteur
affiche « tout est vert » parce qu'il n'a vu aucune alerte *nouvelle* pendant ce cycle.

Journalisez les deux situations différemment :

```text
all green: 0 findings
suppressed: 16 findings still open, alarms already delivered (no new alerts this cycle)
```

Un superviseur qui a affiché « tout est vert » pendant 72 cycles consécutifs, alors que 16
constats restaient ouverts, ne mentait pas sur les constats : il mentait sur la *nature de son
propre silence*.

## Résultats structurés, pas de texte libre {#structured-results-not-prose}

Les formats de rapport CI (JUnit XML, TAP, CTRF) existent parce que le texte libre n'est pas
un contrat. Une étape de synthèse lit le résultat structuré ou le code de retour ; elle ne
recherche jamais un mot.

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

Sans `set -o pipefail`, le pipeline renvoie le code de sortie de `tee`, et chaque échec en
aval d'un tube est alors lu comme un succès.

## Pièges {#gotchas}

- **Problème :** l'agrégateur cherche `FAIL` dans la sortie standard, et une vérification
  écrite plus tard affiche « MISMATCH » ou un mot localisé. La suite passe au vert alors que
  des défauts réels subsistent. -> **Correctif :** juger d'après le code de sortie ou un
  rapport structuré ; ne considérer le texte affiché que comme destiné aux humains.
  Uniformiser la formulation règle un cas, et casse le suivant dès qu'un autre auteur intervient.
- **Problème :** `sys.exit(main())` où `main()` peut atteindre la fin sans instruction de retour
  et renvoyer `None`. `None` correspond à une sortie 0, donc chaque chemin d'échec signale un
  succès. -> **Correctif :** chaque branche renvoie un code explicite ; vérifier le type de
  retour dans un test.
- **Problème :** une vérification qui n'a pas pu s'exécuter (binaire absent, identifiants
  manquants, cible injoignable) est silencieusement omise du rapport, de sorte que la synthèse
  n'affiche que des succès. -> **Correctif :** matérialiser chaque vérification déclarée ; un
  résultat manquant est `UNKNOWN` et bloque le vert.
- **Problème :** une sonde répond sur la mauvaise cible : la file est lue sur un port alors que
  le conteneur redémarré écoute sur un autre, et la mauvaise réponse a la même forme que la
  bonne. -> **Correctif :** la sonde renvoie l'identité de ce qu'elle a mesuré (point de
  terminaison, identifiant de conteneur, révision), et le consommateur vérifie cette identité.
- **Problème :** les dépassements de délai et les signaux sont rangés dans `FAIL`, si bien
  qu'un problème d'infrastructure intermittent est indiscernable d'un échec d'assertion réel
  et finit « corrigé » par de simples relances. -> **Correctif :** dépassement de délai, arrêt
  par signal et échec de lancement sont `UNKNOWN` ; seule une exécution achevée en désaccord
  avec l'attendu est `FAIL`.
- **Problème :** une alerte se répète indéfiniment pour une condition bloquée déjà connue, si
  bien que ses lecteurs finissent par la mettre en sourdine. Un canal que les équipes apprennent
  à ignorer est pire que l'absence de canal. -> **Correctif :** supprimer la répétition, mais
  garder visible le nombre de constats en cours dans le rapport périodique.

## Voir aussi {#see-also}

- [[negative-controls-for-verification]] - prouver qu'une vérification peut effectivement passer au rouge
- [[ci-cd-test-automation]] - là où le contrat de code de sortie est consommé
- [[monitoring-and-observability]] - watchdog et alertes d'absence en pratique
- [[observability-query-languages]] - `absent_over_time` et compagnie
- [[sre-incident-management]] - fatigue d'alerte et politique de suppression
- [[test-architecture]] - couches de reporting et formats de résultats
- [[winhttp-async-client]] - le dépassement de délai comme troisième issue dans le code client
