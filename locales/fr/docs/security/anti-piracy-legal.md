---
level: 3
source_sha256: b8016176a882d5fff6bfe47510a31f5f2d3542fdf0dce56d3a7545b5c5da9d58
translation: machine
translated_at: '2026-10-24'
---
# Cadre juridique anti-piratage : DMCA, secrets d'affaires, conception de CLUF {#anti-piracy-legal-framework-dmca-trade-secrets-eula-design}

Date : 2026-04-03
Contexte : Produit d'inférence ML de bureau. Mécanismes juridiques pour protéger les logiciels et les poids de modèles contre les usages et la distribution non autorisés.

---

## Protection des secrets d'affaires pour les modèles ML {#trade-secrets-protection-for-ml-models}

### Ce qui peut constituer un secret d'affaires {#what-qualifies-as-trade-secret}

Les poids de réseaux de neurones sont protégeables en tant que secrets d'affaires lorsque :
1. La valeur commerciale découle du secret (les concurrents profiteraient d'un accès)
2. Des mesures raisonnables sont prises pour maintenir le secret
3. Ils ne sont pas divulgués publiquement

**DTSA (Defend Trade Secrets Act, États-Unis) :** recours civil fédéral. Permet une injonction et des dommages-intérêts pour détournement.

**Ce que signifient « mesures raisonnables » en pratique :**
- Chiffrer les poids sur disque et en transit (AES-256-GCM)
- Restreindre l'accès : matériel de clés côté serveur, licence liée à l'appareil
- NDA pour tous les salariés et prestataires ayant accès au modèle
- Marquer les fichiers de modèle et la documentation « Propriétaire - Confidentiel »
- Journaux d'audit indiquant qui a accédé aux fichiers de modèle

**Ce qu'il faut NE PAS faire :**
- Livrer des poids en clair dans le bundle de l'application (détruit la revendication de secret d'affaires)
- Autoriser un accès hors ligne illimité sans aucune vérification serveur
- Partager des fichiers de poids bruts, même sous NDA, sans chiffrement

### Format ONNX/PyTorch = structure non protégeable par le droit d'auteur {#onnxpytorch-format-not-copyrightable-structure}

Pour les poids de modèles au format ONNX/SafeTensors : le format de fichier est ouvert, mais les valeurs de poids entraînées spécifiques sont protégeables par le droit d'auteur en tant que « compilation » ou protégeables en tant que secrets d'affaires. L'architecture (topologie du graphe) relève de l'idée et n'est pas protégeable par le droit d'auteur. Les valeurs entraînées spécifiques constituent l'expression.

---

## Contournement anti-circumvention au titre du DMCA (17 U.S.C. § 1201) {#dmca-anti-circumvention-17-usc-1201}

### Champ d'application {#what-it-covers}

Interdit de contourner les « mesures techniques de protection » (TPM) qui contrôlent l'accès à des œuvres protégées par le droit d'auteur.

**S'applique à :**
- Le chiffrement des poids de modèles (les poids = œuvre protégée + TPM = chiffrement)
- Les systèmes de vérification de licence qui contrôlent l'accès aux fonctionnalités du logiciel
- Les DRM protégeant les codes d'activation

**Exigence critique :** la protection contournée doit effectivement contrôler l'accès à une œuvre protégeable par le droit d'auteur. Une vérification de licence qui renvoie vrai/faux sans verrouiller cryptographiquement le contenu = argument DMCA plus faible. Modèle chiffré dont la clé = fonction(licence) = argument DMCA solide.

### Applicabilité {#enforceability}

**Cas solides (architecture licence-comme-donnée) :**
- Poids de modèles chiffrés, clé dérivée d'une licence valide → le contournement est clairement nécessaire pour accéder aux poids protégés
- `CreateSessionFromArray` d'ONNX Runtime avec déchiffrement → la TPM verrouille directement l'œuvre protégée

**Cas faibles (verrou booléen) :**
- `if (isLicensed()) { run(); }` → modifier la vérification relève d'une zone grise (certaines juridictions estiment qu'il ne s'agit pas d'un « contrôle d'accès » à l'œuvre sous-jacente)

**Application pratique :**
1. Demande de retrait DMCA auprès de l'hébergeur (GitHub, miroirs d'hébergement de type RuTracker) : rapide, nécessite des preuves minimales
2. Mise en demeure adressée aux personnes identifiées : efficace contre la contrefaçon commerciale
3. Action civile : coûteuse, réservée aux contrefaçons commerciales importantes

