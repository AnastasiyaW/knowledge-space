---
level: 3
source_sha256: 232647fc555ee120803bc81f920355994d1b3880a848943c33850ae9ce7611f7
translation: machine
translated_at: '2026-10-24'
---
# Bonnes pratiques de production sur RunPod {#runpod-production-patterns}

Référence pour le déploiement de charges de travail GPU sur RunPod : choix du type de déploiement, stratégie d'images en trois niveaux, architecture des workers serverless, gestion des secrets et modes de défaillance courants.

## Choix du type de déploiement {#deploy-type-selection}

| Cas d'usage | Type de déploiement | Facturation |
|----------|------------|---------|
| Entraînement / fine-tuning (heures/jours) | **Pod** | À l'heure, inactivité incluse |
| Débogage, ComfyUI interactif | **Pod** | À l'heure, inactivité incluse |
| API d'inférence en production | **Serverless** | À la seconde, uniquement en activité |
| Trafic irrégulier (pics + périodes creuses) | **Serverless** | 60 à 70 % d'économies par rapport à une instance permanente |
| Hybride : front serverless + tâches longues | **Instant Clusters** | Mixte |

**Règle de décision :** charge constante → Pod. Trafic irrégulier ou endpoint d'API → Serverless.

## Stratégie d'images (3 niveaux) {#image-strategy-3-tiers}

### Niveau 1 — Mis en cache par RunPod (téléchargement de 10 à 60 s) {#tier-1-runpod-cached-10-60-sec-pull}
```text
runpod/pytorch:2.11.0-cuda13.0-cudnn9-devel
runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
runpod/worker-comfyui:<version>-base
runpod/worker-comfyui:<version>-flux1-dev
runpod/base:0.6.x-cuda...
```
Mis en cache sur les nœuds Secure Cloud. Non garanti sur le Community Cloud.

### Niveau 2 — Images Docker Hub populaires (téléchargement de 1 à 5 min) {#tier-2-popular-docker-hub-1-5-min-pull}
```text
pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel
nvidia/cuda:*  (sometimes cached, sometimes not)
```

### Niveau 3 — Images personnalisées (3 à 10 min, ou blocage) {#tier-3-custom-images-3-10-min-or-stuck}
```text
ghcr.io/your-org/your-image:tag
nvidia/cuda:13.0.0-devel-ubuntu22.04  ← confirmed stuck on 4/4 pods (2026-04-17)
```

**Règle :** toujours essayer le niveau 1 en premier. Si la version de CUDA/PyTorch correspond à une image du niveau 1, utilisez-la.  
Les images personnalisées (niveau 3) doivent être publiées sur `ghcr.io` en tant que surcouche d'une image de base du niveau 2, et non directement à partir de `nvidia/cuda`.

## FlashBoot {#flashboot}

Optimisation gratuite des démarrages à froid, activée par défaut.

- 48 % des démarrages à froid se terminent en moins de 200 ms
- Cas typique : démarrage à froid de 1 à 2 s
- ComfyUI : démarrages à froid 50 à 80 % plus rapides avec FlashBoot
- Mécanisme : des appels plus fréquents permettent à RunPod de garder les workers « chauds » sur l'hôte

