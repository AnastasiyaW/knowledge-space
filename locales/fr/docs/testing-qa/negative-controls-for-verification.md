---
title: "Contrôles négatifs pour la vérification"
description: "Une coche verte ne prouve rien tant qu'elle n'a pas été vue capable de passer au rouge. Protocole de masquage du sujet, fixtures à échec obligatoire, test de mutation comme mesure du risque résiduel, et l'anti-pattern de la preuve auto-certifiante."
level: 3
source_sha256: f2f1eed6fdc0c882cf3e76f32aa8553503b9d9e755872d3d067ed6f80c01e9fb
translation: machine
translated_at: '2026-10-24'
---
# Contrôles négatifs pour la vérification {#negative-controls-for-verification}

Tout instrument a besoin d'un cas qui **doit** revenir en rouge. Sans lui, un résultat vert
ne porte aucune information : il est tout aussi compatible avec « le système est correct »
qu'avec « l'instrument ne peut rien détecter ». Un test sans assertion ne peut pas échouer ;
une porte qui lit le mauvais fichier ne peut pas échouer ; une preuve qui ne touche jamais
à son sujet ne peut pas échouer.

## La mesure : masquer le sujet, exiger le rouge {#the-measurement-hide-the-subject-demand-red}

Le protocole tient en une ligne et tranche la question mécaniquement.

1. Déclarer ce que la vérification porte (le *sujet*) et le figer par son empreinte.
2. Supprimer, corrompre ou remplacer le sujet.
3. Lancer la vérification. Elle **doit** renvoyer un code non nul.
4. Si elle reste verte, c'est l'instrument qui est cassé - pas le système.

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

**Référence mesurée lors d'un audit de 18 scripts de preuve :** 16 sont restés verts dans un
monde ne contenant que le script lui-même - 6 n'assertaient rien, 10 vérifiaient des
artefacts qu'ils venaient d'écrire, 1 sortait de son propre périmètre, 1 ne se reproduisait
pas. Leurs codes de sortie n'ont pas changé après la suppression de ce qu'ils prétendaient
prouver.

## Fixtures à échec obligatoire dans l'auto-test {#must-fail-fixtures-in-the-self-test}

Un instrument livre sa propre suite, et cette suite doit contenir des cas rouges par
construction. La fixture la plus précieuse est celle qui **affiche un succès et sort avec un
code non nul**, car elle distingue « lit le texte » de « lit le statut ».

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

Exécutez l'auto-test en CI à chaque modification de l'instrument. Un instrument sans
auto-test est une affirmation non vérifiée sur la vérification.

## Test de mutation : la forme générale {#mutation-testing-the-general-form}

Les contrôles négatifs se généralisent en test de mutation. On injecte un petit changement
sémantique dans le code testé, puis on relance la suite :

- **Mutant tué** - au moins un test a échoué. La suite détecte cette classe de défaut.
- **Mutant survivant** - tous les tests sont passés sur du code faux. C'est un **risque
  résiduel**, mesuré plutôt que supposé.

```bash
# Python: mutmut / cosmic-ray. JS/TS: Stryker. Java: PIT.
mutmut run --paths-to-mutate src/pricing.py
mutmut results          # survivors are the report; coverage percentage is not
```

La couverture de lignes ne peut pas remplacer cette mesure. Le code exécuté par un test
sans assertion est couvert à 100 % et vérifié à 0 % - c'est exactement la forme qui fait
survivre tous les mutants.

Appliquez la même idée à toute porte, pas seulement aux tests unitaires : modifiez la logique
propre de la vérification d'une façon qui devrait la faire échouer (lire le mauvais champ,
comparer à une constante, inverser la comparaison) et confirmez que le verdict change.
Les mutations dont on sait qu'elles ne peuvent pas changer le comportement sont des
*mutants équivalents* ; consignez-les comme tels plutôt que de les compter comme des échecs
de détection.

## La preuve auto-certifiante {#the-self-certifying-proof}

L'anti-pattern récurrent : un script écrit un artefact, puis vérifie l'artefact qu'il vient
d'écrire.

