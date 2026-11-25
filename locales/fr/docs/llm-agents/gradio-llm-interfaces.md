---
title: "Gradio pour les interfaces LLM"
description: "Une frontière de production pour les interfaces de chat Gradio : streaming, file d'attente, exposition des données et contrats de déploiement"
level: 3
source_sha256: b055b5f39f9ec0c89c194741dbe6f14f46e59474ca95e8bfd120d98cc01b540b
translation: machine
translated_at: '2026-10-24'
---
# Gradio pour les interfaces LLM (septembre 2026) {#gradio-for-llm-interfaces-september-2026}

Contexte de version : les exemples utilisent la surface d'API actuelle de Gradio, `ChatInterface` et `Blocks`. Figez la version de Gradio déployée dans le fichier de verrouillage de l'application ; une mise à niveau de l'interface constitue une modification de version, et non une retouche cosmétique.

Gradio est une couche de présentation utile pour un service LLM. Il ne doit pas devenir le système de référence pour l'état des conversations, l'autorisation, les files de travaux ni les identifiants des fournisseurs de modèles.

## Contrat de frontière {#boundary-contract}

Gardez l'adaptateur d'interface étroit :

| Préoccupation | Responsabilité de Gradio | Responsabilité du service applicatif |
|---|---|---|
| Widgets de saisie, affichage en streaming, session navigateur | Oui | Non |
| Identité, autorisation, routage par locataire | Non | Oui |
| Identifiants des fournisseurs et politique de sélection des modèles | Non | Oui |
| Persistance des conversations et des travaux | Non | Oui |
| Permissions des outils, journal d'audit, quotas | Non | Oui |
| Délai d'expiration, reprise, idempotence | Non | Oui |

Un gestionnaire de réponse reçoit un message utilisateur et l'historique d'affichage, puis appelle un service avec une identité de requête explicite. Le service ne renvoie que du texte incrémental sûr pour l'affichage ou un enregistrement d'erreur terminal.

## Chat minimal en streaming {#minimal-streaming-chat}

Gradio traite une réponse issue d'un générateur comme un flux. Produisez à chaque fois la chaîne d'affichage complète accumulée ; produire uniquement le dernier jeton remplacerait la valeur d'affichage précédente.

```python
from collections.abc import Iterator

import gradio as gr


def stream_reply(message: str, history: list[dict[str, str]]) -> Iterator[str]:
    response = f"Received: {message}"
    assembled = ""

    for token in response.split():
        assembled = f"{assembled} {token}".strip()
        yield assembled


demo = gr.ChatInterface(
    fn=stream_reply,
    title="LLM interface boundary",
    description="A deterministic streaming example; connect a provider behind a service adapter.",
)

if __name__ == "__main__":
    demo.queue()
    demo.launch()
```

L'exemple est volontairement neutre vis-à-vis du fournisseur et s'exécute sans secret. Un adaptateur de production convertit les événements du fournisseur en un contrat d'événements local et stable avant de les produire vers Gradio.

## Adaptateur d'événements du fournisseur {#provider-event-adapter}

N'exposez pas directement à l'interface un objet du SDK du fournisseur. Normalisez à la frontière :

```python
from collections.abc import Iterable, Iterator
from typing import Any


def display_deltas(events: Iterable[dict[str, Any]]) -> Iterator[str]:
    assembled = ""

    for event in events:
        if event["type"] == "text_delta":
            assembled += event["text"]
            yield assembled
        elif event["type"] == "terminal_error":
            raise RuntimeError(event["message"])
```

Le service doit produire des événements validés tels que `text_delta`, `tool_started`, `tool_completed`, `citation` et `terminal_error`. Persistez séparément le reçu complet, qui n'est pas destiné à l'affichage ; l'historique du navigateur n'est pas un journal d'audit.

## Interfaces à plusieurs panneaux {#multi-panel-interfaces}

Utilisez `Blocks` lorsqu'une tâche nécessite une mise en page explicite et un câblage d'événements : chat, citations, référence de trace et panneau d'état de travail. Gardez chaque gestionnaire d'événements léger.