**Un nombre de workers actifs ≥ 1** réduit le démarrage à froid à environ 0 ms (au prix d'une instance permanente).

## Network Volumes (stockage des modèles) {#network-volumes-model-storage}

```bash
# Create volume in RunPod Console → pick region closest to traffic source
# Mount volume in pod/worker:
# /opt/ComfyUI/models → Network Volume path

# Pre-load models via cheap CPU pod:
rsync -av ./models/ /workspace/models/
# Or: aws s3 sync s3://your-bucket/models /workspace/models/
```

**Tarification :** 0,07 $/Go/mois pour le premier To, 0,05 $/Go au-delà.  
**Quand l'utiliser :** modèles de plus de 10 Go, mis à jour fréquemment, partagés entre plusieurs pods.  
**Modèles intégrés à l'image :** uniquement pour les modèles stables de 10 Go ou moins qui changent rarement.

## Modèle worker-comfyui {#worker-comfyui-pattern}

Modèle serverless officiel (`github.com/runpod-workers/worker-comfyui`).

### Format de requête {#request-format}

```json
{
  "input": {
    "workflow": {},
    "images": [{"name": "input.png", "image": "<base64>"}],
    "api_key_override": ""
  },
  "webhook": "https://your-endpoint/callback"
}
```

### Format de réponse (v5.0.0 et ultérieures) {#response-format-v500}

```json
{
  "output": {
    "images": [
      {"filename": "out.png", "type": "base64", "data": "..."}
    ],
    "errors": []
  }
}
```

### Endpoints {#endpoints}
- `/run` — asynchrone, charge utile jusqu'à 10 Mo
- `/runsync` — synchrone, charge utile jusqu'à 20 Mo
- `/health` — vérification de l'état

### Accès SSH pour le débogage {#ssh-debug-access}
```bash
# Set env var in pod template:
PUBLIC_KEY=<your-ssh-public-key>
# Opens port 22 for SSH access into worker
```

## Gestion des secrets {#secrets-management}

```bash
# In RunPod Console → Account → Secrets → create named secret
# Reference in template env vars:
RUNPOD_SECRET_WASABI_ACCESS_KEY=my-wasabi-key-name
RUNPOD_SECRET_WASABI_SECRET_KEY=my-wasabi-secret-name
# Runtime substitutes encrypted value → plain env var inside container
```

**Clés d'API limitées (2026) :** créez des clés par endpoint avec suivi de l'utilisation. Appliquez le principe du moindre privilège.

## Matrice de sélection des GPU {#gpu-selection-matrix}

| GPU | Architecture | flash-attn2 | flash-attn3 | Remarques |
|-----|-------------|-------------|-------------|-------|
| A100 | sm_80 | Oui | Non | Standard, largement disponible |
| H100 | sm_90 | Oui | Oui (+30 à 50 % par rapport à FA2) | Idéal pour HF/entraînement |
| H200 | sm_90 | Oui | Oui | Dernière génération, disponibilité limitée |
| A40 | sm_86 | Oui | Non | Entraînement économique |
| RTX 4090 | sm_89 | Oui | Non (sm_89 < sm_90) | Grand public, peu coûteux |

**Choix du runtime Flash Attention :**
```python
import torch
cap = torch.cuda.get_device_capability()
if cap[0] >= 9:
    # H100, H200 → FA3 via HF Kernels
    from kernels import get_kernel
    fa = get_kernel("kernels-community/vllm-flash-attn3",
                    arch=f"sm_{cap[0]}{cap[1]}")
else:
    # A100 → FA2
    fa = get_kernel("kernels-community/flash-attn2",
                    arch=f"sm_{cap[0]}{cap[1]}")
```

## Modèle CI/CD {#cicd-pattern}

```yaml
# .github/workflows/deploy.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/org/image:${{ github.sha }},ghcr.io/org/image:latest
    cache-from: type=registry,ref=ghcr.io/org/image:buildcache
    cache-to: type=registry,ref=ghcr.io/org/image:buildcache,mode=max
```

**Tags immuables :** `:sha` ne change jamais. `:latest` est uniquement un pointeur mobile.

## 8 pièges courants {#8-common-pitfalls}

| Symptôme | Cause racine | Correction |
|---------|-----------|-----|
| Téléchargement d'image bloqué indéfiniment | Image de niveau 3 non mise en cache par RunPod, limitation de débit de Docker Hub | Utiliser les niveaux 1/2 ; publier l'image personnalisée sur ghcr.io en tant que surcouche |
| Incompatibilité CUDA à l'exécution | CUDA de l'image de base ≠ CUDA de PyTorch installé | Faire correspondre exactement : les wheels `cu130` nécessitent une base CUDA 13.0 |
| Mise à l'échelle GPU bloquée à 0 worker | Échec de la vérification d'état du worker | Vérifier `PUBLIC_KEY` pour l'accès SSH de débogage ; tester l'endpoint `/health` |
| Dépassement mémoire (OOM) sur les grands modèles | Modèle chargé à chaque requête au lieu d'une seule fois | Charger le modèle dans l'initialisation de `handler.py`, et non dans la fonction `handler()` |
| Coût des pods inactifs qui s'accumule | Pod laissé en marche après la session | Utiliser Serverless en production ; activer l'arrêt sur inactivité pour les pods de développement |
| Secrets inaccessibles | Référence au nom de variable d'environnement brut au lieu de `RUNPOD_SECRET_*` | Utiliser le préfixe `RUNPOD_SECRET_<nom-du-secret>` dans le template |
| Pods du Community Cloud bloqués | Téléchargement d'image peu fiable sur les nœuds communautaires | Utiliser Secure Cloud pour les images de niveau 3 |
| Incompatibilité des GPU Blackwell | Wheels sm_100 pas encore disponibles | Vérifier la compatibilité des wheels ; utiliser A100/H100 en attendant la prise en charge |

## Points d'attention {#gotchas}

- **Problème :** l'image `nvidia/cuda:13.0.0-devel-ubuntu22.04` utilisée directement comme image de pod → blocage sur 4 pods consécutifs sur A5000/A40/L40S. → **Correction :** utiliser `pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel` comme base (même CUDA 13, même PyTorch 2.11, correctement mise en cache). Ne jamais utiliser les images `nvidia/cuda` brutes comme cibles directes sur RunPod.
- **Problème :** modèle téléchargé sur le disque local du conteneur → perdu à la fin du pod. → **Correction :** toujours utiliser des Network Volumes pour les modèles de plus de 1 Go. Monter le volume sur `/workspace/models`. Utiliser un fichier sentinelle `.models_provisioned` pour éviter un nouveau téléchargement au redémarrage.
- **Problème :** le worker serverless charge un modèle volumineux dans la fonction `handler()` → démarrage à froid de 30 secondes à chaque requête. → **Correction :** charger le modèle au niveau du module (en dehors du handler) : `model = load_model()`, exécuté une seule fois à l'initialisation du worker.
- **Problème :** les sessions `--resume` / `--continue` dont l'historique contient des chaînes liées à la facturation déclenchent un bogue d'invalidation de cache (v2.1.100), multipliant le coût en tokens par 10 à 20. → **Correction :** éviter `--resume` tant que la correction du bogue n'est pas confirmée ; démarrer des sessions neuves pour les workflows longs.

## Voir aussi {#see-also}

- [[docker-for-ml]]
- [[container-registries]]
- [[dockerfile-and-image-building]]
- [[cicd-pipelines]]
