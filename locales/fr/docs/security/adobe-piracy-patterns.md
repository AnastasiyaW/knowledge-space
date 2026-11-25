---
level: 3
source_sha256: 1b62d63d7fca393a30ec7162cfe902fc736ceeffa5acdb3b77a5db4fb4d84f89
translation: machine
translated_at: '2026-10-24'
---
# Modèles d'attaque contre Adobe : catégories d'attaque et enseignements pour la protection des modèles de ML {#adobe-piracy-patterns-attack-categories-and-lessons-for-ml-protection}

Date : 2026-04-03
Contexte : recherche en sécurité défensive. Comprendre les schémas d'attaque contre Adobe pour concevoir une meilleure protection des produits de ML.

---

## Architecture d'Adobe Genuine Software (AGS) {#adobe-genuine-software-ags-architecture}

AGS est un service en arrière-plan qui vérifie l'authenticité des applications Adobe installées.

**Ce qu'il contrôle :**
- Numéro de série et type de licence
- Intégrité binaire (empreintes des exécutables)
- Validité de l'activation via le serveur

**Faiblesses :**
- Processus séparé : peut être arrêté ou bloqué
- Contrôles périodiques, pas continus
- Communication avec le serveur bloquable via le fichier hosts
- Vulnérable à la substitution de DLL

**Emplacement des données de licence :** `<user>/AppData/Roaming/Adobe/`

**Points de terminaison clés :**
- `lcs-cops.adobe.io` : Feature Restricted Licensing
- `lm.licenses.adobe.com` : validation de licence
- `activate.adobe.com` : activation

**Période de grâce hors ligne :**
- Abonnement annuel : 99 jours hors ligne
- Abonnement mensuel : 30 jours
- **Faiblesse critique :** une période de grâce de 99 jours signifie qu'une seule activation réussie permet à l'application de fonctionner hors ligne assez longtemps pour appliquer des correctifs permanents.

**Protection la plus efficace d'Adobe :** Firefly (fonctionnalités d'IA) s'exécute côté serveur. Il est impossible de pirater un calcul côté serveur. C'est l'enseignement architectural à retenir.

---

## Catégorie d'attaque 1 : remplacement de DLL {#attack-category-1-dll-replacement}

**Mécanisme :** remplacer `amtlib.dll` (la DLL de licence) par une version modifiée qui renvoie « licence valide » à toutes les requêtes.

**Chemin d'attaque AMTEmu (2013-2019) :**
1. Trouver `amtlib.dll` dans le répertoire de l'application
2. Le remplacer par une DLL corrigée
3. La DLL corrigée renvoie vrai à toutes les vérifications de licence
4. Résultat : activation permanente

**Pourquoi cela a fonctionné pendant des années :**
- Une seule DLL était responsable de toute la logique de licence
- Porte booléenne : la DLL renvoyait vrai ou faux, et renvoyer toujours vrai contournait tout
- Adobe n'a pas modifié l'architecture pendant des années

**Enseignement :** NE JAMAIS concentrer la logique de licence dans un seul module. Répartir les contrôles sur des dizaines d'emplacements. Vérifications en ligne, pas appels à une fonction « licence » séparée.

---

## Catégorie d'attaque 2 : modification du fichier hosts {#attack-category-2-hosts-file-modification}

```markdown
127.0.0.1 lcs-cops.adobe.io
127.0.0.1 lm.licenses.adobe.com
127.0.0.1 activate.adobe.com
127.0.0.1 genuine.adobe.com
# ... dozens more Adobe domains
```

Des dépôts GitHub maintiennent à jour des listes de blocage des domaines Adobe. Ils bloquent toute communication avec les serveurs.