```python
import gradio as gr


def status_for(_: str) -> str:
    return "No durable job was submitted."


with gr.Blocks(analytics_enabled=False, delete_cache=(86400, 86400)) as demo:
    gr.Markdown("# LLM operations console")
    request_id = gr.Textbox(label="Request ID")
    status = gr.Textbox(label="Status")
    check = gr.Button("Check")
    check.click(status_for, inputs=request_id, outputs=status)

if __name__ == "__main__":
    demo.queue()
    demo.launch(server_name="127.0.0.1")
```

Un gestionnaire `Check` réel doit lire, à partir d'un identifiant de requête autorisé, les informations du service applicatif. Il ne doit pas parcourir des journaux arbitraires ni des chemins de fichiers fournis par le navigateur.

## Sémantique de file d'attente et de travaux {#queue-and-job-semantics}

Utilisez une file d'attente pour les callbacks interactifs coûteux, mais séparez la requête web du travail durable :

1. Validez l'identité, la taille de l'entrée et la limite de débit avant la mise en file.
2. Créez un élément de travail durable avec une clé d'idempotence.
3. Renvoyez au navigateur son identifiant de requête immuable.
4. Ne diffusez que l'état dérivé de cet élément de travail.
5. À la reconnexion, chargez l'état depuis le service plutôt que de rejouer un callback.

Pour les opérations longues sur le modèle, le worker gère l'annulation, l'échéance, les nouvelles tentatives et le reçu terminal. Gradio gère la présentation de la progression.

## Déploiement et exposition {#deployment-and-exposure}

`launch(share=True)` crée un lien public partageable et ne constitue pas un système de contrôle d'accès pour la production. Limitez le développement local à la boucle locale ; placez un déploiement accessible depuis Internet derrière un routage applicatif authentifié et une terminaison TLS.

Les règles d'accès aux fichiers de Gradio sont sensibles sur le plan de la sécurité. Les fichiers renvoyés, les chemins statiques ou un `allowed_paths` trop large peuvent rendre accessibles des fichiers de l'hôte. Utilisez un répertoire d'export dédié, ne contenant que les artefacts créés pour le locataire demandeur, et refusez tous les autres chemins.

Enregistrement opérationnel recommandé :

```json
{
  "request_id": "req_01J...",
  "tenant_id": "tenant_42",
  "actor_id": "user_8",
  "input_digest": "sha256:...",
  "model_policy": "chat-safe-v3",
  "started_at": "2026-09-03T18:00:00Z",
  "trace_ref": "trace_...",
  "terminal_state": "succeeded"
}
```

## Pièges à éviter {#gotchas}

- **Un flux n'est pas une transaction.** Des déconnexions du navigateur et des soumissions répétées peuvent survenir pendant la génération. **Correctif :** associez chaque action à une clé d'idempotence côté serveur et faites du reçu final la référence faisant autorité.
- **Les fichiers renvoyés peuvent être exposés.** Gradio indique que les répertoires autorisés et certains fichiers mis en cache ou renvoyés peuvent être accessibles depuis le navigateur. **Correctif :** ne renvoyez que les fichiers d'export générés depuis un répertoire délimité par locataire ; ne transmettez jamais de chemins larges de l'hôte.
- **Les liens de partage contournent les hypothèses de déploiement.** Un lien temporaire est utile pour une démonstration, mais ne remplace pas un routage authentifié, des limites de débit ou des contrôles d'audit. **Correctif :** déployez l'application derrière la même frontière d'identité que le service qu'elle invoque.
- **L'historique de l'interface n'est pas une mémoire.** L'état de session Gradio peut être évincé et ne doit pas contenir d'état de workflow privilégié ou durable. **Correctif :** stockez l'état durable dans le service applicatif et récupérez-en une projection à moindres privilèges.

## Sources {#sources}

- [Documentation Gradio ChatInterface](https://gradio.app/docs/gradio/chatinterface)
- [Documentation Gradio Blocks](https://gradio.app/docs/gradio/blocks)
- [Guide Gradio sur l'accès aux fichiers et la sécurité](https://gradio.app/guides/file-access)

## Voir aussi {#see-also}

- [[llm-api-integration]]
- [[production-patterns]]
- [[agent-deployment]]
- [[agent-architectures]]
