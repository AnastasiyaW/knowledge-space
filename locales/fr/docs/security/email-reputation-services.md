---
level: 3
source_sha256: 2f5563f946439fe1830c1f9e438b1935cbb1ba5d18e89c6cb09b78c338cd75cb
translation: machine
translated_at: '2026-10-24'
---
# Réputation des e-mails et scoring par ancienneté pour la lutte contre la fraude {#email-reputation-and-age-scoring-for-anti-fraud}

Catégories de signaux, compromis entre services de fournisseurs et pile MVP « faite maison » pour bloquer les inscriptions à haut risque, fondées sur l'ancienneté et la réputation des adresses e-mail.

## Points clés {#key-facts}

- L'ancienneté de l'e-mail au moment de l'inscription est un prédicteur de fraude solide : les comptes dont l'e-mail a moins de 30 jours sont corrélés à la fraude par carte bancaire, aux rétrofacturations et à l'abus d'essais gratuits
- Aucun service ne connaît la *véritable* date de création de la boîte aux lettres ; les signaux sont des horodatages de première observation au sein du consortium du fournisseur, de l'historique des fuites de données et du WHOIS du domaine
- [[anti-fraud-behavioral-analysis]] couvre les signaux comportementaux (souris, frappe au clavier, durée de session) ; cet article traite des signaux statiques liés à l'e-mail appliqués à l'inscription
- [[disposable-email-detection]] couvre la détection des adresses jetables par liste de blocage ; cet article traite du scoring de réputation et d'ancienneté via des API tierces et des piles de signaux maison
- Transmettre des adresses e-mail brutes à des API tierces déclenche les obligations de l'article 4(1) du RGPD ; hacher systématiquement (SHA-256 ou MD5) avant la transmission, sauf si le DPA autorise explicitement l'envoi en clair
- Les services de validation d'e-mail (vérifications de délivrabilité par sondage SMTP) relèvent d'une **autre catégorie de produits** : ils vérifient la délivrabilité, pas l'ancienneté ni le risque de fraude
- Les plateformes de fraude pour grandes entreprises (niveau bancaire, 30 000 $+/an) sortent du périmètre des PME/SaaS ; voir [[threat-modeling]] pour associer les contrôles aux niveaux de risque

## Catégories de signaux {#signal-categories}

| Signal | Ce qu'il indique | Latence | Modèle de coût | Posture vis-à-vis de la vie privée |
|---|---|---|---|---|
| **Date de première observation dans le consortium** | Horodatage le plus ancien auquel le réseau de clients du fournisseur a interrogé cet e-mail ; approximation de l'ancienneté du compte | 150-400 ms | Par appel (PAYG ou abonnement) | E-mail haché avant envoi ; compatible RGPD si un DPA est en place |
| **Présence dans une fuite de données (type HIBP)** | L'e-mail est apparu dans une fuite de données connue ; les fuites anciennes (2012-2019) impliquent une ancienneté de compte de 5 à 10 ans et plus ; l'absence n'est PAS un signal de nouvel e-mail | 100-300 ms | Offre gratuite disponible (3,95 $ à 275 $/mois pour l'API HIBP) | API à k-anonymat MD5/SHA1 ; aucun e-mail brut transmis |
| **Empreinte numérique / présence sociale** | Comptes liés sur plus de 250 plateformes sociales ; une empreinte importante suggère un utilisateur légitime de longue date | 1,4-5 s (enrichissement OSINT) | Principalement par abonnement (699 $/mois et plus) | Basé sur l'OSINT ; complexité du DPA variable |
| **WHOIS du domaine / ancienneté d'enregistrement** | Domaine de l'e-mail (et non la boîte aux lettres) enregistré récemment ; détecte les domaines sosies récents, mais sans intérêt pour gmail.com ou hotmail.com | 200-500 ms (RDAP) | Gratuit (RDAP public) | Au niveau du domaine uniquement ; aucune donnée personnelle |
| **Liste de domaines jetables/temporaires** | Le domaine de l'e-mail correspond à un fournisseur jetable connu | <50 ms | Gratuit (listes de blocage open source) | Aucune donnée personnelle transmise |
| **Score de consortium antifraude** | Score agrégé à partir de signaux e-mail, IP et appareil provenant d'un réseau de fraude partagé | 150-300 ms | PAYG (0,015 $–025 $/appel) | E-mail haché ; IP et appareil inclus dans la charge utile |
| **Présence d'avatar/Gravatar** | Image de profil enregistrée pour le hachage de l'e-mail ; signal faible, plutôt orienté vers des audiences de développeurs | 200-400 ms | Gratuit (aucune clé requise) | Hachage MD5 uniquement |

