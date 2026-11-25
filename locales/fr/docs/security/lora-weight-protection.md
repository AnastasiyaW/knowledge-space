---
level: 3
source_sha256: b56a3b7484b2b1b0c1a8c77ce6be8762ff7745ee0000db3c94605b10f7d7e97a
translation: machine
translated_at: '2026-10-24'
---
# Protection des poids LoRA : filigrane, attaques par extraction et licences {#lora-weight-protection-watermarking-extraction-attacks-and-licensing}

Date : 2026-04-03
Contexte : génération d'images sur poste de travail et serveur, avec adaptateurs LoRA propriétaires sur des modèles de base open source (FLUX, SD). Couvre la protection des poids des adaptateurs contre le vol, la preuve forensique de la propriété et la défense contre les attaques par extraction.

---

## Modèle de menace {#threat-model}

Les adaptateurs LoRA (delta_W = B × A, stockés en `.safetensors`, 10 à 200 Mo) présentent quatre vulnérabilités inhérentes :

1. **Portabilité** : un seul fichier, qui fonctionne avec toute copie du même modèle de base
2. **Format compact** : partage trivial par e-mail, clé USB ou stockage cloud
3. **Extractibilité** : si le modèle de base est public, delta_W peut être récupéré : `delta_W = merged_model - base_model`
4. **Extraction par requêtes** : même un accès uniquement via API permet des attaques par distillation

---

## Filigranage spécifique aux LoRA {#lora-specific-watermarking-methods}

### SEAL (filigranes white-box entrelacés) {#seal-entangled-white-box-watermarks}

**Article :** arxiv:2501.09284 (janv. 2025)

Insère une matrice secrète non entraînable entre les matrices de poids LoRA entraînables pendant l'entraînement. Le filigrane est « entrelacé » avec les poids entraînés : l'extraction du filigrane SEAL nécessite de résoudre un problème d'optimisation conjoint.

**Propriétés :**
- Aucune dégradation de la qualité pour la génération texte-image ou le réglage par instructions
- Résistant aux attaques de suppression, d'obfuscation et d'ambiguïté
- La vérification est white-box (nécessite un accès au modèle)

**Intégration à l'entraînement :**
```python
# Pseudo-code: SEAL inserts a fixed passport matrix P
# between LoRA A and B matrices during forward pass
def forward(x, A, B, P, alpha):
    # Standard LoRA: output = x + alpha * (B @ A @ x)
    # SEAL: output = x + alpha * (B @ P @ A @ x)
    # P is non-trainable, randomly initialized at training start
    return x + alpha * (B @ P @ A @ x)
```

### AquaLoRA (white-box, spécifique à SD) {#aqualora-white-box-sd-specific}

