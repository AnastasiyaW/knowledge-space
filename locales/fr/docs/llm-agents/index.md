---
title: "LLM et agents IA"
type: MOC
level: 3
source_sha256: 0a84593682152b5363e36cfa851da3818a5a1b2782d89ed934ee033081fd1693
translation: machine
translated_at: '2026-10-24'
---
# LLM et agents IA {#llm-ai-agents}

## Fondements {#foundations}
- [[transformer-architecture]] - Guide pratique et tenant compte des versions sur la structure des transformeurs à attention, le décodage autorégressif, l'information positionnelle et les limites de configuration en production.
- [[tokenization]] - BPE, WordPiece, SentencePiece, fenêtres de contexte, comptage de tokens
- [[embeddings]] - Représentations vectorielles, métriques de similarité, modèles d'embedding, problèmes connus
- [[frontier-models]] - Comparatif et guide de sélection : GPT, Claude, Llama, Mistral, Gemini

## Prompting et génération {#prompting-and-generation}
- [[prompt-engineering]] - Prompts système, few-shot, chain-of-thought, motif checklist, distillation d'instructions
- [[function-calling]] - API d'utilisation d'outils d'OpenAI et d'Anthropic, descriptions d'outils, validation
- [[llm-api-integration]] - Chat completions, rôles des messages, streaming, paramètres, gestion des coûts

## Génération augmentée par récupération (RAG) {#retrieval-augmented-generation}
- [[rag-pipeline]] - Architecture RAG, problème des hallucinations, stratégies d'amélioration, évaluation
- [[chunking-strategies]] - Découpage de texte, tailles de chunks, chunking sémantique, chargeurs de documents
- [[vector-databases]] - Construire une récupération vectorielle autour d'embeddings versionnés, de filtres de métadonnées autorisés, de la provenance et de l'évaluation du rappel, avec une migration sûre plutôt que des classements de produits figés.

## Agents IA {#ai-agents}
- [[agent-fundamentals]] - Boucle ReAct, composants d'un agent, types, agent versus workflow
- [[agent-design-patterns]] - Plan-and-execute, reflexion, MRKL, scratchpad, principes de conception
- [[multi-agent-systems]] - Coordonner plusieurs agents à travers des contrats de tâches, la propriété, l'autorité, l'état et les limites de preuve ; n'ajouter des agents que lorsqu'une décomposition mesurée les rend nécessaires.
- [[agent-memory]] - Mémoire à court et long terme, HITL, motif copilote, gestion des conversations
- [[agent-security]] - Jailbreaks, injection de prompt, empoisonnement de données, stratégies de défense

## Frameworks et outils {#frameworks-and-tools}
- [[langchain-framework]] - Guide tenant compte des versions sur le harnais d'agents actuel de LangChain, les intégrations de fournisseurs, les middlewares, l'état et les limites de production.
- [[langgraph]] - Graphes à état, routage conditionnel, human-in-the-loop, orchestration multi-agents
- [[no-code-platforms]] - n8n, FlowWise, création d'interfaces avec Gradio, déploiement
- [[spring-ai]] - Intégration de LLM en Java/Spring Boot
- [[ai-coding-assistants]] - Exploiter les assistants de codage IA à travers des limites explicites de périmètre, de données, d'outils, d'approbation et de preuve, plutôt que des classements de produits ou une confiance accordée au code généré.
- [[qwen-code]] - Installation de la CLI Qwen Code, contrat de fournisseur et historique de l'authentification
- [[unsloth]] - Unsloth Core, Studio, Desktop, et limites du fine-tuning propres à chaque modèle

## Exploitation des modèles {#model-operations}
- [[fine-tuning]] - LoRA, QLoRA, PEFT, fine-tuning OpenAI, qualité des données
- [[model-optimization]] - Quantification (GGUF, GPTQ, AWQ), distillation, élagage
- [[ollama-local-llms]] - Mise en place de l'inférence locale, niveaux de quantification, sélection de modèles
- [[llmops]] - Évaluation, supervision, optimisation des coûts, CI/CD pour les applications LLM
- [[production-patterns]] - Injection de contexte déterministe, copilote, décomposition en workflows, journalisation