## Catégories de fournisseurs {#vendor-service-categories}

Il existe trois niveaux ; le bon choix dépend du volume et de la tolérance au risque de fraude :

**Niveau 1 : API de consortium antifraude (e-mail + IP + appareil combinés)**
Tarification PAYG, sans seuil d'abonnement ; renvoie `first_seen`, `is_disposable`, `is_free` pour l'e-mail, ainsi que l'ancienneté du domaine, à côté des signaux IP et appareil. Programmes DPA matures. E-mail haché (MD5) par défaut avant transmission. Particulièrement adapté aux volumes PME et ETI, où un seul appel d'API doit couvrir plusieurs types de signaux.
- Capacité type : `email.first_seen`, `is_disposable`, ancienneté du domaine, géolocalisation IP, détection de proxy/VPN dans une seule réponse
- Latence : 150-300 ms ; coût : environ 0,015-0,025 $/appel en PAYG
- RGPD : fournisseur basé aux États-Unis ; DPA disponible sur demande ; certains délégués à la protection des données européens exigent un examen
- Piège courant : `first_seen` enregistre la première observation du fournisseur dans le consortium, et non la véritable date de création de la boîte aux lettres. Les fraudeurs interrogés pour la première fois reçoivent un horodatage vierge ; le signal se précise à mesure que la couverture du consortium s'étend

