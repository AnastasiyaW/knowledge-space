---
level: 3
source_sha256: 9e6a9298ff4e77417bebac5f660e6308bc43dd89935d73e4bf5cf3d2e3e2a9ab
translation: machine
translated_at: '2026-10-24'
---
# Retouch4me : analyse concurrentielle {#retouch4me-competitive-analysis}

Date : 2026-04-03
Contexte : analyse architecturale et produit en vue du développement d'un produit concurrent de retouche.

---

## Profil de l'entreprise {#company-profile}

- **Entité juridique :** RELU OU (Estonie, Tallinn, Vesivarava 50-201)
- **Création :** 28 mars 2021. Immatriculation : 16194437
- **Fondateur :** Oleg Sharonov (également auteur de 3D LUT Creator)
- **Parcours :** développeur professionnel, a débuté avec des synthétiseurs virtuels. 8 ans d'expérience en retouche + 2 ans d'étude approfondie du deep learning
- **Chiffre d'affaires :** 2,63 M EUR (2023), TCAC de 19 %
- **Utilisateurs :** plus de 70 pays
- **Financement :** autofinancée (aucune levée externe identifiée)

---

## Gamme de produits {#product-line}

### 13 plugins photo {#13-photo-plugins}

Chaque plugin = réseau de neurones distinct, entraîné pour une tâche de retouche spécifique :

| Plugin | Tâche | Prix |
|--------|-------|------|
| Heal | Suppression des imperfections et boutons | 124 $ |
| Dodge & Burn | Dodge & burn haut de gamme automatisé | 149 $ |
| Skin Tone | Correction et uniformisation du teint | 124 $ |
| Mattifier | Suppression de la brillance et des reflets gras | 124 $ |
| Portrait Volumes | Ajout de profondeur et de volume | 124 $ |
| Skin Mask | Génération d'un masque de peau (visage/corps) | 124 $ |
| Eye Vessels | Suppression des vaisseaux rouges de l'œil | 124 $ (lot) |
| Eye Brilliance | Renforcement des reflets dans les yeux | 124 $ (lot) |
| White Teeth | Blanchiment des dents | 124 $ |
| Fabric | Suppression des plis du tissu | 124 $ |
| Clean Backdrop | Nettoyage de l'arrière-plan | 149 $ |
| Stray Hair | Suppression des cheveux parasites | 124 $ |
| Dust | Suppression des poussières et particules | 124 $ |

**Gratuits :** Panel (panneau Photoshop), Frequency Separation, Glasses Glare Removal (dans Apex), Face Make Lifting (dans Apex).

### 2 plugins vidéo {#2-video-plugins}

| Plugin | Tâche | Prix | Standard |
|--------|-------|------|----------|
| Dust OFX | Suppression des poussières et particules en vidéo | 349 $ | OFX |
| Color Match OFX | Harmonisation colorimétrique en vidéo | n/a | OFX |

Prise en charge OFX : DaVinci Resolve 18+, Nuke, VEGAS Pro, Natron, Assimilate SCRATCH.

### Apex : tout-en-un dans le cloud {#apex-cloud-all-in-one}

Produit phare stratégique. Inclut tous les plugins ; l'inférence s'exécute sur les serveurs de Retouch4me (cloud uniquement).
Fonctionne en autonome et en plugin (Photoshop, Lightroom, Affinity Photo).
Aucune configuration matérielle locale requise.

### Arams : application autonome {#arams-standalone-app}

Tous les plugins dans une seule application, traitement par lots (illimité), gestion de fichiers intégrée, sans Photoshop.

---

## Tarification {#pricing}

### Licence perpétuelle (plugins locaux) {#perpetual-license-local-plugins}
- 124 à 149 $ par plugin, à vie
- Mises à jour gratuites à vie
- 3 activations (1 active + 2 de secours)
- Liée au matériel

### Crédits cloud (Panel / Apex) {#cloud-credits-panel-apex}

| Forfait | Prix | Par photo |
|---------|------|-----------|
| Essai | Gratuit | 20 retouches |
| 100 retouches | 20 $ (paiement unique) | 0,20 $ |
| Basic | 20 $/mois | 200 (0,10 $) |
| Pro | 35 $/mois | 500 (0,07 $) |
| Business | 90 $/mois | 1500 (0,06 $) |

