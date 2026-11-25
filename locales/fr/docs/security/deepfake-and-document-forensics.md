---
title: "Deepfake et criminalistique documentaire"
category: concepts
tags: [security, deepfake, forensics, image-analysis, anti-fraud, document-forgery]
level: 3
source_sha256: 3fdcb85f11f638a8ffb08da5f8e9f07018cabf6973eadbc1017571912511bda5
translation: machine
translated_at: '2026-10-24'
---
# Deepfake et criminalistique documentaire {#deepfake-and-document-forensics}

Détection et analyse de contenus falsifiés : technologies de deepfake vidéo/audio et méthodes de détection, techniques de falsification de documents et vérification, criminalistique de l'image (ELA, hachage perceptuel, détection de clonage) et analyse d'usurpation d'e-mails.

## Faits clés {#key-facts}
- Le clonage vocal moderne atteint une fidélité d'environ 99 % à partir de quelques minutes d'audio d'exemple
- Error Level Analysis (ELA) détecte les régions d'image manipulées grâce aux différences d'artefacts de compression JPEG
- Le hachage perceptuel produit des empreintes similaires pour des images similaires (contrairement au hachage cryptographique)
- SPF, DKIM et DMARC, pris ensemble, empêchent l'usurpation d'e-mails : vérifiez les trois pour valider un message
- Les métadonnées EXIF survivent à la plupart des retouches, mais sont supprimées par les plateformes de réseaux sociaux
- Des outils de deepfake en temps réel pour les appels vidéo existent désormais sur le marché

## Technologie deepfake {#deepfake-technology}

### Composants {#components}
1. **Synthèse faciale** - modèles d'IA entraînés sur le visage de la cible (des centaines à des milliers de photos)
2. **Synthèse vocale** - clonage de voix à partir d'échantillons audio (~99 % de fidélité à partir de quelques minutes d'audio)
3. **Synchronisation labiale** - adaptation de la parole générée aux mouvements du visage

### Méthodes de détection {#detection-methods}
- **Analyse du clignement** - les premiers deepfakes ne simulaient pas un clignement des yeux naturel
- **Artefacts de frontière faciale** - coutures là où la superposition du visage rencontre l'arrière-plan
- **Synchronisation audio-visuelle** - subtils décalages entre mouvements de la bouche et parole
- **Analyse fréquentielle** - les images générées par GAN présentent des motifs détectables dans le domaine fréquentiel
- **Analyse des métadonnées** - les vidéos générées ne contiennent pas les métadonnées de caméra attendues

## Falsification de documents {#document-forgery}

### Types de documents falsifiés {#types-of-forged-documents}
- Documents d'identité (passeports, permis de conduire)
- Documents financiers (relevés bancaires, déclarations fiscales, factures)
- Documents d'entreprise (lettres d'embauche, statuts de société)
- Selfies de vérification KYC accompagnés de documents

### Méthodes de vérification {#verification-methods}
- **Métadonnées EXIF** - date de création, logiciel utilisé, informations sur l'appareil
- **Correspondance de gabarits** - comparaison avec des modèles de documents authentiques connus
- **Recoupement en base de données** - vérification des numéros de document auprès des bases officielles
- **Contrôles UV/hologrammes** - vérification physique des documents imprimés

## Criminalistique de l'image {#image-forensics}

### Error Level Analysis (ELA) {#error-level-analysis-ela}
Détecte les régions manipulées en analysant les artefacts de compression JPEG :
- Réenregistrer l'image à un niveau de qualité connu
- Comparer avec l'original pixel par pixel
- Les régions manipulées présentent des niveaux de compression différents (plus claires dans la sortie ELA)

### Hachage perceptuel {#perceptual-hashing}
- Images réduites à des valeurs de hachage compactes
- Des images similaires produisent des hachages similaires
- Utilisé pour : la détection de documents frauduleux connus, la correspondance avec des bases de données
- Permet de parcourir des milliards d'images sans revue humaine

### Techniques complémentaires {#additional-techniques}
- **Détection de clonage** - repérage de régions copiées-collées au sein d'une même image
- **Analyse de l'éclairage et des ombres** - des sources lumineuses incohérentes révèlent un montage
- **Analyse du bruit** - des appareils ou capteurs différents produisent des motifs de bruit différents
- **Extraction des données EXIF** - modèle d'appareil, GPS, date, logiciel de retouche

## Criminalistique des e-mails {#email-forensics}

### Analyse des en-têtes {#header-analysis}
```sql
Received: chain   - traces routing path from sender to recipient
X-Originating-IP  - may reveal sender's real IP
Message-ID         - domain should match sender
Return-Path        - vs From: mismatches indicate spoofing
```

### Détection d'usurpation {#spoofing-detection}
- Vérifier l'alignement de l'enregistrement SPF (expéditeur de l'enveloppe vs From de l'en-tête)
- Vérifier la signature cryptographique DKIM
- Évaluer la politique DMARC
- Analyser la cohérence de la chaîne d'en-têtes
- Rechercher les indicateurs de BEC (Business Email Compromise)

## Signaux anti-fraude de Google {#google-anti-fraud-signals}
Modèle de confiance unifié de Google à travers ses services :
- Numéro de téléphone : type d'opérateur (VoIP ou mobile), ancienneté du numéro, schémas de réutilisation
- Empreinte d'appareil et réputation de l'IP lors de l'inscription
- Schémas comportementaux après l'inscription (activité humaine ou robotisée)
- Ancienneté du compte et historique d'activité

### Schémas d'abus courants {#common-abuse-patterns}
- Revente de comptes (la valeur augmente avec l'ancienneté, la vérification téléphonique et l'éligibilité aux services)
- Abus des hébergements cloud (crédits d'essai de 1 $ pour des ressources de calcul)
- Fraude AdSense (fausses impressions et faux clics)
- Fausses entreprises sur Maps (manipulation du référencement et de la réputation)

## Pièges à éviter {#gotchas}
- La détection de contenus générés par IA est une course aux armements : les méthodes de détection présentent des taux de faux négatifs croissants
- ELA ne fonctionne que sur le JPEG (artefacts de compression avec pertes), pas sur PNG ou BMP
- Les données EXIF peuvent être modifiées ou supprimées très facilement : l'absence d'EXIF ne constitue pas une preuve de falsification
- Le hachage perceptuel peut être contourné par une transformation suffisante de l'image
- Un résultat SPF positif ne vérifie que le domaine de l'expéditeur de l'enveloppe, et non le From de l'en-tête affiché à l'utilisateur
- Les deepfakes en appel vidéo sont détectables en demandant à la personne d'effectuer des actions inattendues (se tourner de profil, cacher partiellement son visage)

## Voir aussi {#see-also}
- [[osint-and-reconnaissance]] - extraction de métadonnées, collecte de preuves
- [[anti-fraud-behavioral-analysis]] - signaux comportementaux de fraude
- [[browser-and-device-fingerprinting]] - identification des appareils
- [[compliance-and-regulations]] - protection des données dans les enquêtes
