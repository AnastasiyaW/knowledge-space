---
title: Confidentialité
description: "Quelles données, quels cookies et quelle publicité utilise Happyin Knowledge Space."
---
# Confidentialité {#_1}

La branche russe n'ajoute aucun système distinct de collecte de données : elle fonctionne sur les mêmes pages et selon les mêmes règles que la base anglaise.

## Compteurs sans cookie {#cookie}

Les visites sont comptabilisées par Cloudflare Web Analytics : sans cookie et sans empreintes de navigateur. Le compteur anonyme de retours et des boutons « étoile » n'enregistre des données que dans le stockage local du navigateur ; les détails et le commutateur se trouvent dans la [politique en anglais](https://happyin.space/privacy/).

## Google Analytics et publicité Google {#google-analytics-google}

Si la propriétaire les a configurés, les pages chargent Google Analytics 4 et, sur les pages d'articles, la publicité Google AdSense. La manière dont Google utilise ces données est décrite dans le document [« Comment Google utilise les informations provenant des sites ou des applications de ses partenaires »](https://policies.google.com/technologies/partner-sites?hl=ru) et dans la section sur les [cookies publicitaires de Google](https://policies.google.com/technologies/ads?hl=ru).

**Mode de consentement (Consent Mode v2)** est défini avant le chargement de tout script Google :

- **Dans l'EEE, au Royaume-Uni et en Suisse**, le stockage à des fins d'analyse et de publicité est refusé par défaut. Vous verrez une demande, et les cookies Google Analytics ne sont utilisés qu'après un choix « Autoriser ». Jusque-là, Google peut recevoir des signaux sans cookie ni identifiants publicitaires (par exemple, la consultation d'une page). Le consentement à la publicité personnalisée dans ces pays est recueilli par la plateforme de gestion du consentement certifiée par Google, lorsque la publicité est activée ; sans ce consentement, la publicité n'est pas personnalisée.
- **Dans les autres pays**, ces paramètres sont activés par défaut, et Google peut déposer des cookies d'analyse et de publicité. Vous pouvez les désactiver à tout moment.
- **Global Privacy Control ou Do Not Track** désactivent tout : la balise Google Analytics n'est pas chargée, et la publicité s'affiche sans personnalisation par cookies.

**Votre choix.** Le lien « Paramètres de confidentialité » en bas de chaque page et le bouton ci-dessous rouvrent la demande. « Refuser » interdit les quatre signaux de Consent Mode dans ce navigateur, arrête nos événements d'analyse et supprime les cookies Google de ce site (`_ga`, `_ga_*`, `__gads`, `__gpi`, `__eoi`). Le choix est conservé dans le stockage local du navigateur (`ks_consent_v2`). Pour déterminer si la demande est nécessaire, la page interroge `/api/consent-region` de ce site ; celui-ci répond uniquement « nécessaire / non nécessaire » selon le pays que Cloudflare détermine à partir de l'adresse IP, et ne conserve pas le pays.

**Ce que nous mesurons.** Uniquement des actions agrégées : consultation des pages et des articles, utilisation de la recherche et ouverture des résultats, copie de code, passages vers GitHub et inscription réussie. Nous ne transmettons dans les événements ni les requêtes de recherche, ni les prompts, ni les adresses e-mail, ni le texte des retours, ni la query string des URL, ni les identifiants publicitaires ; les signaux Google et la personnalisation publicitaire sont désactivés pour notre analyse.

**La publicité** n'apparaît que sur les pages d'articles : jamais sur la page d'accueil, sur cette page ni sur les pages « À propos du projet » et « Contacts ». La publicité personnalisée peut être configurée dans le [« Centre publicitaire » de Google](https://myadcenter.google.com/). Les publicités sont signalées par le mot « Publicité » et n'influencent pas le contenu des articles.

<p class="ks-counter-switch"><span data-ks-analytics-state>Ce commutateur nécessite JavaScript.</span> <button type="button" class="md-button" data-ks-analytics-preferences hidden>Paramètres de confidentialité</button></p>

## Cookies {#cookie_1}

- **Google Analytics** (`_ga`, `_ga_*`, jusqu'à 2 ans) et **cookies publicitaires Google** (`__gads`, `__gpi`, `__eoi` sur ce domaine, et cookies propres à Google sur les domaines Google) — uniquement dans les conditions décrites ci-dessus.
- **Cloudflare** peut déposer les cookies de sécurité nécessaires.
- Dans le **stockage local** (et non en cookies) : le compteur de retours, votre choix de consentement et l'indication de fermeture ou non de la fenêtre d'inscription.

## Contact {#_2}

Pour les questions relatives aux données, utilisez les [GitHub Issues](https://github.com/AnastasiyaW/knowledge-space/issues) ou le [canal Telegram](https://t.me/happyin_space) ; plus de détails sur la page [« Contacts »](contact.md). Ne publiez pas de données personnelles dans un ticket public.

## Politique complète {#_3}

La politique complète et canonique (inscription, rapports d'erreurs, services tiers) se trouve [en anglais](https://happyin.space/privacy/). En cas de divergence, en attendant une vérification juridique distincte de la traduction, le texte anglais fait foi.
