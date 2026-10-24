---
title: "Compression du cache KV et contrôle de la mémoire"
description: "Mesurer, sélectionner et valider les stratégies de cache KV pour l'inférence des LLM, sans se fier aux idées reçues issues des benchmarks."
tags: [llm-agents, kv-cache, inference, memory-optimization, long-context, serving]
level: 5
source_sha256: 523aded393e40949109d66a23d56108db76c45c74da097692bbc3cd32d0dc914
translation: machine
translated_at: '2026-10-24'
---
# Compression du cache KV et contrôle de la mémoire (septembre 2026) {#kv-cache-compression-and-memory-control-september-2026}

Contexte de version : les formats de cache et les stratégies prises en charge dépendent de l'architecture du modèle, du framework, du backend, de la précision et du moteur de service. Consultez la documentation et la télémétrie pour la combinaison exacte déployée. Cette page évite les taux de compression universels et les affirmations de performance.

Un cache clé-valeur (KV) stocke les clés et valeurs d'attention déjà calculées pour les tokens précédents, afin que le décodage autorégressif n'ait pas à les recalculer à chaque étape de génération. Il améliore l'efficacité du décodage, mais la mémoire occupée par le cache peut devenir la ressource limitante pour les contextes longs ou les requêtes concurrentes.

## Ce qui détermine la taille du cache {#what-determines-cache-size}

Pour un modèle decoder-only à attention conventionnelle, une estimation de planification est :

```text
bytes ≈ 2 × layers × batch_size × retained_tokens
        × num_kv_heads × head_dim × bytes_per_element
```

Le facteur deux représente les clés et les valeurs. L'attention à requêtes groupées (grouped-query) ou multi-requêtes (multi-query) peut utiliser moins de têtes clé/valeur que de têtes de requête ; utilisez donc le nombre réel de têtes KV du modèle. Les implémentations de cache propres aux architectures encodeur-décodeur, à fenêtre glissante, à attention linéaire ou à un modèle particulier peuvent adopter une disposition différente.

```python
def estimate_kv_cache_bytes(
    *,
    num_layers: int,
    batch_size: int,
    retained_tokens: int,
    num_kv_heads: int,
    head_dim: int,
    bytes_per_element: int,
) -> int:
    return (
        2
        * num_layers
        * batch_size
        * retained_tokens
        * num_kv_heads
        * head_dim
        * bytes_per_element
    )
```

Considérez ce calcul comme une planification de capacité, et non comme un reçu d'allocation. Le surcoût du framework, les noyaux d'attention, la fragmentation, la réutilisation des préfixes, la capture de graphe et le parallélisme consomment également de la mémoire.

## Diagnostiquer avant de compresser {#diagnose-before-compressing}

Collectez un profil de charge avant de choisir une stratégie :

| Signal | Pourquoi il compte |
|---|---|
| Distributions des tokens d'entrée et générés | Détermine la longueur de séquence conservée |
| Séquences actives simultanées | Multiplie l'allocation du cache |
| Latence de préremplissage (prefill) versus décodage | Sépare les goulots d'étranglement du prompt et de la génération de tokens |
| Taux de réutilisation / de succès du cache | Indique si les préfixes communs sont utiles |
| Mémoire GPU, OOM, fragmentation | Détermine si la mémoire est la vraie contrainte |
| Qualité à la longueur de contexte cible | Détecte les régressions sur les contextes longs |
| Périmètre tenant/données | Empêche une réutilisation dangereuse du cache |

Ne réglez pas un cache sur un prompt synthétique court puis ne le déployez pas sur une charge de documents longs ou multi-utilisateurs.

## Choisir une stratégie de cache selon la contrainte {#choose-a-cache-strategy-by-constraint}

| Stratégie | Idéale quand | Compromis |
|---|---|---|
| Cache dynamique | Les longueurs de séquence varient et la simplicité compte | Croissance des allocations et formes moins prévisibles |
| Cache statique / préalloué | La longueur maximale est connue et le framework le prend en charge | La mémoire réservée peut être gaspillée ou provoquer un OOM |
| Cache à fenêtre glissante | Le modèle et la tâche tolèrent un contexte récent borné | Le contexte ancien n'est plus accessible à l'attention |
| Cache déporté (offloaded) | La mémoire du périphérique est rare et le budget de latence permet le transfert | Le transfert hôte/périphérique peut dominer la latence |
| Cache quantifié | La mémoire est le goulot d'étranglement et le modèle/backend le supporte | La précision propre à la tâche et le comportement des noyaux doivent être mesurés |
| Cache de service paginé / géré par blocs | Nombreuses séquences concurrentes de longueurs inégales | Réglage opérationnel propre au moteur |
| Cache de préfixe | Nombreuses requêtes partagent un préfixe identique et immuable | Nécessite des clés de cache exactes et des contrôles d'isolation |

Hugging Face documente les variantes de cache dynamique, statique, déporté et quantifié. Un moteur de service peut utiliser un allocateur par blocs ou par pages plutôt qu'un tenseur contigu unique. Sélectionnez l'implémentation prise en charge par le modèle et le backend déployés ; ne copiez pas les options d'un moteur sans rapport.

## Cache statique et formes compatibles avec la compilation {#static-cache-and-compile-friendly-shapes}

Un cache statique préalloue le stockage jusqu'à une longueur de cache maximale. Dans les configurations Transformers compatibles, il peut permettre une exécution adaptée à la compilation, mais il élève le plancher de mémoire.