1 crédit = 1 photo retouchée téléchargée (un nombre quelconque d'outils peut être appliqué).

---

## Architecture technique {#technical-architecture}

### Moteur d'inférence {#inference-engine}

**Constat essentiel : Retouch4me utilise un moteur d'inférence propriétaire.**

D'après les entretiens avec Oleg Sharonov : plusieurs frameworks d'entraînement ML ont été testés, mais aucun n'était adapté à un déploiement sur poste de travail dans Photoshop. Un moteur sur mesure a été développé pour garder un contrôle total.

- **PAS d'ONNX, PAS de TensorFlow, PAS de PyTorch** pour l'inférence
- Moteur propriétaire utilisant **OpenCL** pour l'accélération GPU
- Inférence CPU via Intel OpenCL 1.1+
- Configuration requise : GPU avec 4 Go de VRAM minimum ou CPU Intel compatible OpenCL

### Architecture des réseaux de neurones {#neural-network-architecture}

- **CNN (réseaux de neurones convolutifs)** : cœur du système
- Architectures **encodeur-décodeur**
- **Convolutions partielles** : pour l'inpainting des zones endommagées
- **Pertes perceptuelles** : optimisation sur des métriques perceptuelles (caractéristiques extraites de réseaux pré-entraînés), et non sur la L2 au niveau du pixel
- Chaque plugin = réseau distinct entraîné sur des paires « avant/après » issues de retoucheurs professionnels

### Tailles des modèles {#model-sizes}

- Installeur Heal : environ 35 à 41 Mo (Windows), environ 20 Mo (macOS)
- **Modèles intégrés à l'installeur** : aucun téléchargement séparé des poids
- Indique des CNN compacts (quelques dizaines de Mo par module)
- Optimisé pour l'inférence OpenCL

### Modes de traitement {#processing-modes}

**Sur l'appareil (local) :**
- Moteur OpenCL propriétaire
- GPU ou CPU
- 4 Go de VRAM minimum
- Entièrement hors ligne après activation

**Retouche cloud (Panel/Apex) :**
- Inférence sur les serveurs de Retouch4me
- Serveur : `retoucher.hz.labs.retouch4.me`
- API REST avec des points de terminaison de tâches
- Aucune configuration matérielle locale requise

---

## API cloud {#cloud-api}

**URL de base :** `https://retoucher.hz.labs.retouch4.me/api/v1/`

Points de terminaison principaux :

| Point de terminaison | Méthode | Description |
|----------------------|---------|-------------|
| `/info/limits` | GET | Limites des fichiers (formats, taille, résolution) |
| `/retoucher/getFile/{id}` | GET | Récupération du fichier traité |
| création de tâche | POST | Création d'une tâche de retouche |
| statut de tâche | GET | Vérification du statut d'une tâche |

**Limites :** PNG/JPG/JPEG, 100 Mo maximum, 250 mégapixels maximum.

**Mode professionnel :** `mode=professional`, `layers=1` → le serveur renvoie une archive ZIP contenant les calques séparés.

---

## Configuration requise {#system-requirements}

**Windows :** Win 7/10/11 x64, 6 Go de RAM, CPU 1,2 GHz x64, GPU avec 4 Go de VRAM minimum et OpenCL, OU CPU Intel avec OpenCL 1.1+. Recommandé : RTX 3050 8 Go / RTX 4070Ti 12 Go.

**macOS :** 10.14+ (10.15+ pour les nouveaux produits), Mac 2015+ (Intel, M1-M4 prises en charge nativement).

---

## Licences et protection {#licensing-and-protection}

### Modèle de licence {#license-model}
- 1 clé active + 2 clés de secours (3 activations au total)
- Liée à la configuration matérielle
- 2 appareils actifs simultanément au maximum
- Un changement de matériel invalide la clé ; utiliser la clé de secours
- Clé supplémentaire : uniquement via le support, au minimum 6 mois après l'achat

### Mécanisme {#mechanism}
- Activation liée au matériel
- **Aucune désactivation en libre-service** (pas de tableau de bord utilisateur)
- Les anciennes activations ne peuvent pas être supprimées techniquement
- Changement d'ordinateur portable : contacter le support pour une nouvelle activation

### État de la piraterie {#anti-piracy-state}

D'après les forums russophones (diakov.net, 4pda.to) :
- Des versions « traitées » (crackées) existent, avec la vérification désactivée
- Retouch4me attribue de nombreux plantages aux versions piratées
- Les versions piratées déstabilisent parfois les plugins légitimes installés à côté
- Norton détecte parfois les plugins (probablement en raison de l'obfuscation de la protection)

---

## Faiblesses (opportunités concurrentielles) {#weaknesses-competitive-opportunities}

### Faiblesses principales {#primary-weaknesses}

1. **Prix :** 124 à 149 $ par plugin. La suite complète = plus de 1500 $. Obstacle élevé pour les photographes des marchés émergents.

2. **Fragmentation :** 13 plugins distincts. Aucune solution unifiée (Apex est cloud uniquement, sans mode hors ligne).

3. **UX de la licence (principale plainte) :** liaison au matériel sans désactivation en libre-service. Les utilisateurs perdent leurs activations lors d'un changement de matériel et doivent contacter le support. Délai de 6 mois pour obtenir des clés supplémentaires. Principale plainte sur Trustpilot.

4. **Contrôle utilisateur minimal :** un seul curseur d'intensité. Aucun contrôle par zone, aucun masque, aucun préréglage, aucun réglage fin.

5. **OpenCL uniquement :** pas d'optimisations spécifiques à CUDA, pas de shaders Metal. ONNX Runtime couvrirait CUDA/DirectML/CoreML/OpenVINO.

6. **Pas de SDK ni de bibliothèque intégrable :** plugin ou API uniquement. Impossible d'intégrer le moteur dans un pipeline personnalisé.

7. **Dépendance à Apex (cloud) :** Apex fonctionne UNIQUEMENT via le cloud, sans mode hors ligne.

### Opportunités architecturales {#technical-architecture-opportunities}

| Approche de Retouch4me | Meilleure alternative |
|------------------------|-----------------------|
| Moteur OpenCL propriétaire (investissement important) | ONNX Runtime (CUDA/DirectML/CoreML/OpenVINO) : développement plus rapide + compatibilité plus large |
| Filtre Photoshop in-process | Daemon out-of-process avec IPC (isolation des plantages) |
| 13 plugins distincts | Produit unique avec modules activables |
| Aucun tableau de bord utilisateur | Portail de désactivation de licence en libre-service |

---

## Synthèse du positionnement concurrentiel {#competitive-positioning-summary}

**Atouts de Retouch4me :** plus de 8 ans de présence sur le marché, données d'entraînement issues de retoucheurs professionnels, qualité éprouvée, licence perpétuelle appréciée des photographes, expansion vers la vidéo.

**Leurs vulnérabilités (notre opportunité) :**
1. Prix + fragmentation → produit unique à prix plus bas
2. UX de la licence → tableau de bord en libre-service, transfert flexible
3. Absence de réglage fin → intensité par zone, masques de calque, préréglages
4. Absence de SDK → bibliothèque intégrable pour pipelines personnalisés
5. OpenCL uniquement → ONNX Runtime pour une meilleure couverture GPU
6. Apex cloud uniquement → local + cloud unifiés avec repli hors ligne

---

## Points d'attention {#gotchas}

- **L'activation liée au matériel sans désactivation en libre-service est la principale plainte UX sur Trustpilot.** C'est un problème soluble (mettre en place un tableau de bord de gestion des appareils) et un différenciateur fort.
- **La contrainte OpenCL (4 Go de VRAM minimum) limite la portée du marché.** ONNX Runtime DirectML fonctionne sur tout GPU DX12 (jusqu'aux GPU intégrés pour des modèles plus simples), et CoreML exploite le Neural Engine d'Apple sur les Mac récents.
- **Les versions piratées qui provoquent des instabilités dans les installations légitimes** suggèrent que leur protection interagit avec le processus hôte de manière à causer des dommages collatéraux. Une architecture propre out-of-process évite ce problème.
- **La détection des plugins par Norton** représente une charge pour le support client. Les techniques d'obfuscation connues déclenchent les heuristiques des antivirus. Il faut trouver un équilibre entre la solidité de la protection et le taux de faux positifs.
- **« Pas de tableau de bord » n'est pas une fonctionnalité de sécurité**, c'est une défaillance UX. La désactivation en libre-service avec limites d'appareils (par exemple 2 simultanés, 5 transferts par an au total) est nettement préférable : elle réduit la charge du support, améliore la satisfaction et n'affaiblit pas sensiblement la protection.
- **Les modèles intégrés à l'installeur (environ 35 à 41 Mo)** font que la fréquence des mises à jour dépend d'une réinstallation complète. Une infrastructure de téléchargement séparée pour les modèles permettrait de les mettre à jour sans mettre à jour l'application.