**Article :** arxiv:2405.11135 (ICML 2024) | [GitHub](https://github.com/Georgefwt/AquaLoRA)

Deux étapes : (1) pré-entraînement d'un encodeur/décodeur de filigrane dans l'espace latent ; (2) intégration du filigrane dans l'U-Net de SD via LoRA pendant le réglage fin.

- **Capacité :** 48 bits par modèle
- **Matrice de mise à l'échelle :** permet de modifier la charge utile du filigrane sans réentraînement complet
- Résistant à la fusion LoRA et aux tentatives de suppression

### LoRAGuard (black-box, méthode Yin-Yang) {#loraguard-black-box-yin-yang-method}

**Article :** arxiv:2501.15478 (janv. 2025)

Détecte la propriété sans accéder aux poids internes :
- **Yin** (chemin à poids négatifs) : détectable par une opération de négation sur les sorties du modèle
- **Yang** (chemin à poids positifs) : détectable par une opération d'addition

Résout le problème majeur des filigranes antérieurs, qui cèdent lors de la combinaison de LoRA (fusion de plusieurs adaptateurs) ou de la négation. Taux de réussite de la vérification proche de 100 %.

### AuthenLoRA (filigrane propagé dans les sorties) {#authenlora-output-propagating-watermark}

**Article :** arxiv:2511.21216 (nov. 2025) | [GitHub](https://github.com/ShiFangming0823/AuthenLoRA)

Le filigrane se propage dans chaque image générée, et pas seulement dans les poids :
- Optimisation à double objectif : entraînement conjoint du transfert de style et de l'insertion du filigrane
- Un mapper léger permet de modifier la charge utile du filigrane sans réentraînement complet
- La détection s'effectue sur les images produites, ce qui reste utile même si les poids sont volés

### Tableau comparatif {#comparison-table}

| Méthode | Année | Accès | Résiste à la fusion | Résiste à la quantification | Capacité |
|---------|-------|-------|---------------------|-----------------------------|----------|
| AquaLoRA | 2024 | Blanche | Oui | Partiel | 48 bits |
| SEAL | 2025 | Blanche | Oui | Oui | Intégré |
| LoRAGuard | 2025 | Noire | Oui | Oui | Binaire |
| AuthenLoRA | 2025 | Sortie | N/A (par image) | N/A | Par image |
| MOLM | 2024 | Routage | Oui | Oui | >0,98 de précision |

**Recommandation pour la production :** SEAL pour la preuve de propriété au niveau des poids, combiné à AuthenLoRA ou à un filigranage standard des sorties pour la criminalistique au niveau des images. Combinez les deux : prouvez que vous possédez les poids ET que des images précises proviennent de votre modèle.

---

## Attaques par extraction {#extraction-attacks}

### StolenLoRA (distillation par requêtes) {#stolenlora-query-based-distillation}

**Article :** arxiv:2509.23594 (ICCV 2025)

Attaque qui reconstruit la fonctionnalité d'un LoRA à l'aide de requêtes synthétiques :

- **Méthode :** l'attaquant génère des données synthétiques via un LLM et un modèle de diffusion, interroge l'API cible, puis entraîne un LoRA élève à partir des réponses en utilisant l'apprentissage semi-supervisé fondé sur le désaccord (DSL, Disagreement-based Semi-supervised Learning)
- **Coût :** environ 10 000 requêtes, réalisables en une seule journée par un seul utilisateur
- **Taux de réussite :** réplication fonctionnelle à 96,6 %
- **Inter-backbone :** fonctionne même lorsque l'attaquant utilise un modèle de base différent de celui de la victime

**Conséquence :** la protection par API seule (ne jamais livrer les poids) n'est PAS suffisante. 10 000 requêtes provenant d'un seul utilisateur suffisent à reconstruire votre LoRA.

### Fusion puis soustraction (extraction des poids à partir du modèle fusionné) {#merge-and-subtract-weight-extraction-from-merged-model}

Si le modèle de base est public (FLUX, SD) :
```python
# Attacker recovers delta_W exactly
import torch
merged = load_state_dict("your_product_model.safetensors")
base = load_state_dict("FLUX.1-dev.safetensors")  # public
delta_W = {k: merged[k] - base[k] for k in merged}
# delta_W ≈ your LoRA (full-rank, functionally equivalent)
```

`unfuse_lora()` dans Diffusers utilise exactement ce même calcul. Fusionner avec un modèle de base open source n'offre **aucune protection** si l'attaquant connaît le modèle de base (ce qui est le cas, puisqu'il est public).

**Atténuations partielles (efficacité moindre) :**
- Quantification INT4/INT8 après fusion (dégrade la précision de la reconstruction)
- Réglage fin sur du bruit pendant quelques étapes après fusion (brouille la frontière du delta)
- Fusion de plusieurs LoRA (plus difficile d'isoler un seul)

**Efficacité de la fusion comme protection : 2/10**

### Inférence d'appartenance sur LoRA {#membership-inference-on-lora}

**Article :** arxiv:2507.18302 (juil. 2025)

Les attaques par inférence d'appartenance (MIA, Membership Inference Attacks) permettent de déterminer si des images précises faisaient partie du jeu d'entraînement en interrogeant le LoRA. Pertinent pour le secret industriel et la conformité au RGPD : l'appartenance aux données d'entraînement peut être inférée à partir du comportement du modèle.

---

## Stratégies de défense {#defense-strategies}

### Contre l'extraction par requêtes (StolenLoRA) {#against-query-based-extraction-stolenlora}

```python
# Server-side: detect extraction patterns
def detect_extraction_query(user_id: str, request: dict) -> float:
    """Returns extraction suspicion score 0-100"""
    history = get_request_history(user_id, hours=24)
    
    score = 0
    # High volume from single user
    if len(history) > 500: score += 30
    if len(history) > 2000: score += 50
    
    # Uniform/grid-like inputs (systematic sampling)
    if _is_systematic_sampling(history): score += 40
    
    # Inputs similar to known synthetic datasets
    if _resembles_synthetic_grid(request): score += 20
    
    return min(score, 100)
```

**Contre-mesures :**
- Limitation du débit par licence (plafond souple de 50 à 100 inférences par jour, plafond strict de 500 par jour)
- Perturbation des sorties : ajout d'un bruit minimal invisible qui dégrade l'entraînement de l'élève sans affecter la qualité perçue par l'utilisateur
- Empreinte API : intégration d'un filigrane propre à chaque utilisateur dans toutes les sorties de l'API (dans le style d'AuthenLoRA)
- Détection d'anomalies dans les schémas de requêtes (entrées systématiques = échantillonnage en grille = extraction)

### Contre le vidage mémoire des poids déchiffrés {#against-memory-dump-of-decrypted-weights}

Une fois les poids déchiffrés pour l'inférence, ils existent en RAM. Atténuation :

- Utiliser `VirtualLock()` (Windows) / `mlock()` (macOS/Linux) sur les tampons de poids afin d'empêcher leur écriture sur disque par la pagination
- Effacer les tampons de poids immédiatement après la fin de la session (`sodium_memzero()`)
- Motif CORELOCKER : servir les tenseurs critiques depuis le serveur, sans jamais les stocker localement

```cpp
// Lock weight buffer in RAM, prevent swap to pagefile
VirtualLock(tensor_buffer, tensor_size);
// ... run inference ...
sodium_memzero(tensor_buffer, tensor_size);
VirtualUnlock(tensor_buffer, tensor_size);
```

---

## Chiffrement à l'exécution dans ComfyUI (ComfyUI-LMCQ) {#comfyui-runtime-encryption-comfyui-lmcq}

**GitHub :** [github.com/sebord/ComfyUI-LMCQ](https://github.com/sebord/ComfyUI-LMCQ)

Chiffrement pratique lié au matériel pour les déploiements ComfyUI :

**Génération du code machine :**
```text
GPU ID + CPU serial + MAC address + disk serial + motherboard ID
-> HMAC-SHA256 -> machine_code
```

**Flux de travail :**
1. Générer le `machine_code` sur la machine cible
2. Chiffrer le fichier LoRA en le liant à la liste des `machine_code` autorisés
3. Le nœud de déchiffrement à l'exécution vérifie le `machine_code` avant le chargement
4. Le modèle ne réside qu'en mémoire : aucun fichier déchiffré n'est écrit sur disque

**Limites :**
- L'usurpation matérielle contourne la liaison à la machine
- Les VM ont des identifiants matériels instables (cela casse lors de la restauration d'un instantané)
- Les instances GPU cloud changent d'identifiants matériels au remplacement de l'instance
- Une fois déchiffrés, les poids sont en RAM : un vidage mémoire reste possible

---

## Contraintes de licence FLUX {#flux-license-constraints}

| Modèle | Licence | Usage commercial |
|--------|---------|------------------|
| FLUX.1 [dev] | Non commerciale v2.0 | Non autorisé sans accord avec BFL |
| FLUX.2 Klein 4B | Apache 2.0 | Entièrement autorisé |
| FLUX.2 Klein 9B | Non commerciale | Nécessite une licence commerciale BFL |
| Stable Diffusion 1.5/SDXL | CreativeML Open RAIL-M | Autorisé avec restrictions d'usage |

**Les dérivés LoRA héritent des restrictions d'usage** de la licence du modèle de base, mais n'ont PAS à être publiés en open source. Un LoRA entraîné sur FLUX.1 [dev] ne peut pas être utilisé commercialement sans licence BFL, que vous possédiez ou non le LoRA.

Pour les applications de retouche en production : utilisez Klein 4B (Apache 2.0, sans restriction) ou obtenez une licence commerciale BFL pour Klein 9B.

---

## Empreintes pour la preuve juridique de propriété {#fingerprinting-for-legal-ownership-proof}

### Chain & Hash (arxiv:2407.10887) {#chain-hash-arxiv240710887}

Lie cryptographiquement des prompts d'empreinte aux réponses. Le propriétaire conserve des paires (prompt, réponse_attendue) : elles démontrent que la sortie n'est déterministe que pour leur modèle. Sert de preuve de propriété en cas de litige.

### Cadre LoRA-FP (arxiv:2509.00820) {#lora-fp-framework-arxiv250900820}

Intégration d'empreinte « plug-and-play » par réglage fin contraint :
- L'empreinte se transmet aux modèles dérivés par fusion de paramètres
- Coût de calcul inférieur aux approches portant sur l'ensemble des paramètres
- Survit au réglage fin incrémental

### RoFL (arxiv:2505.12682) {#rofl-arxiv250512682}

Empreinte par motifs statistiques des sorties :
- Résistant au réglage fin, à l'élagage et à la quantification
- Utilise des engagements cryptographiques (hachage publié avant le déploiement = pré-enregistrement)
- Fournit des preuves recevables devant un tribunal : « Nous avons enregistré l'empreinte X avant l'apparition de votre modèle »

---

## Pièges {#gotchas}

- **La fusion puis soustraction annule toute chiffrement des poids si le modèle de base est public.** Chiffrer le fichier du modèle fusionné est inutile si le modèle de base est librement disponible et que l'attaquant sait lequel a été utilisé. Protégez uniquement les fichiers LoRA autonomes ou utilisez un modèle de base privé.
- **StolenLoRA fait de « API seule » une fausse sécurité.** 10 000 requêtes en une journée constituent un usage normal pour un photographe professionnel. La limitation de débit doit être combinée à une détection comportementale (schémas d'échantillonnage en grille, caractéristiques uniformes des images), et non se limiter à un simple compteur de requêtes.
- **Le chiffrement homomorphe (FHE) pour l'inférence est environ 1000 fois plus lent.** PrivTuner et des articles similaires montrent qu'une inférence FHE sur LoRA est théoriquement possible, mais inadaptée à la génération interactive d'images, car trop lente de plusieurs ordres de grandeur. Non viable en 2026.
- **Un filigrane AuthenLoRA dans les sorties peut être sondé par les attaquants.** Si l'attaquant peut détecter si sa copie extraite produit le même motif de filigrane, il peut vérifier que son extraction a réussi. Conservez le décodeur de filigrane uniquement côté serveur.
- **Le format `.ckpt`/`.pt` de ComfyUI permet l'exécution de code arbitraire via pickle.** Utilisez toujours `.safetensors` pour la distribution et le chargement des LoRA. `.safetensors` a fait l'objet d'un audit de sécurité ; pickle, non.
- **La méthode Yin-Yang de LoRAGuard exige une configuration d'inférence spécifique.** La détection nécessite d'exécuter le modèle avec des opérations de négation ou d'addition qui ne font pas partie de l'inférence normale. Si vous ne conservez pas le protocole de vérification, vous perdez la capacité de prouver la propriété ultérieurement.

## Voir aussi {#see-also}
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[model-weight-encryption]]
- [[output-scrambling-antipiracy]]
- [[anti-piracy-legal]]