```python
generation = model.generate(
    **inputs,
    cache_implementation="static",
    max_new_tokens=256,
)
```

Définissez le maximum à partir des limites de requêtes observées, auxquelles vous ajoutez une marge justifiée. Un maximum arbitrairement élevé transforme une optimisation en risque de saturation mémoire. Effectuez un test de endurance isolé avec la concurrence visée avant de l'activer pour le trafic de production.

## La réutilisation des préfixes est une frontière de données {#prefix-reuse-is-a-data-boundary}

La réutilisation des préfixes peut éviter de recalculer un prompt système commun, un préfixe de document ou un contexte partagé. Elle n'est sûre que si la clé de cache inclut toutes les entrées qui influencent le comportement :

```json
{
  "model_revision": "immutable-model-revision",
  "tokenizer_revision": "tokenizer:sha256:...",
  "chat_template_revision": "template:sha256:...",
  "system_prompt_revision": "prompt:sha256:...",
  "tenant_scope": "tenant_42",
  "tool_schema_revision": "tools:sha256:..."
}
```

Ne réutilisez jamais un état de cache entre locataires, utilisateurs, périmètres de permissions ou révisions de prompt, sauf si la politique autorise explicitement cette frontière précise. L'invalidation du cache relève ici de la correction et de la confidentialité, et non uniquement de la performance.

## Quantification et compression {#quantization-and-compression}

Les caches quantifiés réduisent le nombre d'octets par valeur stockée. La précision appropriée dépend du modèle, de l'architecture d'attention, de l'implémentation, de la longueur de contexte et de la tâche. Un cache moins gourmand peut améliorer la concurrence tout en dégradant la recherche d'information, la sortie structurée ou le raisonnement sur des contextes plus longs.

Validez les candidats avec :

1. un prompt fixe et une distribution de tokens générés figée ;
2. des cas représentatifs de contexte long et de recherche d'information ;
3. des vérifications de sortie structurée et d'usage d'outils ;
4. une comparaison de qualité avec la référence approuvée ;
5. la mémoire maximale, la latence p50/p95, le débit et le taux d'erreur ;
6. une condition de retour arrière si la qualité ou le taux d'OOM franchit un seuil.

Les travaux de recherche sur la compression peuvent suggérer des candidats, mais les chiffres publiés dans les articles ne constituent pas un plan de capacité de production.

## Exploitation du service {#serving-operations}

Séparez deux préoccupations :

```text
per-request correctness: prompt, cache key, context limit, output validation
system capacity: batching, allocator pressure, memory headroom, admission control
```

Pour un service multi-utilisateurs, le contrôle d'admission doit tenir compte de la capacité du cache avant d'accepter une requête. Rejeter ou mettre en file d'attente une requête avec un statut de capacité explicite est plus sûr que de l'accepter puis d'échouer après un travail partiel. Exportez la mémoire du cache, les séquences actives, les succès/échecs de cache, les évictions, les OOM et la latence comme signaux d'observabilité.

## Reçu de vérification {#verification-receipt}

```json
{
  "candidate": "cache-strategy-revision",
  "model_revision": "immutable-model-revision",
  "workload_revision": "eval:sha256:...",
  "context_distribution": "production-like-v3",
  "quality_gate": "no material regression",
  "capacity_gate": "no OOM at approved concurrency",
  "rollback": "dynamic-cache-baseline"
}
```

Un reçu indique clairement si un résultat s'applique au modèle, au moteur, à la charge et au matériel visés. Relancez-le après toute modification des poids du modèle, du tokenizer, de la politique de contexte, du noyau/backend ou du moteur de service.

## Pièges {#gotchas}

- **Le nombre de têtes KV n'est pas toujours celui des têtes d'attention.** GQA et MQA modifient le calcul de la mémoire. **Correctif :** lisez la configuration réelle du modèle avant d'estimer la capacité.
- **Une allocation statique peut échouer avant le premier token.** Un maximum élevé réserve de la mémoire même pour de petites requêtes. **Correctif :** dimensionnez-la à partir d'une limite mesurée et testez la concurrence.
- **Une clé de cache peut franchir une frontière de données par accident.** Des prompts d'apparence semblable peuvent avoir des locataires, outils ou permissions différents. **Correctif :** incluez les révisions et le périmètre dans la clé et échouez en mode sécurisé en cas de non-concordance.
- **Les gains de la quantification dépendent de la tâche.** Un cache qui préserve la perplexité sur des textes courts peut échouer sur la recherche d'information dans un contexte long. **Correctif :** validez les tâches cibles à la longueur de contexte déployée.
- **La mise en cache est un mécanisme d'inférence.** L'activer pendant l'entraînement peut provoquer des comportements inattendus. **Correctif :** suivez les recommandations d'entraînement du framework et séparez les configurations d'entraînement et de service.

## Sources {#sources}

- [Stratégies de cache Hugging Face](https://huggingface.co/docs/transformers/main/kv_cache)
- [Explication du cache Hugging Face](https://huggingface.co/docs/transformers/v5.12.0/cache_explanation)
- [Optimisation de l'inférence Hugging Face](https://huggingface.co/docs/transformers/main/llm_optims)
- [Documentation vLLM](https://docs.vllm.ai/en/latest/)
- [Utilitaires de génération Transformers](https://huggingface.co/docs/transformers/internal/generation_utils)

## Voir aussi {#see-also}

- [[model-optimization]]
- [[token-optimization]]
- [[production-patterns]]
- [[transformer-architecture]]
- [[llm-api-integration]]
- [[ollama-local-llms]]
