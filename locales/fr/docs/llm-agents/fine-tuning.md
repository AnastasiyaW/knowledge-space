---
title: "Fine-tuning et LoRA"
description: "Choisir, exécuter et publier un fine-tuning via des contrats orientés évaluation, des jeux de données reproductibles et un entraînement efficace en paramètres."
tags: [llm-agents, fine-tuning, lora, qlora, peft, evaluation]
level: 3
source_sha256: 4e2c8baa683a3421ea6b233c29dcdd966a3ccd004a1f0efd92f6d25d072edbbc
translation: machine
translated_at: '2026-10-24'
---
# Fine-tuning et LoRA (septembre 2026) {#fine-tuning-and-lora-september-2026}

Contexte de version : la disponibilité des modèles, l'accès au fine-tuning géré, les API des trainers et le support matériel évoluent rapidement. Consignez la révision exacte du modèle de base, le tokenizer et le template de chat, les versions des bibliothèques, la révision du jeu de données et la suite d'évaluation pour chaque entraînement. Ne déduisez pas la disponibilité actuelle d'un fournisseur à partir d'un ancien exemple de code.

Le fine-tuning modifie le comportement du modèle. Il ne remplace ni des faits à jour, ni une autorisation, ni la qualité du retrieval, ni la sécurité des outils, ni une porte de validation avant mise en production. Commencez par un problème mesurable et conservez un jeu d'évaluation intact avant tout entraînement.

## Décider avant d'entraîner {#decide-before-you-train}

| Besoin | Première option | Pourquoi |
|---|---|---|
| Faits actuels ou privés | Retrieval ou outil de données contrôlé | Les faits peuvent être mis à jour sans réentraînement |
| Comportement ponctuel plus clair | Révision du prompt ou des instructions | Coût opérationnel le plus faible |
| Formatage, style, classification ou comportement de tâche stable et répétable | Fine-tuning après une baseline | L'entraînement peut réduire la longueur des prompts et améliorer la cohérence |
| Préférence entre des sorties valides | Optimisation par préférences lorsqu'elle est supportée | Les labels peuvent exprimer quelle réponse est préférée |
| Raisonnement à fort enjeu | Évaluation plus conception du workflow et des outils | L'entraînement ne rend pas un résultat non vérifié sûr |

La décision est empirique. Un fine-tuning ne se justifie que s'il améliore une évaluation représentative et tenue à l'écart, par rapport à une baseline documentée, et si son coût d'exploitation est acceptable.

## Figer le contrat d'expérimentation {#freeze-the-experiment-contract}

Avant de créer un job, consignez le problème et la règle de mise en production :

```json
{
  "run_id": "sft-2026-09-003",
  "base_model_revision": "approved-model-revision",
  "tokenizer_and_template_revision": "chat-template@42",
  "train_dataset_revision": "data:sha256:...",
  "eval_dataset_revision": "data:sha256:...",
  "baseline": "prompt-v7",
  "primary_metric": "schema_valid_and_human_approved",
  "promotion_rule": "beats baseline without safety regression"
}
```

Gardez les exemples d'entraînement, de validation et de test de release disjoints. Le test de release doit ressembler aux entrées de production, y compris les cas difficiles et ceux liés aux politiques, mais il ne doit servir à aucun réglage des hyperparamètres.

## Les données d'entraînement sont le produit {#training-data-is-the-product}

Chaque exemple doit enseigner le comportement attendu à l'inférence. Incluez les mêmes rôles, le même contrat de sortie, les mêmes outils ou la même représentation des résultats d'outils, la même langue et le même niveau de détail que ceux de la production.

```json
{"messages":[{"role":"system","content":"Return a JSON support triage record."},{"role":"user","content":"My order arrived damaged."},{"role":"assistant","content":"{\"category\":\"damage\",\"needs_human\":true}"}]}
```

La revue des données doit vérifier :

- le consentement, les licences, la confidentialité, la rétention et les frontières entre tenants ;
- les exemples dupliqués ou quasi dupliqués ;
- les labels contradictoires et les affirmations non étayées ;
- les instructions empoisonnées ou les erreurs générées par un modèle présentées comme vraies ;
- la sur-représentation des cas faciles ;
- les fuites de tests, d'identifiants, d'identifiants internes ou de données futures.

Ne placez pas de prompts de production secrets ni d'enregistrements clients bruts dans un fichier d'entraînement au motif qu'un fournisseur accepte le format JSONL.

## L'évaluation précède et suit l'entraînement {#evaluation-comes-before-and-after-training}

Mesurez d'abord la baseline. Exécutez ensuite le même jeu de test figé sur chaque candidat. Suivez au minimum une métrique de qualité de tâche, une métrique de sécurité ou de politique, et une métrique opérationnelle.

| Catégorie | Exemple de signal |
|---|---|
| Qualité de la tâche | Correspondance exacte, validité du schéma, score d'un relecteur approuvé ou grille du domaine |
| Sécurité | Conformité aux refus et aux politiques, résistance à l'injection, fuite de données sensibles |
| Opérations | Latence, consommation de tokens, taux d'échec, mémoire de déploiement, coût |
| Régression | Entrées où la baseline réussit mais le candidat échoue |

Analysez les groupes d'erreurs, pas seulement une moyenne unique. Un modèle qui améliore le formatage mais dégrade la sécurité sur les cas limites ne passe pas la porte de validation.

## Le fine-tuning géré est une surface mouvante {#managed-fine-tuning-is-a-moving-surface}

