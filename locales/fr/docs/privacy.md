---
title: Politique de confidentialité
---
# Politique de confidentialité {#privacy-policy}

**Dernière mise à jour :** 24 octobre 2026

## Données collectées {#what-we-collect}

Lorsque vous vous abonnez aux mises à jour, nous enregistrons :

- Votre adresse e-mail
- L'horodatage de l'abonnement
- Votre adresse IP (pour la vérification du consentement)

En dehors de l'analyse facultative décrite ci-dessous, nous ne collectons ni noms, ni informations de paiement, ni autres données personnelles.

## Finalité de la collecte {#why-we-collect-it}

Vous envoyer, de temps à autre, des mises à jour par e-mail lorsque de nouveaux articles sont publiés sur happyin.space.

## Conservation des données {#how-we-store-it}

Vos données sont stockées sur l'infrastructure de Cloudflare (base de données D1), chiffrées au repos.

## Vos droits {#your-rights}

- **Se désabonner** à tout moment via le lien présent dans chaque e-mail, ou en nous contactant
- **Demander la suppression** de vos données en nous contactant
- **Demander l'export** de vos données en nous contactant

## Contact {#contact}

Pour toute question relative à la confidentialité : [GitHub Issues](https://github.com/AnastasiyaW/knowledge-space/issues) ou la [chaîne Telegram](https://t.me/happyin_space). D'autres moyens de contact sont présentés sur la [page de contact](contact.md). Merci de ne pas publier de données personnelles dans un ticket public ; demandez plutôt un canal privé.

## Comptages d'usage anonymes {#anonymous-usage-counts}

Nous comptabilisons l'utilisation du site ; nous ne constituons pas de profils de visiteurs.

- **Les vues de pages** proviennent de Cloudflare Web Analytics, qui ne dépose aucun cookie et ne procède à aucune empreinte numérique (fingerprinting) des visiteurs. Nous consultons ses totaux quotidiens par page, par site référent, par pays et par type d'appareil.
- **Compteur de retours.** Pour savoir si les personnes reviennent, votre navigateur conserve un petit enregistrement dans son stockage local : la date de votre première visite, la date de votre dernière visite et le nombre de jours différents où vous avez visité le site. Cet enregistrement reste sur votre appareil. Une fois par jour de visite, la page demande un très petit fichier dont le nom indique seulement l'une des situations suivantes :
    - une nouvelle visite ;
    - un retour après 1, 2-7, 8-30 ou 31 jours et plus ;
    - la même chose, depuis un navigateur ayant visité le site sur 5 jours différents ou plus.
- **Boutons Star.** Un clic sur un bouton « Star » demande un très petit fichier qui indique seulement l'emplacement du bouton : la barre supérieure, la fin d'un article, ou la notification affichée après la copie de code. La page demande également un fichier lorsque cette notification s'affiche, afin de savoir quel emplacement est efficace.
- **Robots d'indexation et assistants IA.** Nous consultons des statistiques agrégées des requêtes, regroupées par user agent, par exemple la fréquence à laquelle un assistant IA a récupéré un article pour le compte d'un utilisateur. Ces statistiques ne contiennent aucune adresse IP.

Ces requêtes ne transportent aucun cookie, aucun identifiant ni aucune adresse de page. Comme toute requête adressée à ce site, elles atteignent le réseau de Cloudflare avec votre adresse IP et les en-têtes HTTP standard de votre navigateur. Nos comptages utilisent le nom du fichier, le jour et le fait qu'un navigateur ait envoyé la requête ; ils ne contiennent aucune adresse IP.

L'enregistrement expire 13 mois après votre première visite, et les visites ultérieures ne le prolongent pas. La suppression des données de ce site le réinitialise.

Le compteur de retours et les comptages des boutons Star sont désactivés si l'une de ces conditions s'applique :

- votre navigateur envoie le signal Global Privacy Control ou Do Not Track ;
- le navigateur est piloté par un logiciel d'automatisation ;
- le navigateur ne permet pas au site de stocker des données ;
- vous le désactivez ci-dessous.

Les vues de pages dans Web Analytics et les statistiques agrégées des requêtes restent en vigueur. Safari supprime le stockage d'un site au bout de 7 jours de navigation sans aucune interaction avec ce site ; un visiteur Safari qui revient après une telle interruption est donc compté comme un nouveau visiteur.

<p class="ks-counter-switch"><span data-ks-counter-state>Ce commutateur nécessite JavaScript.</span> <button type="button" class="md-button" data-ks-counter-toggle>Désactiver</button></p>

## Google Analytics et publicité Google {#google-analytics-and-google-advertising}

Lorsque le propriétaire du site les a configurés, les pages chargent Google Analytics 4 et, sur les pages d'articles, les publicités Google AdSense. Le document [How Google uses information from sites or apps that use our services](https://policies.google.com/technologies/partner-sites) (en anglais) explique ce que Google fait de ces données ; [How Google uses cookies in advertising](https://policies.google.com/technologies/ads) (en anglais) décrit ses cookies publicitaires.

**Mode de consentement.** Les deux utilisent Google Consent Mode v2, configuré avant le chargement de tout script Google :

- **Dans l'EEE, au Royaume-Uni et en Suisse**, le stockage à des fins d'analyse et de publicité est désactivé par défaut (`analytics_storage`, `ad_storage`, `ad_user_data` et `ad_personalization` refusés). Une fenêtre de consentement s'affiche, et les cookies Google Analytics ne sont utilisés que si vous choisissez **Autoriser**. Jusque-là, Google peut tout de même recevoir des signaux sans cookies ni identifiants publicitaires (par exemple, le fait qu'une page a été consultée). Le consentement à la publicité personnalisée dans ces pays est recueilli par le message de consentement certifié de Google, affiché par Google lorsque les publicités sont activées ; sans lui, les publicités ne sont pas personnalisées dans ces pays.
- **Ailleurs**, ces réglages sont activés par défaut, et Google peut déposer des cookies d'analyse et publicitaires. Vous pouvez les désactiver à tout moment.
- **Le signal Global Privacy Control ou Do Not Track** passe tous les réglages à « refusé » : la balise Google Analytics n'est pas chargée du tout, et les éventuelles publicités s'affichent sans personnalisation fondée sur les cookies.