```python
# WRONG - proves the script can write a file, nothing about the system
out = run_pipeline()
Path("evidence.json").write_text(json.dumps(out))
assert json.loads(Path("evidence.json").read_text())["status"] == "ok"
```

Elle est verte sur une machine où le sujet n'existe pas du tout. La correction consiste à
faire dépendre la preuve de quelque chose qu'elle n'a pas produit : une empreinte d'entrée
figée, une réponse du service réel, un artefact construit par une autre étape, un fichier
dont l'absence ne peut pas être masquée.

```python
# RIGHT - the proof is bound to an external subject it cannot fabricate
manifest = json.loads(Path("proof.manifest.json").read_text(encoding="utf-8"))
subject = Path(manifest["subject"])                      # produced elsewhere
assert digest(subject) == manifest["subject_sha256"]     # cannot pass if it is missing
assert probe_real_endpoint(manifest["endpoint"]).status_code == 200
```

## Là où les suites vertes deviennent aveugles {#where-green-suites-go-blind}

Une suite qui passe est une preuve sur les formes que quelqu'un a imaginées. Elle ne dit
rien sur les formes que personne n'a énumérées.

- Un garde écrit contre une liste d'orthographes ne couvre que cette liste. Un cas mesuré :
  un correctif a fermé une voie de contournement, sa propre sonde l'a confirmé, 32 tests
  sont passés - et un relecteur indépendant a trouvé 18 variantes supplémentaires de la même
  construction, dont 15 exploitables.
- L'auteur d'une découverte est le pire relecteur de son correctif : la sonde partage l'angle
  mort qui a produit le défaut. Celui qui écrit le correctif ne devrait pas certifier la
  classe comme fermée.
- Privilégiez une vérification *causale* (une propriété unique que toutes les variantes
  doivent violer) plutôt qu'une vérification qui énumère les orthographes.

## Pièges courants {#gotchas}

- **Problème :** une porte est ajoutée, passe au vert immédiatement, et est dès lors
  considérée comme fiable - alors qu'elle était verte avant même l'existence de la
  fonctionnalité. -> **Correction :** avant de fusionner toute porte, exécutez-la sur une
  entrée délibérément cassée et exigez le rouge. Une porte dont le premier résultat est vert
  n'a pas été démontrée fonctionnelle.
- **Problème :** la vérification cherche un mot de succès dans son propre journal, donc
  reformuler le message fait basculer le verdict en silence. -> **Correction :** statuez sur
  le code de sortie ou une sortie structurée ; voir [[three-state-check-aggregation]].
- **Problème :** une couverture de lignes élevée sert de métrique de qualité alors que les
  assertions sont minces. Tous les mutants survivent et personne ne s'en aperçoit. ->
  **Correction :** rapportez les mutants survivants, pas le pourcentage de couverture ;
  traitez les survivants comme une liste de travail.
- **Problème :** l'exécution du contrôle négatif laisse le sujet déplacé parce que la
  vérification a planté en cours de route. -> **Correction :** restaurez dans un bloc
  `finally` (ou travaillez sur une copie), et vérifiez que le sujet est bien revenu avant de
  quitter.
- **Problème :** une étape de « vérification » relance le générateur et le compare à lui-même,
  donc les deux côtés bougent ensemble et le désaccord est impossible. -> **Correction :**
  figez un côté par son empreinte, ou comparez à un artefact issu d'un producteur
  indépendant.
- **Problème :** la suite de fixtures ne contient que des cas à réussite obligatoire, donc un
  instrument cassé qui sort toujours avec 0 réussit son propre auto-test. -> **Correction :**
  au moins une fixture qui affiche un mot de succès et doit tout de même être jugée rouge.

## Voir aussi {#see-also}

- [[three-state-check-aggregation]] - PASS / FAIL / UNKNOWN et agrégation fail-closed
- [[test-architecture]] - où vivent les portes dans la suite
- [[ci-cd-test-automation]] - exécution des auto-tests et des campagnes de mutation dans le pipeline
- [[pytest-fundamentals]] - styles d'assertion qui échouent réellement
- [[chaos-engineering-and-testing]] - injection de fautes comme contrôle négatif à l'échelle système
- [[agent-evaluation]] - le même problème pour les évaluateurs de sorties d'agents
