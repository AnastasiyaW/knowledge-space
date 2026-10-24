---
description: "Fiches de référence sur les vulnérabilités CWE structurées pour la revue de code assistée par IA. Causes profondes, conditions de déclenchement, heuristiques de détection et schémas de correction pour le Top 25 CWE."
date: 2026-04-16
tags:
  - security
  - cwe
  - vulnerability-detection
level: Advanced
source_sha256: d234d6cf5ac564a188dd03e276355497a028e9bdb47dcd6279f0863c196c7653
translation: machine
translated_at: '2026-10-24'
---
# Fiches de référence sur les vulnérabilités CWE {#cwe-vulnerability-reference-cards}

Entrées de connaissances structurées pour la détection de vulnérabilités assistée par IA, suivant l'approche Vul-RAG (ACM TOSEM 2025). Chaque entrée couvre : la sémantique fonctionnelle, la cause profonde, les conditions de déclenchement, les heuristiques de détection et les schémas de correction.

Conçues pour être exploitées par des agents de revue de sécurité. Chaque fiche est autonome : un agent qui lit une fiche dispose de tout ce qui est nécessaire pour détecter cette classe de vulnérabilité.

Basées sur le Top 25 des faiblesses logicielles les plus dangereuses du CWE (2024).

## Entrées {#entries}

### Injection et validation des entrées {#injection-input-validation}

- CWE-079: XSS - Cross-site Scripting (Rang 1)
- [[cwe-089-sql-injection]] - Injection SQL (Rang 3)
- [[cwe-918-ssrf]] - Falsification de requête côté serveur (Rang 19)
- CWE-434: File Upload - Téléversement de fichiers non restreint (Rang 10)
- [[cwe-502-deserialization]] - Désérialisation de données non fiables (Rang 16)

### Sécurité de la mémoire {#memory-safety}

- [[cwe-787-oob-write]] - Écriture hors limites (Rang 2)
- CWE-125: Out-of-Bounds Read - Lecture hors limites (Rang 6)
- CWE-416: Use After Free - Utilisation après libération (Rang 8)
- CWE-190: Integer Overflow - Dépassement d'entier (Rang 23)

### Gestion des ressources {#resource-management}

- [[cwe-400-resource-consumption]] - Consommation de ressources non contrôlée (Rang 24)

## Méthodologie {#methodology}

Chaque entrée suit la structure de connaissances Vul-RAG :

1. **Sémantique fonctionnelle** - ce que fait le code vulnérable (schéma comportemental, non syntaxique)
2. **Cause profonde** - pourquoi la vulnérabilité existe (défaut de conception fondamental)
3. **Conditions de déclenchement** - quand la faille est exploitable et quand elle ne l'est PAS (indicateurs de faux positifs)
4. **Heuristiques de détection** - ce qu'il faut rechercher lors de la revue (motifs source-puits, contrôles manquants)
5. **Schémas de correction** - comment corriger (modèles de correction) et anti-patrons (corrections erronées)

Cette structure surpasse le RAG basé sur des exemples de code de +16 à 24 % en précision (Vul-RAG, ACM TOSEM 2025).