**Niveau 2 : API de risque spécifiques aux e-mails (meilleure fidélité de `first_seen`)**
Services de réputation d'e-mail dédiés, avec des signaux d'ancienneté plus propres (`first_seen: {human, timestamp, iso}`) et des indicateurs d'abus explicites (`recent_abuse`, `frequent_complainer`, `leaked`). Offres gratuites généreuses (5 000 requêtes/mois et plus), adaptées à la validation et aux tests A/B. Champ d'ancienneté au niveau du domaine uniquement (first_seen au niveau de la boîte aux lettres seulement lorsque le fournisseur a déjà observé l'adresse).
- Latence : 200-400 ms ; coût : offre gratuite + PAYG d'environ 0,001-0,005 $
- RGPD : fournisseur basé aux États-Unis, centre de données unique ; DPA sur demande
- Piège courant : `first_seen` renvoie « just now » (à l'instant) pour tout e-mail que le service n'a jamais vu auparavant, ce qui produit un taux élevé de faux positifs s'il est utilisé seul comme seuil. Le combiner avec `fraud_score`, `disposable` et `recent_abuse`

**Niveau 3 : empreinte numérique / enrichissement OSINT**
Vérifications de présence sur plus de 250 plateformes (réseaux sociaux, forums, jeux vidéo, réseaux professionnels). Renvoie `minimum_age_months`, `earliest_profile_date` et le `first_seen` du consortium. Signal catégoriquement plus fort que les niveaux 1 et 2 pour détecter les identités synthétiques, mais sa latence (1,4-5 s) exclut un blocage synchrone à l'inscription. Tarif d'entrée à partir de 699 $/mois minimum. À utiliser pour un enrichissement asynchrone après l'inscription, avec suspension du compte en cas de dépassement du seuil.
- Schéma : inscription terminée → tâche d'enrichissement asynchrone → si score > seuil → suspension et demande de revérification avant la première action payante
- La couverture de l'empreinte se dégrade à mesure que les plateformes sociales renforcent leur protection contre le scraping ; valider sur vos propres données de fraude étiquetées

## Pile MVP « faite maison » {#diy-mvp-stack}

Combine quatre signaux gratuits ou peu coûteux en un score de risque de 0 à 100. Aucun abonnement requis ; environ 50 à 200 $/an pour l'API HIBP à faible volume.

```python
import hashlib
import httpx
import asyncio
from datetime import datetime, timezone

async def check_breach_presence(email: str, client: httpx.AsyncClient) -> dict:
    """HIBP k-anonymity API: no raw email transmitted."""
    sha1 = hashlib.sha1(email.lower().encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = await client.get(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        headers={"hibp-api-key": "YOUR_KEY"},  # required for email API; range API is free
    )
    # Range API returns hashes for breaches, not email-specific breach list.
    # For per-email breach metadata use /breachedaccount/{email} endpoint (paid).
    breaches_found = suffix in resp.text
    return {"breached": breaches_found, "signal_strength": "strong_if_true"}

async def check_gravatar(email: str, client: httpx.AsyncClient) -> dict:
    """Gravatar presence: weak signal, skewed to dev/designer audience."""
    md5 = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        resp = await client.get(
            f"https://www.gravatar.com/{md5}.json",
            timeout=2.0,
        )
        return {"gravatar_present": resp.status_code == 200}
    except httpx.TimeoutException:
        return {"gravatar_present": None, "error": "timeout"}

async def check_domain_age(domain: str, client: httpx.AsyncClient) -> dict:
    """RDAP domain age via IANA bootstrap. Freemail domains (gmail.com etc) skip."""
    FREEMAIL_SKIP = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"}
    if domain.lower() in FREEMAIL_SKIP:
        return {"domain_age_days": None, "is_freemail": True}
    try:
        bootstrap = await client.get(
            "https://data.iana.org/rdap/dns.json", timeout=3.0
        )
        # Simplified: use rdap.org as convenience resolver
        rdap = await client.get(
            f"https://rdap.org/domain/{domain}", timeout=3.0
        )
        if rdap.status_code != 200:
            return {"domain_age_days": None}
        data = rdap.json()
        for event in data.get("events", []):
            if event.get("eventAction") == "registration":
                reg_date = datetime.fromisoformat(
                    event["eventDate"].replace("Z", "+00:00")
                )
                age_days = (datetime.now(timezone.utc) - reg_date).days
                return {"domain_age_days": age_days}
        return {"domain_age_days": None}
    except Exception as e:
        return {"domain_age_days": None, "error": str(e)}

async def check_disposable(domain: str, client: httpx.AsyncClient) -> dict:
    """
    Check against open disposable domain list.
    Fetch once, cache in memory or Redis for 24h.
    Source: github.com/disposable-email-domains/disposable-email-domains
    """
    resp = await client.get(
        "https://raw.githubusercontent.com/disposable-email-domains/"
        "disposable-email-domains/master/disposable_email_blocklist.conf",
        timeout=5.0,
    )
    blocklist = set(resp.text.strip().splitlines())
    return {"is_disposable": domain.lower() in blocklist}

def compute_risk_score(signals: dict) -> dict:
    """
    Combine signals into 0-100 risk score.
    Higher score = higher risk.
    """
    score = 0
    reasons = []

    if signals.get("is_disposable"):
        score += 40
        reasons.append("disposable_domain")

    domain_age = signals.get("domain_age_days")
    if domain_age is not None and not signals.get("is_freemail"):
        if domain_age < 7:
            score += 35
            reasons.append("domain_registered_<7d")
        elif domain_age < 30:
            score += 20
            reasons.append("domain_registered_<30d")

    if not signals.get("breached"):
        # Absence of breach does NOT imply new account; only presence implies age
        pass
    else:
        score = max(0, score - 15)
        reasons.append("breach_presence_age_signal")

    if signals.get("gravatar_present") is True:
        score = max(0, score - 10)
        reasons.append("gravatar_present")

    return {
        "score": min(score, 100),
        "reasons": reasons,
        "action": "block" if score >= 70 else ("require_verify" if score >= 40 else "allow"),
    }

async def email_risk_check(email: str) -> dict:
    domain = email.split("@")[-1]
    async with httpx.AsyncClient() as client:
        breach, gravatar, domain_age, disposable = await asyncio.gather(
            check_breach_presence(email, client),
            check_gravatar(email, client),
            check_domain_age(domain, client),
            check_disposable(domain, client),
        )
    signals = {**breach, **gravatar, **domain_age, **disposable}
    result = compute_risk_score(signals)
    result["signals"] = signals
    return result
```

```python
# Cache results in Postgres or Redis to avoid redundant API calls
# Cache TTL: 30 days for allow/block decisions; 1 day for require_verify
# Key: SHA-256(email) — never cache by raw email

import hashlib

def cache_key(email: str) -> str:
    return "email_risk:" + hashlib.sha256(email.lower().encode()).hexdigest()
```

## Schéma d'intégration {#integration-pattern}

**Principal : API de consortium antifraude (niveau 1)**
Appel unique à l'inscription couvrant l'ancienneté de l'e-mail, l'indicateur jetable et les signaux IP. PAYG, sans minimum d'abonnement. Hacher l'e-mail (MD5) avant transmission. Journaliser la réponse complète de l'API pour l'audit et le réglage des seuils.

**Secondaire : pile maison**
À exécuter en parallèle ou en repli lorsque l'API du niveau 1 est indisponible. Mettre les résultats en cache pendant 30 jours. Utiliser comme base de corrélation des signaux pour l'analyse des rétrofacturations sur 60 jours avant de souscrire à l'abonnement du niveau 1.

**Escalade : API d'empreinte numérique (niveau 3)**
Exclusivement asynchrone : ne jamais bloquer l'inscription de façon synchrone sur un enrichissement de 1,4 à 5 s. Schéma :

```text
POST /register
  ↓
[synchronous] disposable check (<50ms) → block if hit
[synchronous] Tier 1 consortium API (~200ms) → block/phone-gate on score
  ↓ signup completes
[async job queue] Tier 3 enrichment (1.4-5s) → suspend if score > threshold
  ↓
Log full response → audit table
  ↓
Monthly: correlate signal thresholds vs confirmed fraud / chargebacks → tune
```

**Variables d'environnement pour le fonctionnement en interrupteur d'urgence (kill switch) :**

```bash
EMAIL_RISK_THRESHOLD_BLOCK=75       # score >= this → reject registration
EMAIL_RISK_THRESHOLD_VERIFY=50      # score >= this → require phone/card verify
EMAIL_RISK_DISABLE=false            # kill-switch; set true to bypass all checks
```

## Pièges {#gotchas}

- **Problème :** Transmettre des adresses e-mail brutes aux API des niveaux 1 et 2 viole l'article 4(1) du RGPD pour les utilisateurs de l'UE, car l'e-mail est une donnée personnelle. -> **Correction :** Hacher l'e-mail avec MD5 (par défaut pour le niveau 1) ou SHA-256 avant transmission. Vérifier dans le DPA du fournisseur que le mode haché seul est pris en charge. Mettre à jour la politique de confidentialité pour mentionner le scoring de risque d'e-mail par des tiers.

- **Problème :** L'horodatage `first_seen` des API de consortium renvoie « just now » pour tout e-mail que le fournisseur n'a jamais vu, ce qui est courant pour les SaaS de niche dont la base d'utilisateurs diffère de celle des clients existants du fournisseur. Appliquer un seuil sur `first_seen` seul produit un taux élevé de faux positifs. -> **Correction :** Ne jamais utiliser `first_seen` comme porte unique. Le combiner avec `is_disposable`, un `fraud_score` explicite, les indicateurs `recent_abuse` et l'ancienneté WHOIS du domaine. Utiliser la présence dans une fuite de données comme signal d'ancienneté corroborant (présence = ancien ; absence = inconnu).

- **Problème :** L'enrichissement par empreinte numérique (niveau 3) prend de 1,4 à 5 secondes ; bloquer l'inscription de façon synchrone sur ce signal détruit la conversion. -> **Correction :** Exécuter l'enrichissement de façon asynchrone après l'inscription. Conditionner la première action payante (export, achat, création de clé API) plutôt que la création du compte. Mettre en place un flux de suspension de compte : création du compte → tâche d'enrichissement → si le seuil est dépassé, envoyer un e-mail « vérifiez votre identité pour continuer ».

- **Problème :** Les utilisateurs soucieux de leur vie privée (alias d'e-mail uniques, pas de Gravatar, pas de présence sur les réseaux sociaux, VPN) obtiennent artificiellement un score élevé avec les piles maison, alors qu'ils sont légitimes. -> **Correction :** Régler prudemment les seuils de la pile maison (require_verify à partir de 60, blocage à partir de 85). Prévoir un parcours clair de revue humaine pour les faux positifs. Suivre le taux de faux positifs chaque mois ; si plus de 2 % des utilisateurs réels atteignent require_verify, abaisser les seuils ou ajouter un parcours de régularisation.

## Voir aussi {#see-also}

- [[anti-fraud-behavioral-analysis]] — signaux comportementaux (souris, frappe, durée de session) complémentaires aux vérifications statiques de l'e-mail
- [[browser-and-device-fingerprinting]] — signaux au niveau de l'appareil à combiner avec le scoring de l'e-mail à l'inscription
- [[disposable-email-detection]] — détection des adresses jetables par liste de blocage ; à utiliser en première passe avant d'appeler les API de réputation
- [[authentication-and-authorization]] — architecture du parcours d'inscription, solution de repli par téléphone/SMS
- [[secure-backend-development]] — gestion sécurisée des identifiants d'API tierces et des données personnelles dans les journaux d'audit
- [[compliance-and-regulations]] — obligations RGPD des articles 4, 6 et 9 lors du scoring d'inscriptions issues de l'UE ; exigences des DPA
- [[threat-modeling]] — associer le niveau de contrôle antifraude (maison, niveau 1, niveau 3) au risque réel et à l'échelle

**Sources :**
- Documentation de l'API MaxMind minFraud : https://dev.maxmind.com/minfraud/api-documentation/requests/
- API IPQS Email Validation : https://www.ipqualityscore.com/documentation/email-validation-api/overview
- API SEON Email : https://docs.seon.io/api-reference/email-api
- Abonnement à l'API HIBP : https://haveibeenpwned.com/API/v3
- Liste de domaines d'e-mails jetables : https://github.com/disposable-email-domains/disposable-email-domains
- Bootstrap RDAP : https://data.iana.org/rdap/dns.json