**Enseignements :**
- Ne pas se fier uniquement aux noms DNS ; utiliser le certificate pinning
- Détecter la modification du fichier hosts (comparer la résolution DNS à une adresse IP connue)
- Utiliser un repli sur adresse IP en complément du DNS
- Utiliser une communication stéganographique (signal d'arrêt dans les en-têtes ou les poids transmis par CDN)
- Ne pas être trop agressif : les pare-feu d'entreprise affectent les utilisateurs légitimes

---

## Catégorie d'attaque 3 : patch binaire {#attack-category-3-binary-patching}

**Mécanisme :**
1. Désassembler le binaire (IDA Pro, Ghidra, OllyDbg)
2. Trouver le branchement conditionnel qui suit le contrôle de licence
3. Remplacer `JNZ` par `JMP` (inconditionnel) ou mettre l'appel en NOP

```asm
; Original
call license_check
test eax, eax
jnz  failure_path    ; jump if license invalid

; Patched
call license_check
test eax, eax
nop                  ; always falls through to success
nop
```

**Techniques :**
- Injection de NOP
- Inversion de branchement conditionnel
- Forçage du résultat de comparaison
- IAT hooking (substitution d'adresses dans la table d'imports, Import Address Table)

**GenP (2019 à aujourd'hui) :** patcheur AutoIt open source, maintenu par la communauté. Il recherche par motifs les séquences d'octets caractéristiques des contrôles de licence, à chaque mise à jour.

Pourquoi GenP continue de fonctionner malgré les mises à jour : la structure logique des contrôles de licence ne change pas fondamentalement. `if (license_valid) { run } else { block }` reste un seul bit. GenP trouve de nouveaux motifs pour chaque version.

**Problème fondamental de la « porte booléenne » :**
```c
if (isLicensed()) {
    enableFeatures();
}
```
Quelle que soit la complexité de `isLicensed()`, le résultat est un bit (vrai/faux). Une seule instruction corrigée contourne tout.

**Enseignement : la licence doit être une DONNÉE, pas un booléen :**
- La clé de licence contient les paramètres nécessaires au fonctionnement de l'algorithme
- Sans la bonne clé, l'algorithme produit des données inexploitables, et non un simple « blocage »
- Pas de `if (licensed)` unique à corriger
- Exemple : poids de modèle dérivés par HKDF ([[hkdf-personalized-weights]]), modèle chiffré ([[watermarking-encrypted-models]])

---

## Catégorie d'attaque 4 : faux serveur de licences local {#attack-category-4-fake-local-license-server}

**Mécanisme :** un serveur local imite les réponses du serveur Adobe. Le pirate intercepte les requêtes via le fichier hosts ou un proxy, et envoie de fausses réponses « licence valide ».

**Avantage par rapport au patch binaire :** il ne modifie aucun fichier sur le disque, ce qui le rend plus difficile à détecter.

**Enseignements :**
- Les réponses du serveur doivent être signées cryptographiquement (Ed25519)
- TLS mutuel
- La réponse doit contenir les DONNÉES nécessaires au calcul (pas seulement un « OK »)
- Même avec un faux serveur, l'attaquant ne peut pas forger un matériel de clé signé en Ed25519

---

## Catégorie d'attaque 5 : installeurs pré-patchés (repacks) {#attack-category-5-pre-patched-installers-repacks}

**Mécanisme :** installeurs modifiés, dont les correctifs sont déjà appliqués. Aucun Creative Cloud n'est nécessaire.

**Pourquoi c'est difficile à empêcher :** si l'application peut fonctionner de manière autonome, sans liaison avec un serveur, les repacks sont inévitables.

**Enseignements :** une architecture dépendant du serveur est la seule défense fiable contre les repacks. Si les fonctionnalités essentielles exigent une validation en temps réel qui renvoie du matériel cryptographique, les installeurs repackés sont inutilisables.

---

## Catégorie d'attaque 6 : exploitation de la période de grâce {#attack-category-6-grace-period-exploitation}

**Mécanisme :** activer légitimement, attendre la fin de la période de grâce, patcher le binaire, puis continuer à travailler indéfiniment (la licence mise en cache, valide hors ligne, reste utilisable après le patch).

**Enseignements pour les applications de ML hors ligne :**
- Le modèle est chiffré ; la clé de déchiffrement est une fonction de l'identifiant matériel, de la licence et des horodatages
- Sans vérification serveur, le modèle ne se déchiffre pas
- Même une licence en cache exige une re-dérivation périodique de la clé de chiffrement

---

## Défenses efficaces d'Adobe (à reprendre) {#adobes-effective-defenses-to-copy}

### Plusieurs points de vérification indépendants {#multiple-independent-verification-points}
AGS (service en arrière-plan) + contrôles dans l'application + contrôles de l'application de bureau Creative Cloud. Même si l'un est contourné, les autres continuent de fonctionner.

Pour les produits de ML : répartir les contrôles dans le code. Pas un seul `if (licensed)`, mais des dizaines de points de contrôle dans des modules différents.

### Restriction des fonctionnalités côté serveur {#server-side-feature-gating}
L'IA générative (Firefly) ne s'exécute QUE sur les serveurs d'Adobe. Il est impossible de pirater un calcul côté serveur. Elle génère des crédits génératifs, une comptabilité côté serveur qui ne peut pas être falsifiée.

Pour les produits de ML : le tout-serveur est idéal, mais pas toujours viable. Solution hybride : le matériel de déchiffrement des clés provient du serveur, et le modèle stocké est inutilisable sans lui.

### Mises à jour continues qui cassent les anciens cracks {#continuous-updates-breaking-old-cracks}
Chaque mise à jour peut casser les correctifs en circulation. Cela crée des fenêtres pendant lesquelles la version piratée ne fonctionne plus, et oblige les pirates à mettre leurs cracks à jour en permanence.

### Abonnement et fonctionnalités cloud comme valeur ajoutée {#subscription-cloud-features-as-value-add}
Le stockage cloud, les polices, les bibliothèques et la collaboration ne fonctionnent qu'avec un abonnement actif. Une version piratée équivaut à une version bridée. Le chiffre d'affaires est passé de 4,2 à 21,5 milliards de dollars (2011-2024). 37 millions d'abonnés à Creative Cloud.

### Réponse graduée plutôt que blocage total {#graduated-response-vs-hard-block}
Réponse d'Adobe à GenP 3.x : avertissements, dégradation des fonctionnalités, blocages ciblés. Pas de mise hors service de toutes les installations patchées, ce qui éloignerait les utilisateurs occasionnels.

---

## Défenses inefficaces d'Adobe (à éviter) {#adobes-ineffective-defenses-to-avoid}

### Une seule DLL pour toute la licence (amtlib.dll) {#single-dll-for-all-licensing-amtlibdll}
Un seul remplacement = contournement complet. Corrigé depuis, mais l'enseignement reste : ne jamais centraliser.

### Noms DNS prévisibles {#predictable-dns-names}
Bloquer 20 domaines dans le fichier hosts suffit. Utiliser le pinning, des canaux stéganographiques et un repli sur IP.

### Porte booléenne partout {#boolean-gate-everywhere}
Schéma : `if (isLicensed())` est toujours contournable par un NOP. Solution : la licence doit être un ingrédient de déchiffrement.

### Longue période de grâce hors ligne {#long-offline-grace-period}
99 jours de grâce = 99 jours pour que les pirates appliquent des correctifs permanents. Pour les produits de ML : re-dérivation périodique des clés à partir des données du serveur.

---

## Surface d'attaque des plugins Photoshop {#photoshop-plugin-attack-surface}

**Extensions CEP (obsolètes) :** la minification JavaScript n'offre aucune protection réelle. Le JavaScript minifié se désobfusque facilement.

**Plugins UXP :** le code est examiné par Adobe avant publication sur la place de marché, mais l'installation directe (`.ccx`) contourne cet examen.

**Vérification de licence des plugins :** généralement une requête HTTP vers le serveur de l'éditeur au démarrage (vérification d'environ 0,3 s). Facilement contournable en renvoyant un faux « OK » depuis un proxy local si la réponse n'est pas signée cryptographiquement.

**Enseignement pour les développeurs de plugins :** la signature des réponses est obligatoire. Si la réponse de licence ne contient que `{"valid": true}`, un faux serveur local l'imite trivialement.

---

## Stratégie de mise en application {#enforcement-strategy}

**BSA (Business Software Alliance) + Adobe :**
- Lettres de mise en demeure d'audit envoyées aux entreprises
- Déclaration d'auto-audit obligatoire
- Transactions : 100 000 $ et plus, typiquement, pour un usage commercial
- L'entreprise doit acheter les licences, détruire les copies non licenciées et accepter des audits futurs

**Stratégie de « tolérance au piratage » :**
- Les étudiants piratent → apprennent → trouvent un emploi → l'entreprise achète des licences d'entreprise
- Les utilisateurs individuels sont largement laissés tranquilles (ils restent dans l'écosystème)
- Le piratage commercial et d'entreprise est poursuivi avec vigueur
- Les redistributeurs font l'objet de retraits de contenus

**Chronologie :**
- Années 1990 : SafeDisc/SecuROM (cassés en une semaine environ)
- 2013 : lancement de l'abonnement CC ; les premiers cracks sont apparus 2 JOURS plus tard
- 2019 et après : AGS + fonctionnalités cloud restreintes
- 2022 : détection de motifs GenP dans CC 23.x
- 2024 et après : Neural Filters/Firefly déplacés côté serveur

---

## Comparaisons avec d'autres écosystèmes logiciels de création {#creative-software-ecosystem-comparisons}

### Autodesk (AutoCAD, Maya) {#autodesk-autocad-maya}
- Licences en ligne depuis 2017 (numéros de série hors ligne supprimés)
- Télémétrie intégrée : remontée automatique d'informations sur les installations, avec des identifiants uniques
- Base de données de numéros de série : saisir un numéro divulgué déclenche une invitation à un audit
- Le groupe de crackers MAGNiTUDE a piraté le Network Licensing Mechanism (NLM) et diffusé un NLM craqué, utilisé dans de nombreux repacks
- Enseignement : la télémétrie avec des identifiants d'installation uniques permet la détection, mais soulève des questions de vie privée

### Maxon (Cinema 4D) {#maxon-cinema-4d}
- Vérifie la signature de chaque fichier de projet, délivrée par la source officielle
- Une signature absente ou invalide bloque le fichier
- Enseignement : intégrer les informations de licence DANS les fichiers produits (tatouage des sorties) ; les fichiers traités portent l'identifiant de licence

### Foundry (Nuke) {#foundry-nuke}
- Licence flottante RLM (Reprise License Manager) liée à l'identifiant système du serveur
- Les serveurs RLM craqués imitent des réponses légitimes : attaque standard contre les licences flottantes
- Foundry est connue pour ses poursuites judiciaires agressives : menaces portant sur des dizaines de milliers de dollars
- Enseignement : le TLS mutuel et le certificate pinning protègent contre l'imitation par un faux serveur

### Topaz Photo AI {#topaz-photo-ai}
- Modèles stockés au format `.tz`/`.tz2`, téléchargés depuis `models-bal.topazlabs.com`
- **Échec critique :** les URL des modèles sont accessibles sans authentification ; environ 180 modèles (plus de 100 Go) ont été récupérés et publiés sur GitHub
- Modèles non chiffrés, utilisables directement
- Note : 2/10 pour la protection des modèles. Seule vraie défense : la dépendance aux mises à jour cloud, qui casse les versions craquées
- Sept. 2025 : passage à un abonnement uniquement (199 $/an en standard, 599 $/an en pro), suscitant une forte réaction des utilisateurs

### Retouch4me {#retouch4me}
- Clés liées au matériel (3 activations à l'achat)
- Versions autonomes avec modèles locaux : versions craquées trouvées sur des sites de torrents (modèles extraits avec succès)
- Version cloud (2024) : protection 8/10. L'inférence côté serveur ne peut pas être piratée
- Stratégie : la transition vers le cloud comme réponse au piratage

### Luminar Neo (Skylum) {#luminar-neo-skylum}
- Basé sur un compte, connexion internet obligatoire pour l'activation
- Le CLUF accorde explicitement le droit de « restreindre, suspendre ou résilier la licence à tout moment, sans compensation ni préavis »
- Massivement piraté : versions craquées sur des dizaines de sites, à des versions proches de l'actuelle

## Écosystème du piratage en Russie et dans la CEI {#russiancis-piracy-ecosystem}

**RuTracker.org :** 15,5 millions d'utilisateurs actifs, 2,59 millions de torrents, 6,2 pétaoctets. Bloqué en Russie, au Royaume-Uni, en Australie et ailleurs. Accessible via VPN.

**Schéma m0nkrus :** prend les installeurs officiels, applique les correctifs GenP et les empaquette en version autonome (sans CC, sans identifiant Adobe). Les nouvelles versions d'Adobe apparaissent en quelques jours ou semaines. Flux de travail automatisé.

Enseignements :
- Si l'application fonctionne de manière autonome, sans liaison avec un serveur, les repacks sont inévitables
- Un modèle CDN combiné à un blob d'activation par utilisateur empêche la distribution de repacks

## Pièges à éviter {#gotchas}

- **Le chiffre d'affaires a été multiplié par 5 malgré le piratage (ou grâce à lui).** La stratégie de « tolérance au piratage » d'Adobe est délibérée : une exposition gratuite auprès des étudiants crée de futurs clients payants. Tout piratage n'est pas une perte pure.
- **Même après les améliorations d'architecture, GenP continue de fonctionner.** Le détecteur de motifs maintenu par la communauté s'adapte aux nouveaux motifs binaires. Seules les fonctionnalités côté serveur sont réellement résistantes au piratage.
- **Une période de grâce nulle est incompatible avec l'expérience utilisateur.** 99 jours est excessif ; 7 à 30 jours représentent le bon équilibre entre l'expérience utilisateur (déplacements, problèmes réseau) et la sécurité.
- **La lutte anti-piratage agressive pénalise d'abord les utilisateurs légitimes.** Les pare-feu d'entreprise bloquent les remontées vers le serveur, ce qui génère des tickets de support. Concevoir une dégradation progressive plutôt que des blocages stricts en cas de défaillance réseau.
- **La signature des réponses est non négociable.** L'attaque par faux serveur (catégorie 4) rend inutiles toutes les réponses serveur non signées. La vérification Ed25519 doit faire partie de toute vérification de licence impliquant une communication avec le serveur.
- **Le code source de GenP a été publié en 2023.** La communauté open source continue de maintenir des forks. La « sécurité par l'obscurité » des motifs binaires a une durée de vie limitée ; la défense architecturale (licence = donnée) est durable.
- **Fuite des URL de modèles Topaz :** un CDN non protégé équivaut à une extraction complète des modèles, sans aucun contournement de licence. Il faut chiffrer les modèles ET authentifier les requêtes de téléchargement : les deux sont nécessaires.
- **Les applications « autonomes d'abord » seront craquées.** La version autonome de Retouch4me a été craquée malgré la liaison matérielle ; la version cloud a survécu. Pour les applications de ML avec inférence sur l'appareil, la défense en profondeur doit aller au-delà des seuls contrôles de licence.