### DMCA et filigranes numériques {#dmca-for-digital-watermarks}

§ 1202 : interdit de supprimer ou de modifier les « informations relatives à la gestion du droit d'auteur » (CMI). Les filigranes intégrés aux images produites constituent des CMI s'ils identifient le titulaire du droit et la licence.

**Charge utile du filigrane pour le soutien au DMCA :**
```text
bits 0-31: license_id hash (ties output to specific license)
bits 32-47: timestamp (days since epoch)
bits 48-55: app version
bits 56-63: CRC-8
```

Grâce à cette charge utile, il est possible de détecter la suppression du filigrane. Si des sorties piratées apparaissent sans filigrane → action au titre du §1202 pour suppression intentionnelle.

---

## Conception de la CLUF pour les mesures anti-piratage {#eula-design-for-anti-piracy-measures}

### Informations obligatoires {#mandatory-disclosures}

La gestion à distance et le kill switch nécessitent une information explicite dans la CLUF pour être juridiquement défendables :

```text
LICENSE COMPLIANCE AND REMOTE MANAGEMENT

The Software periodically communicates with our servers to:
(a) Verify your license status and activation count;
(b) Transmit a device identifier (hardware fingerprint) for license
    validation purposes;
(c) Deliver configuration updates and security parameters.

In cases of confirmed license violation, we may progressively limit
application functionality. Full functionality is restored immediately
upon valid license activation. We will not damage or delete your
personal data as part of any compliance action.

By installing or using the Software, you consent to this communication.
```

**Précédent du rootkit Sony (2005) :** installation d'un rootkit DRM sans information → transaction à 7,50 $ par disque et rappel obligatoire. Toujours informer des mesures techniques de protection.

**Précédent WGA (2006) :** remontée quotidienne silencieuse vers le serveur → action collective → Microsoft a retiré cette fonctionnalité. Le comportement de remontée vers le serveur doit être divulgué.

### Clickwrap et browse-wrap {#clickwrap-vs-browse-wrap}