Le guide actuel d'optimisation de modèles d'OpenAI décrit un cycle alliant évaluations, prompting, affinage des données d'entraînement et réévaluation. Il indique également que sa plateforme de fine-tuning historique est en cours d'arrêt et n'est plus disponible pour les nouveaux utilisateurs. La disponibilité actuelle, les modèles de base supportés et les dates de dépréciation doivent être vérifiés dans la documentation actuelle du fournisseur avant de planifier un travail.

Pour toute plateforme gérée, conservez l'identifiant du job, l'instantané du modèle de base, le hash du jeu de données envoyé, la méthode, les hyperparamètres, le résultat de validation, ainsi que le plan de dépréciation et de remplacement. Ne prenez jamais une décision de déploiement à partir du seul alias d'un modèle.

## Fine-tuning efficace en paramètres {#parameter-efficient-fine-tuning}

LoRA et les méthodes PEFT apparentées entraînent des adaptateurs tout en gardant la plupart des poids du modèle de base fixes. Cela peut réduire la mémoire de l'optimiseur et des gradients par rapport à un fine-tuning complet, mais cela ne supprime ni le besoin d'évaluation, ni la nécessité de disposer d'entrées figées pour reproduire un résultat.

Une forme minimale d'entraînement supervisé avec les bibliothèques Hugging Face actuelles :

```python
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

adapter_config = LoraConfig(
    task_type="CAUSAL_LM",
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules="all-linear",
)

trainer = SFTTrainer(
    model=model_id,
    train_dataset=train_dataset,
    args=SFTConfig(
        output_dir="runs/sft-2026-09-003",
        max_length=1024,
        num_train_epochs=1,
    ),
    peft_config=adapter_config,
)

trainer.train()
```

L'architecture du modèle détermine les modules cibles compatibles, le formatage du chat, la précision, la longueur de séquence et le comportement matériel. Commencez par un test de fumée qui charge un batch, entraîne un pas, évalue un batch et écrit un manifeste d'artefact avant de lancer un entraînement long.

## QLoRA et quantification {#qlora-and-quantization}

QLoRA combine des adaptateurs efficaces en paramètres avec un chargement en faible précision pour faire tenir une expérimentation sur un matériel plus modeste. La quantification est un compromis entre mémoire et débit, non une garantie de qualité.

Testez chaque candidat à la précision et à la longueur de séquence qui seront utilisées en déploiement. Incluez la validité des sorties structurées, le comportement sur contexte long, les cas de sécurité et la précision sur la tâche cible. Une configuration d'entraînement moins gourmande en mémoire peut tout de même produire un candidat de release moins bon.

## Artefact de release {#release-artifact}

Un adaptateur promu ou un fine-tuning géré a besoin d'un manifeste déployable :

```json
{
  "candidate": "adapter-or-provider-model-id",
  "base_model_revision": "immutable-revision",
  "adapter_revision": "artifact:sha256:...",
  "tokenizer_revision": "artifact:sha256:...",
  "chat_template_revision": "artifact:sha256:...",
  "eval_receipt": "eval-2026-09-003",
  "rollback_target": "baseline-v7"
}
```

Servez le modèle de base, l'adaptateur, le tokenizer, le template et la politique comme une seule unité de release compatible. Conservez une cible de rollback et relancez la suite de release après toute modification d'un élément de cette unité.

## Pièges {#gotchas}

- **Le fine-tuning ne met pas à jour les connaissances factuelles.** Il peut même exprimer des faits périmés avec plus d'assurance. **Correction :** utilisez le retrieval ou un outil de données contrôlé pour les informations changeantes.
- **Les formats d'entraînement et d'inférence peuvent diverger.** Un tokenizer ou un template de chat différent peut effacer un gain mesuré. **Correction :** figez et testez l'ensemble complet du bundle de service.
- **Un découpage aléatoire peut laisser fuir des quasi-doublons.** Les scores exagèrent alors la généralisation. **Correction :** découpez par source, utilisateur, document ou date selon le cas.
- **Un entraînement peu gourmand en mémoire n'est pas une preuve de production.** La quantification et les adaptateurs peuvent modifier le comportement selon la tâche. **Correction :** évaluez la précision et la longueur de contexte exactes du déploiement.
- **Un endpoint de fournisseur peut être en transition.** La disponibilité du fine-tuning et les modèles éligibles peuvent changer. **Correction :** vérifiez l'accès actuel du compte et les consignes de dépréciation avant de concevoir autour de cette option.

## Sources {#sources}

- [Guide d'optimisation de modèles et de fine-tuning d'OpenAI](https://developers.openai.com/api/docs/guides/model-optimization)
- [OpenAI, travailler avec les evals](https://developers.openai.com/api/docs/guides/evals)
- [Documentation Hugging Face PEFT](https://huggingface.co/docs/peft/en/index)
- [Hugging Face TRL SFTTrainer](https://huggingface.co/docs/trl/en/sft_trainer)
- [Démarrage rapide bitsandbytes](https://huggingface.co/docs/bitsandbytes/main/quickstart)
- [Documentation de quantification de Transformers](https://huggingface.co/docs/transformers/quantization/bitsandbytes)

## Voir aussi {#see-also}

- [[model-optimization]]
- [[frontier-models]]
- [[ollama-local-llms]]
- [[rag-pipeline]]
- [[prompt-engineering]]
- [[agent-evaluation]]