## Références complémentaires {#additional-references}

- [[adaptive-learning-systems]] - Motifs d'architecture pour les systèmes éducatifs pilotés par l'IA qui s'adaptent à chaque apprenant
- [[adaptive-patterns-for-autonomous-agents]] - Utiliser un état de tâche explicite, des hooks bornés, des sous-agents à capacités restreintes et des portes fondées sur des preuves, plutôt que des déclencheurs par mots-clés opaques ou des scores d'ambiguïté arbitraires.
- [[agent-architectures]] - Comment structurer le flux de contrôle et la gestion d'état d'un agent LLM au-delà des motifs individuels
- [[agent-deployment]] - Faire passer les agents du prototype à la production
- [[agent-evaluation]] - Évaluer le comportement d'un agent à l'aide de jeux de tâches versionnés, de validateurs déterministes, de contrôles d'effets de bord maîtrisés et de preuves reproductibles, plutôt qu'à partir d'un score de benchmark unique.
- [[agent-observability-dashboards]] - Observabilité en temps réel pour les systèmes multi-agents et sous-agents : télémétrie basée sur les hooks, événements
- [[agent-orchestration]] - Coordonner appels de modèles, outils, transferts, approbations, nouvelles tentatives et preuves à travers un état de tâche explicite, plutôt qu'une boucle d'agent propre à un framework.
- [[agent-safety-alignment]] - Construire la sécurité des agents comme des limites explicites d'autorité, de données, d'outils, d'approbation et de preuve, plutôt que comme une simple promesse portée par le prompt.
- [[agent-scope-evasion]] - Les agents de codage entraînés à réduire la complaisance présentent un mode de défaillance documenté : face à
- [[agent-self-improvement]] - Techniques permettant aux agents d'améliorer leurs propres performances par la réflexion, la récompense au niveau de l'étape
- [[agentic-rl-competitive-programming]] - GrandCode (2026) atteint des performances de niveau grand maître sur des problèmes de programmation compétitive grâce à
- [[agentic-security-2026]] - Guide de modélisation des menaces et de contrôles pour les agents utilisant des outils, les intégrations MCP, la mémoire persistante et les effets irréversibles. Périmètre vérifié le 2026-09-03.
- [[agentic-systems-landscape-2026]] - Protocoles multi-agents, comparatif des SDK, motifs d'orchestration et agents de codage en conditions réelles
- [[ai-adaptive-learning-systems]] - Architecture tenant compte des versions pour les preuves relatives à l'apprenant, la planification déterministe, le tutorat LLM contraint, l'évaluation et la protection des données d'apprentissage.
- [[ai-agent-ide-features]] - Concevoir et évaluer des environnements de codage assistés par IA autour de l'isolation des espaces de travail, des permissions explicites, des artefacts de tâche durables, de la vérification et de la revue.
- [[autonomous-agent-evolution]] - Remplacer la recherche évolutionnaire figée (agents sans état) par des agents autonomes à longue durée de vie
- [[chinese-ai-coding-ecosystem]] - Outils chinois de codage assisté par IA, motifs et pratiques communautaires : Trae, OpenSpec, MetaGPT, GLM-5
- [[claude-adaptive-thinking]] - Configurer et évaluer l'effort de raisonnement de Claude sans s'appuyer sur des pratiques figées et propres à chaque modèle.
- [[claude-code-degradation-2026]] - Méthode fondée sur des preuves tangibles pour diagnostiquer les évolutions de qualité, de configuration, de coût et de disponibilité d'un agent de codage, sans inventer d'incident chez le fournisseur.
- [[claude-code-ecosystem]] - Utiliser les plugins, skills, hooks, instructions de projet et sous-agents de Claude Code comme des surfaces de gouvernance explicites et versionnées ; vérifier leur schéma actuel et leur portée effective avant tout déploiement.
- [[claude-code-harness-patterns]] - Une frontière pratique entre instructions, outils, portes déterministes, revue et preuves durables pour le travail d'un agent de codage.
- [[claude-desktop-session-management]] - Utiliser les contrôles d'export, de compte et d'extension officiellement supportés plutôt que des éléments internes non versionnés du cache local, pour la récupération des conversations ou la synchronisation entre appareils.
- [[claude-managed-agents]] - Définir des sous-agents Claude Code gérés par l'organisation, avec portée explicite, ordre de priorité, limites d'outils et vérification, plutôt que de traiter la configuration gérée comme un environnement d'exécution dans le cloud.
- [[context-engineering]] - Traiter le contexte du modèle comme une entrée de travail bornée, et conserver l'état de la tâche, les preuves, l'autorité et la provenance de la récupération dans des artefacts versionnés plutôt que dans des allocations de tokens figées.
- [[gradio-llm-interfaces]] - Prototypage rapide d'interfaces de chat avec streaming, rendu Markdown et comparaison de plusieurs modèles
- [[handoff-rollup-pattern]] - Comment créer une synthèse bornée et auditable d'un travail d'agent de longue durée, sans prétendre qu'un résumé est sans perte.
- [[kv-cache-compression]] - Réduire la mémoire du cache KV pendant l'inférence des LLM afin d'allonger les contextes et d'augmenter le nombre de requêtes concurrentes
- [[llm-fine-tuning-practical]] - Guide de bout en bout pour le fine-tuning via API frontière et QLoRA, avec un cadre de décision sur le moment d'y recourir
- [[llm-persona-design-and-engineering]] - Concevoir la persona d'un LLM comme une politique comportementale versionnée, avec des limites explicites d'autorité, de confidentialité, d'escalade et d'évaluation, plutôt que comme une personnalité supposée du modèle.
- [[managed-agents]] - Guide tenant compte des versions sur le harnais d'agents gérés d'Anthropic : configuration des agents, environnements, sessions, événements, politiques de permission et limites des données.
- [[multi-agent-messaging]] - Motifs de communication inter-agents pour les sessions Claude Code : Agent Teams intégrés, basés sur les hooks
- [[multi-agent-systems-architectures-2026]] - Les systèmes multi-agents (MAS) se sont scindés en deux grandes écoles architecturales : fondées sur les rôles
- [[multi-session-coordination]] - Motifs de coordination durables pour plusieurs sessions d'agents de codage : worktrees isolés, manifestes, preuves en ajout seul, baux sur les ressources exclusives et intégration vérifiée.
- [[notebooklm-integration]] - Utiliser Google NotebookLM comme backend de recherche gratuit pour Claude Code, avec des workflows économes en tokens
- [[oh-my-claudecode-omc-architecture]] - Comment adopter le plugin OMC, qui évolue rapidement, sans confondre commandes tierces, routage de modèles ou état généré avec une limite stable de sécurité ou de publication.
- [[persona-adaptive-llm]] - Cadre de décision pour les champs de profil, la mémoire de récupération et la personnalisation par adaptateurs, avec isolation des locataires, évaluation, consentement et limites de suppression.
- [[scaling-laws-and-benchmarks]] - Loi d'échelle de Chinchilla, benchmarks standards (ARC, DROP, HellaSwag) et recommandations pour la sélection de modèles
- [[social-media-mcp-tools]] - Conception indépendante du fournisseur, centrée sur l'approbation, pour utiliser MCP afin de rédiger, valider et publier des contenus sur les réseaux sociaux sans traiter une publication comme une action réversible dans un chat.
- [[swarm-based-review-and-multisampling-in-agentic-workflows]] - Générer des candidats indépendants, valider les preuves et sélectionner les sorties des agents à partir de critères d'acceptation explicites, plutôt que de nombres de votes fixes ou de la confiance accordée par le modèle.
- [[telegram-managed-bots]] - Guide de mise en production sûre du modèle de bots gestionnaires de Telegram : création, rotation des tokens, paramètres d'accès, isolation d'état et reçus de cycle de vie.
- [[token-optimization]] - Réduire la consommation de tokens dans les systèmes d'agents sans dégrader les performances de la tâche
- [[tool-use-patterns]] - Comment concevoir, exposer et gérer les outils des agents LLM
- [[uml-driven-agent-development]] - Utiliser de petits diagrammes versionnés de séquence, d'états et de frontières de confiance pour clarifier les workflows d'agents, puis les valider dans le moteur de rendu et la cible CI qui les publieront.