**Clickwrap (requis pour l'opposabilité) :** l'utilisateur coche activement la case « J'accepte » et doit faire défiler la CLUF. Appliqué par la plupart des tribunaux américains.

**Browse-wrap (« en utilisant ce logiciel, vous acceptez... ») :** faible, souvent inopposable aux consommateurs. À utiliser uniquement en complément du clickwrap.

**Mise en œuvre :** afficher la CLUF au premier lancement avec un bouton explicite « J'accepte ». Stocker l'horodatage de l'acceptation ainsi qu'un hash de la version de la CLUF dans un stockage persistant. En cas de mise à jour, la réafficher si la CLUF a changé.

### Considérations juridictionnelles {#jurisdiction-considerations}

**UE - Protection des consommateurs :**
- Directive sur les contenus numériques (2019/770), art. 14(2) : permet la résiliation pour violation du contrat moyennant un préavis « raisonnable »
- Directive sur les pratiques commerciales déloyales : une dégradation non divulguée peut constituer une pratique déloyale
- RGPD : empreinte d'appareil + données d'usage = données à caractère personnel → politique de confidentialité + base légale (intérêt légitime)

**Russie/CIS - Applicabilité limitée :**
- L'application des licences logicielles est pratiquement limitée pour les utilisateurs individuels
- L'application pour les entreprises et les usages commerciaux est possible devant les tribunaux russes
- Stratégie pratique : réponse graduée (dégradation de la qualité) plutôt que action en justice

**Chine - Régime d'application distinct :**
- La loi sur le droit d'auteur existe, mais son application pratique aux éditeurs de logiciels étrangers est difficile
- Envisager une tarification spécifique à la Chine et des moyens de paiement locaux pour réduire l'incitation économique au piratage
- Les canaux de distribution Weibo/WeChat sont plus difficiles à surveiller que le web ouvert

---

## Enregistrement du droit d'auteur {#copyright-registration}

Enregistrer le droit d'auteur sur le logiciel et les poids de modèles pour établir :
- Des dommages-intérêts légaux (750 à 30 000 $ par œuvre ; jusqu'à 150 000 $ en cas de contrefaçon délibérée)
- L'éligibilité au remboursement des honoraires d'avocat
- Une présomption de validité

**Ce qu'il faut enregistrer :**
- Le binaire du logiciel (en tant que « programme informatique »)
- Les poids du modèle (en tant que « compilation » ou « œuvre architecturale »)
- Enregistrer avant la contrefaçon pour être éligible aux dommages légaux

**Frais d'enregistrement du droit d'auteur aux États-Unis :** 45 à 65 $ par œuvre en ligne. Déposer dans les 3 mois suivant la publication pour bénéficier de l'option de dommages complets.

---

## Préservation des preuves pour l'application {#evidence-preservation-for-enforcement}

### Chaîne de traçabilité des filigranes {#watermark-chain-of-custody}

```python
# When pirated output detected: preserve evidence
evidence_record = {
    'detected_at': datetime.utcnow().isoformat(),
    'image_hash': sha256(image_bytes).hex(),
    'watermark_payload': decoded_payload,
    'license_id': lookup_license(decoded_payload['license_id_hash']),
    'original_activation': get_activation_record(license_id),
    'detection_confidence': confidence,
    'detection_threshold': 0.85,
    'detector_version': '2.1.0',
    'source_url': piracy_url,
}
# Store immutably with timestamp server signature
```

Exigences de la chaîne de traçabilité pour les litiges :
- Journaux serveur horodatés (utiliser un stockage de journaux en ajout seul)
- Enregistrements de détection signés cryptographiquement
- Conservation des URL/contenus contrefaisants d'origine (captures d'écran + captures des réponses HTTP)
- Enregistrements d'activation reliant le license_id à l'achat

### Préparation à un audit BSA {#bsa-audit-preparation}

Pour l'application contre la contrefaçon commerciale ou en entreprise via la BSA :
1. Documenter : nombre d'activations par licence, empreintes des appareils d'activation, dates
2. Preuves : journaux serveur montrant qu'un appareil utilisant le logiciel sous licence → sorties filigranées retrouvées en ligne
3. Saisine de la BSA : la BSA dispose d'un pouvoir délégué de ses sociétés membres ; orienter les cas de contrefaçon commerciale vers elle

---

## Paliers d'application pratiques {#practical-enforcement-tiers}

| Type de contrefaçon | Réponse | Mécanisme |
|---------------------|---------|-----------|
| Usage personnel individuel | Tolérer ou arrêt graduel | Kill switch étapes 1-2 |
| Indépendant commercial utilisant une copie piratée | Retrait DMCA chez l'hébergeur des sorties + kill switch | Détection de filigrane |
| Usage en entreprise | Renvoi vers audit BSA + lettre de mise en demeure | Anomalie du nombre de licences |
| Redistributeur de version craquée | Retrait DMCA auprès de l'hébergeur | Surveillance des URL |
| Développeur de crack (GitHub) | DMCA + mise en demeure | Procédure DMCA de GitHub |

---

## Pièges courants {#gotchas}

- **Verrou booléen sans chiffrement = argument DMCA faible.** Les tribunaux sont partagés sur la question de savoir si la modification d'une vérification booléenne de licence constitue le contournement d'une « TPM » protégeant l'œuvre. Licence-comme-donnée (poids chiffrés déchiffrés avec une clé dérivée de la licence) = TPM DMCA sans ambiguïté.
- **Kill switch sans information dans la CLUF = pratique déloyale (UE).** Impossible d'activer une dégradation à distance sans fondement divulgué. Le rootkit Sony (7,50 $ par disque) et le procès WGA établissent un précédent clair.
- **Le secret d'affaires exige des mesures de confidentialité effectives.** Livrer des poids non chiffrés dans le bundle de l'application = statut de secret d'affaires détruit. Il faut chiffrer + restreindre + NDA.
- **Les dommages légaux exigent un enregistrement en temps utile.** Un droit d'auteur enregistré après la découverte de la contrefaçon : seuls les dommages réels sont accessibles (difficiles à prouver). Enregistrer avant la livraison pour bénéficier de l'option de dommages légaux.
- **L'application en Chine est pratiquement limitée.** Même des revendications valides de droit d'auteur ou de secret d'affaires peuvent ne pas aboutir à une action d'application. La stratégie tarifaire et le filigranage sont plus pratiques sur le marché chinois que l'action juridique.
- **Le droit à l'effacement du RGPD s'applique à la télémétrie.** Si vous hachez des empreintes d'appareils pour la détection de piratage, une demande d'effacement RGPD pour cet appareil doit supprimer tous les enregistrements de télémétrie. Mettre en place un point d'accès à l'effacement.

## Voir aussi {#see-also}
- [[remote-kill-switch]]
- [[watermarking-encrypted-models]]
- [[adobe-piracy-patterns]]
- [[piracy-economics]]
