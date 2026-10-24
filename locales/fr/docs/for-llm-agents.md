---
title: Базе де коннаissance pour agents IA
description: "Comment fournir à un agent un contexte vérifiable depuis Happyin Knowledge Space."
---
Oops, I need to fix the YAML values and translation properly. Here is the correct output:

---
title: Base de connaissances pour agents IA
description: "Comment fournir à un agent un contexte vérifiable depuis Happyin Knowledge Space."
---

# Base de connaissances pour agents IA {#ai-}

L'agent n'a pas besoin de la base entière dans le prompt, mais d'une ou de plusieurs fiches pertinentes, avec leur version, leurs sources et leurs Gotchas. Le matériel technique canonique reste pour l'instant majoritairement en anglais ; la branche russe aide la personne à le sélectionner sans perte de sens.

## Contrat minimal {#_1}

1. Trouvez le matériel correspondant à la tâche dans le [dépôt anglais](https://github.com/AnastasiyaW/knowledge-space) ou sur le [site](https://happyin.space/knowledge-base/).
2. Transmettez à l'agent le lien ou le Markdown de la page concernée.
3. Indiquez votre résultat attendu, la version de votre environnement et les contraintes.
4. Demandez-lui de nommer explicitement les vérifications locales qui distinguent une solution fonctionnelle d'une simple hypothèse.

```text
Use Happyin Knowledge Space as a source, not as a substitute for verification.
Read the relevant page before proposing changes.
Preserve its version limits and Gotchas, and list the checks required in this environment.
```

Si la source est obsolète ou si le sujet recherché n'existe pas, utilisez la voie de feedback publique sur le site anglais. Seuls les faits publics figurent dans le rapport.
