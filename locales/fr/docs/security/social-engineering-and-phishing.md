---
title: "Ingénierie sociale et hameçonnage"
category: concepts
tags: [security, social-engineering, phishing, email-security, human-factors]
level: 3
source_sha256: be8bac5e9ebee7d11d688df8534bb2ff122d3799eff12913f8e708c351a10e31
translation: machine
translated_at: '2026-10-24'
---
# Ingénierie sociale et hameçonnage {#social-engineering-and-phishing}

Vecteurs d'attaque ciblant l'humain : hameçonnage (spear phishing, whaling, vishing), pretexting, détection d'usurpation d'e-mail (SPF/DKIM/DMARC), analyse des en-têtes d'e-mail et techniques d'investigation dans les bases de fuites de données.

## Points clés {#key-facts}
- Le spear phishing cible des personnes précises avec un contenu personnalisé ; le whaling cible les dirigeants
- SPF + DKIM + DMARC ensemble empêchent l'usurpation d'e-mail : vérifiez les trois
- Les pertes liées à la compromission de messagerie professionnelle (BEC) dépassent les pertes dues aux rançongiciels à l'échelle mondiale
- La chaîne `Received:` de l'en-tête d'un e-mail retrace l'ensemble du chemin de routage
- Les bases de fuites de données (HIBP) permettent des attaques par réutilisation d'identifiants sur plusieurs services
- L'ingénierie sociale physique (tailgating, usurpation d'identité) contourne l'ensemble des contrôles numériques

## Types d'hameçonnage {#phishing-types}

| Type | Cible | Méthode |
|------|-------|---------|
| Phishing | Masse/aléatoire | E-mails génériques, fausses pages de connexion |
| Spear phishing | Personnes précises | Contenu personnalisé, adapté au contexte |
| Whaling | Dirigeants/C-suite | Usurpation de membres du conseil d'administration, du service juridique |
| Vishing | Cibles téléphoniques | Usurpation d'identité par la voix |
| Smishing | Destinataires de SMS | Liens malveillants envoyés par SMS |

## Outils de campagnes d'hameçonnage {#phishing-campaign-tools}
- **GoPhish** - framework open source d'hameçonnage pour les tests de sensibilisation
- **King Phisher** - boîte à outils de campagnes d'hameçonnage
- Pages de collecte d'identifiants
- Pièces jointes malveillantes : documents avec macros, HTML smuggling

## Pretexting {#pretexting}
Création de scénarios fabriqués pour manipuler les cibles :
- Usurpation du support informatique (« Nous avons besoin de vos identifiants pour résoudre un problème »)
- Usurpation d'un fournisseur (« Facture en retard de paiement »)
- Usurpation d'un dirigeant (« Virement urgent nécessaire »)
- Physique : suivre quelqu'un pour franchir une porte sécurisée, porter de faux badges

## Authentification des e-mails {#email-authentication}

### SPF (Sender Policy Framework) {#spf-sender-policy-framework}
Enregistrement DNS TXT listant les adresses IP des serveurs de messagerie autorisés :
```ini
v=spf1 mx ip4:203.0.113.0/24 include:_spf.google.com -all
```

### DKIM (DomainKeys Identified Mail) {#dkim-domainkeys-identified-mail}
Signature cryptographique dans les en-têtes d'e-mail prouvant l'intégrité du message et le domaine de l'expéditeur.

### DMARC (Domain-based Message Authentication) {#dmarc-domain-based-message-authentication}
Politique de traitement des échecs SPF/DKIM :
```ini
v=DMARC1; p=reject; rua=mailto:dmarc@example.com
```
Politiques : `none` (surveillance), `quarantine` (dossier spam), `reject` (blocage).

## Analyse des en-têtes d'e-mail {#email-header-analysis}
```sql
Received: chain          - full routing path (read bottom-up)
X-Originating-IP         - sender's real IP
Message-ID               - domain should match sender
Return-Path vs From      - mismatch = likely spoofing
Authentication-Results    - SPF/DKIM/DMARC pass/fail
```

## Investigation dans les bases de fuites de données {#breach-database-investigation}
- **Have I Been Pwned** (HIBP) - vérification légitime des fuites de données
- **DeHashed / IntelX** - recherche avancée dans les données de fuites (incluant les mots de passe)
- E-mail -> mot de passe issu d'une fuite -> réutilisation de l'identifiant sur d'autres services
- Holehe : vérifier si une adresse e-mail est enregistrée sur des services sans alerter l'utilisateur

## Pièges courants {#gotchas}
- Le succès SPF seul ne prévient pas l'usurpation du nom affiché (From: « Nom du PDG » <attacker@evil.com>)
- DMARC `p=none` assure la surveillance mais aucune protection : il faut `p=quarantine` ou `p=reject`
- La formation à la sensibilisation à la sécurité réduit le taux de clics sans jamais l'éliminer (certains employés cliquent toujours)
- L'hameçonnage avancé utilise des comptes légitimes compromis, qui passent toutes les vérifications d'authentification
- Les contenus d'hameçonnage générés par IA sont de plus en plus indiscernables des communications légitimes

## Voir aussi {#see-also}
- [[penetration-testing-methodology]] - ingénierie sociale dans les tests d'intrusion
- [[osint-and-reconnaissance]] - collecte d'informations pour un hameçonnage ciblé
- [[siem-and-incident-response]] - procédures de réponse à l'hameçonnage
- [[anti-fraud-behavioral-analysis]] - détection de l'hameçonnage à grande échelle