**Votre choix.** Le lien **Choix de confidentialité** présent dans le pied de page de chaque page, ainsi que le bouton ci-dessous, rouvrent la fenêtre de consentement. Choisir **Refuser** fait passer les quatre signaux du mode de consentement à « refusé » dans ce navigateur, interrompt nos événements d'analyse et supprime les cookies Google de ce site (`_ga`, `_ga_*`, `__gads`, `__gpi`, `__eoi`). Votre choix est conservé dans le stockage local de ce navigateur sous `ks_consent_v2`. Pour déterminer si la fenêtre doit être affichée, la page interroge `/api/consent-region` de ce site, qui répond uniquement « prompt needed: yes or no » à partir du pays que Cloudflare déduit de votre adresse IP ; le pays n'est pas stocké.

**Ce que nous mesurons.** L'utilisation globale de la base de connaissances : vues de pages et d'articles, usage de la recherche et ouvertures de résultats, copies de code, clics sur les étoiles GitHub et abonnements réussis à la lettre d'information, chacun avec la section du site et, pour les boutons, l'emplacement du bouton. Nous n'envoyons **pas** de termes de recherche, de prompts, d'adresses e-mail, de texte de retour, de chaînes de requête d'URL ni d'identifiants publicitaires dans ces événements, et les signaux Google ainsi que la personnalisation publicitaire sont désactivés pour notre analyse.

**Publicité.** Les publicités, lorsqu'elles s'affichent, proviennent de Google AdSense et n'apparaissent que sur les pages d'articles (jamais sur la page d'accueil, cette page, ni sur les pages « à propos » et contact). Google et ses partenaires peuvent utiliser des cookies pour diffuser des publicités en fonction de vos visites sur ce site et sur d'autres ; vous pouvez gérer la publicité personnalisée dans [Mon centre des annonces Google](https://myadcenter.google.com/). Les publicités sont signalées par la mention « Publicité » et n'influencent pas le contenu des articles.

<p class="ks-counter-switch"><span data-ks-analytics-state>Ce commutateur nécessite JavaScript.</span> <button type="button" class="md-button" data-ks-analytics-preferences hidden>Choix de confidentialité</button></p>

## Signalements {#feedback-reports}

Toute personne, y compris un assistant IA travaillant pour vous, peut envoyer un signalement à `/api/feedback` : un sujet manquant, un article obsolète ou erroné, ou un article utile. Nous conservons le contenu du signalement (type, sujet, article, détail, un lien facultatif et un nom de client facultatif tel que « claude-code »), l'heure, la méthode utilisée (POST ou GET), la famille du logiciel émetteur lue à partir de son User-Agent (par exemple « curl » ou « claude-user » ; le User-Agent complet n'est pas conservé), ainsi qu'un pseudonyme valable un jour : un hachage de l'adresse IP, de la date et d'un secret. Ce pseudonyme nous permet de limiter le nombre de signalements qu'un même émetteur peut envoyer par jour, et il ne permet pas de retrouver l'adresse. L'adresse IP elle-même n'est pas stockée. Les signalements ne sont lus que par le pipeline de recherche du propriétaire et ne sont jamais publiés sur le site ; la page de suivi d'un signalement n'affiche que son numéro, son type, sa date et son résultat et, une fois le signalement traité, le titre que nous lui avons donné ainsi qu'un lien vers le résultat ; la liste des sujets recherchés n'affiche que des titres rédigés par le propriétaire, jamais les termes d'un signalement ; un article rédigé en réponse cite ses propres sources, et non le signalement. Les signalements de plus de 12 mois sont supprimés automatiquement à l'arrivée du signalement suivant. Ne mettez aucune donnée personnelle dans un signalement. Pour obtenir la suppression anticipée d'un signalement, ouvrez une [GitHub Issue](https://github.com/AnastasiyaW/knowledge-space/issues) en indiquant son texte et sa date.

## Autres services chargés par les pages {#other-services-the-pages-load}

Les pages chargent des polices depuis Google Fonts, la bibliothèque de graphe 3D depuis jsDelivr (page d'accueil uniquement), et le nombre d'étoiles depuis l'API de GitHub. Chacun de ces services reçoit votre adresse IP et les en-têtes de votre navigateur, comme pour toute requête web. Lorsque Google Analytics ou les publicités sont activés, Google reçoit également les requêtes décrites ci-dessus, selon ses propres conditions de confidentialité.

## Cookies {#cookies}

- **Google Analytics** (`_ga`, `_ga_*`, jusqu'à 2 ans) et **cookies publicitaires Google** (`__gads`, `__gpi`, `__eoi` sur ce domaine, et cookies propres à Google sur les domaines Google), uniquement selon le mode décrit plus haut dans la section Mode de consentement : après votre consentement dans l'EEE, au Royaume-Uni et en Suisse ; par défaut ailleurs, jusqu'à ce que vous refusiez.
- **Cloudflare** peut déposer des cookies essentiels à la sécurité.
- **Stockage local**, et non cookies : le compteur de retours, votre choix de consentement, et le fait que la proposition de lettre d'information ait été fermée.
