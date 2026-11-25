---
level: 3
source_sha256: 52390eba927f492b92d335caa98d1c1ff9e48220c2d2cb1af8220f50a52e6e1d
translation: machine
translated_at: '2026-10-24'
---
# RunPod Flash GPU Serverless {#runpod-flash-gpu-serverless}

RunPod Flash est un SDK Python open source (licence MIT, v1.16.0) qui permet de déployer des fonctions serverless accélérées par GPU via une interface basée sur des décorateurs. Il automatise le provisionnement des workers, la configuration de l'environnement et la gestion des dépendances, ce qui évite de créer manuellement des Dockerfiles et de maintenir un registre de conteneurs.

## Architecture de base et implémentation {#core-architecture-and-implementation}
Les fonctions Flash sont définies à l'aide du décorateur `@Endpoint`, qui spécifie les exigences matérielles et les dépendances logicielles. Le SDK prend en charge le processus de build multiplateforme, ce qui permet aux développeurs sous macOS (puces M) ou Linux de cibler des environnements GPU distants x86_64.

### Définition de la fonction serverless {#serverless-function-definition}
```python
from runpod_flash import Endpoint, GpuType

@Endpoint(
    name="tensor-processor",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(0, 10), # scale-to-zero to 10 max workers
    dependencies=["torch>=2.4.0", "numpy", "pillow"]
)
async def process_data(payload):
    # Logic executes on remote RunPod Serverless infrastructure
    import torch
    return {"device": str(torch.cuda.get_device_name(0))}
```

### Flux de déploiement {#deployment-workflow}
La CLI gère l'authentification et le cycle de vie des endpoints :
```bash
pip install runpod-flash
flash login   # OAuth browser flow
flash deploy  # Provisions infrastructure and uploads code
```

## Gestion des ressources et sélection du matériel {#resource-management-and-hardware-selection}
Le SDK utilise des énumérations typées pour un ciblage matériel précis et des configurations de mise à l'échelle flexibles.

- **Types de GPU :** sélection via `GpuType` pour des modèles spécifiques (par exemple, `NVIDIA_A100_80GB_PCIe`, `NVIDIA_GEFORCE_RTX_4090`).
- **Groupes de GPU :** utilisation de `GpuGroup` (par exemple, `GpuGroup.AMPERE_80`, `GpuGroup.ANY`) pour permettre au provisionneur de sélectionner le premier nœud compatible disponible.
- **Mise à l'échelle des workers :** le paramètre `workers=(min, max)` active la logique de mise à l'échelle à zéro afin d'éliminer les coûts liés aux workers inactifs.
- **Stockage :** l'intégration de `NetworkVolume` fournit un stockage persistant, accessible entre centres de données, pour les poids de modèles ou les jeux de données.
- **Variables d'environnement :** Flash exclut les valeurs des variables d'environnement du hachage de configuration, afin que la rotation des secrets ou les modifications de configuration ne déclenchent pas la reconstruction de l'image.

## Modèles de déploiement {#deployment-patterns}
1. **Basé sur une file d'attente (asynchrone) :** modèle standard pour les traitements par lots déclenchés via l'API asynchrone du SDK.
2. **API à répartition de charge :** routes accessibles en HTTP qui partagent un pool commun de workers mis à l'échelle.
3. **Orchestration Docker personnalisée :** intégration d'images préconstruites existantes (par exemple, vLLM, TensorRT-LLM, ComfyUI) dans la couche d'orchestration Flash.
4. **Mode développement :** provisionnement éphémère de workers via `flash dev --auto-provision` pour le débogage local contre des ressources GPU distantes.

## Contraintes opérationnelles {#operational-constraints}
- **Limites de paquet :** la taille totale du déploiement (code + dépendances locales) est plafonnée à 500 Mo.
- **Support d'exécution :** limité à Python 3.10, 3.11 et 3.12.
- **Démarrages à froid :** les piles de dépendances lourdes (par exemple, `torch` + `diffusers`) peuvent entraîner des démarrages à froid durant plusieurs minutes.
- **Prérequis système :** la CLI de développement local nécessite macOS ou Linux ; Windows n'est pris en charge que via WSL2.

## Pièges courants {#gotchas}
- **Problème :** la surcharge liée aux dépendances volumineuses dépasse la limite de déploiement de 500 Mo ou ralentit les démarrages à froid. → **Solution :** déplacer les ressources statiques volumineuses et les poids de modèles vers un `NetworkVolume` et le monter sur le worker, au lieu de les intégrer au paquet de déploiement.
- **Problème :** les installations pip standard dans le décorateur échouent pour les paquets privés ou complexes. → **Solution :** utiliser le modèle `Custom Docker` (modèle 3) pour fournir un environnement préconstruit tout en utilisant Flash pour l'orchestration.
- **Problème :** l'exécution locale sous Windows empêche l'initialisation de la CLI Flash. → **Solution :** utiliser un conteneur de développement basé sur Linux ou WSL2, car le shell Windows natif n'est pas pris en charge pour les builds locaux.

## Voir aussi {#see-also}
- [[runpod-production]]
- [[docker-for-ml]]
- [[deployment-strategies]]
- [[kubernetes-resource-management]]
