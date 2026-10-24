---
title: "Analyse comportementale anti-fraude"
category: concepts
tags: [security, anti-fraud, behavioral-analysis, keystroke-dynamics, payment-fraud]
level: 3
source_sha256: 1c58d1d3acbe0da6f45754ed9496a17b281181e724844539851532c9c457a26a
translation: machine
translated_at: '2026-10-24'
---
# Analyse comportementale anti-fraude {#anti-fraud-behavioral-analysis}

Signaux comportementaux utilisés par les systèmes anti-fraude : schémas de mouvement de la souris, dynamique de frappe au clavier, analyse du rythme des sessions, détection de fraude au paiement (contrôles de vélocité, analyse des BIN, 3D Secure) et signaux de notation sociale.

## Faits clés {#key-facts}
- Les trajectoires du curseur humain suivent des chemins de type Bézier ; les bots utilisent une interpolation linéaire
- La dynamique de frappe (temps d'appui, temps de vol) permet d'identifier des utilisateurs individuels sans identifiants
- Les contrôles de vélocité détectent des schémas de fraude : plusieurs cartes depuis le même appareil, impossibilité géographique
- Le BIN (les 6 à 8 premiers chiffres) révèle la banque émettrice, le type de carte, le pays et le statut particulier ou professionnel
- 3D Secure transfère la responsabilité de la fraude du marchand vers l'émetteur de la carte
- Le scoring anti-fraude combine des centaines de signaux : une anomalie sur une seule dimension augmente le risque

## Schémas de mouvement de la souris {#mouse-movement-patterns}
- **Vitesse et accélération** : les bots se déplacent à vitesse constante ; les humains effectuent de micro-corrections
- **Précision des clics** : les humains manquent parfois leur cible ; les bots cliquent sur des coordonnées exactes
- **Courbes de déplacement** : les trajectoires humaines sont de type Bézier ; les bots utilisent une interpolation linéaire
- **Schémas d'inactivité** : pauses naturelles contre absence totale de mouvement
- **Comportement de défilement** : vitesse, changements de direction, inertie

## Dynamique de frappe (biométrie) {#keystroke-dynamics-biometrics}
Schémas de frappe propres à chaque utilisateur :
- **Temps d'appui** : durée pendant laquelle chaque touche est maintenue enfoncée
- **Temps de vol** : délai entre le relâchement d'une touche et l'appui sur la suivante
- **Vitesse de frappe** : mots par minute et régularité
- **Schémas d'erreur** : fréquence de la touche retour arrière, corrections courantes
- **Temps des digrammes et trigrammes** : délai entre des paires de lettres spécifiques

Ces données biométriques construisent des profils au fil du temps et permettent d'identifier des utilisateurs même sans identifiants de connexion.

## Analyse du rythme de session {#session-timing-analysis}
- Délai entre les chargements de pages
- Temps passé sur les formulaires avant soumission (trop rapide = bot, trop lent = fraude manuelle)
- Schémas de navigation (lecture du contenu ou accès direct au paiement)
- Durée des sessions et schémas de retour

## Détection de fraude au paiement {#payment-fraud-detection}

### Analyse des BIN (Bank Identification Number) {#bin-bank-identification-number-analysis}
Les 6 à 8 premiers chiffres révèlent :
- La banque émettrice et le pays
- Le type de carte : crédit, débit, prépayée, virtuelle
- La marque de la carte et son niveau (standard, gold, platinum)
- Carte de particulier ou carte professionnelle

Usages anti-fraude : vérifier que le pays de facturation correspond au pays du BIN, détecter les cartes virtuelles ou prépayées (risque de fraude plus élevé), appliquer des contrôles de vélocité par plage de BIN.

### Contrôles de vélocité {#velocity-checks}
- Nombre de transactions par carte sur une fenêtre temporelle donnée
- Nombre de cartes différentes provenant du même appareil ou de la même adresse IP
- Schémas de montants de transaction (petits montants de test avant les montants élevés)
- Vélocité géographique (transactions depuis des lieux éloignés dans un délai impossible)

### AVS (Address Verification System) {#avs-address-verification-system}
Comparaison de l'adresse de facturation avec les données de l'émetteur : concordance du numéro de voie et du code postal, concordance du pays entre la facturation et le BIN.

### 3D Secure (3DS) {#3d-secure-3ds}
- Authentification du titulaire via le portail de sa banque (Verified by Visa, Mastercard SecureCode)
- Transfère la responsabilité de la fraude du marchand vers l'émetteur
- 3DS2 : authentification basée sur le risque, avec parcours sans friction pour les transactions à faible risque

### Indicateurs de cartes virtuelles et prépayées {#virtualprepaid-card-indicators}
- Les cartes prépayées ne permettent pas de vérifier l'adresse de facturation
- Les cartes virtuelles sont souvent générées en masse
- Plages de BIN connues pour les produits prépayés et virtuels
- Historique de transactions limité pour l'évaluation du risque

## Signaux de notation sociale {#social-rating-signals}
- Ancienneté du compte et schémas d'activité
- Cohérence du profil sur les réseaux sociaux
- Domaine de l'adresse e-mail (gratuit ou professionnel)
- Validation du numéro de téléphone (VoIP ou opérateur, ancienneté du numéro)
- Cohérence comportementale avec l'identité déclarée

## Pièges courants {#gotchas}
- L'analyse de la souris et de la frappe peut être contournée par des outils de rejeu sophistiqués qui injectent un bruit de type humain
- Les contrôles de vélocité doivent tenir compte de cas légitimes (cartes professionnelles utilisées par plusieurs personnes, adresses IP partagées)
- Les utilisateurs de VPN ou de proxys ne sont pas nécessairement frauduleux : un scoring IP trop agressif génère des faux positifs
- La friction de 3DS réduit les taux de conversion : les marchands doivent arbitrer entre sécurité et perte de chiffre d'affaires
- La biométrie comportementale soulève des questions de confidentialité au regard du RGPD (les données biométriques sont une catégorie particulière)

## Voir aussi {#see-also}
- [[browser-and-device-fingerprinting]] - signaux d'empreinte au niveau de l'appareil
- [[tls-fingerprinting-and-network-identifiers]] - analyse IP et réseau
- [[deepfake-and-document-forensics]] - détection de falsification de documents
- [[compliance-and-regulations]] - implications du RGPD pour le suivi comportemental
