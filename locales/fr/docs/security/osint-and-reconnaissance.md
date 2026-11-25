---
title: "OSINT et reconnaissance"
category: techniques
tags: [security, osint, reconnaissance, shodan, google-dorking, metadata, enumeration]
level: 3
source_sha256: 237a9c888565812eaa12b322dd8067b3fc8208b09b87183d97a00f6ab68b75b1
translation: machine
translated_at: '2026-10-24'
---
# OSINT et reconnaissance {#osint-and-reconnaissance}

Techniques de renseignement en sources ouvertes : recherche d'infrastructures avec Shodan/Censys, Google Dorking, extraction de métadonnées (EXIF, métadonnées de documents), énumération de sous-domaines, investigation sur les noms d'utilisateur et les adresses e-mail, et analyse de la Wayback Machine.

## Points clés {#key-facts}
- Shodan balaie l'intégralité de l'espace IPv4 et indexe les bannières de services : reconnaissance passive, sans toucher à la cible
- Le Google Dorking a été systématisé en 2002 (Johnny Long) et reste très efficace
- Les données EXIF des photos peuvent contenir des coordonnées GPS, le numéro de série de l'appareil et le logiciel de retouche utilisé
- Les sites gouvernementaux sont une mine d'or de métadonnées de documents (noms d'auteurs, chemins internes)
- Les journaux de Certificate Transparency (crt.sh) révèlent tous les certificats SSL émis pour un domaine
- L'OSINT passif (données publiques) est légal ; le balayage actif (interaction avec les systèmes cibles) nécessite une autorisation

## Shodan {#shodan}
Balaie l'espace IPv4, sonde les ports et collecte les bannières :
```typescript
port:22                              # SSH servers
os:"Windows 7"                       # Specific OS
city:"Moscow"                        # Location
org:"Company"                        # Organization
ssl.cert.subject.CN:"example.com"   # SSL certificates
http.title:"Dashboard"              # Web interface titles
has_screenshot:true                  # With screenshots (VNC, RDP, webcams)
```

### Outils associés {#related-tools}
- **Censys** - orienté certificats, données plus structurées, mieux adapté à l'analyse TLS
- **BinaryEdge** - renseignement sur les menaces en temps réel, découverte d'objets connectés (IoT), surveillance des fuites de données

## Google Dorking {#google-dorking}
```bash
site:example.com                     # Limit to domain
intitle:"index of"                   # Directory listings
inurl:admin                          # URLs with "admin"
filetype:pdf                         # Specific file types
intext:"password"                    # Content search

# Practical examples
filetype:env "DB_PASSWORD"           # Exposed .env files
filetype:sql "INSERT INTO" "password"  # Exposed database dumps
intitle:"phpinfo()" "PHP Version"    # PHP info pages
site:gov.* filetype:xlsx             # Government spreadsheets
inurl:"/view.shtml" intitle:"camera" # IP cameras
filetype:yml "password:"             # Exposed config files
```

Défense : un `robots.txt` correct, des contrôles d'accès côté serveur, `X-Robots-Tag: noindex` et des audits réguliers de vos propres dorks sur vos domaines.

## Extraction de métadonnées {#metadata-extraction}

### Données EXIF (images) {#exif-data-images}
```bash
exiftool image.jpg
```
Contient : modèle de l'appareil, numéro de série, coordonnées GPS, date et heure, logiciel de retouche, miniature d'origine (pouvant survivre à la retouche).

### Métadonnées de documents (DOCX, PDF, PPTX) {#document-metadata-docx-pdf-pptx}
- Nom de l'auteur (souvent le vrai nom issu du profil du système d'exploitation)
- Nom de l'organisation
- Dates de création et de modification, durée d'édition
- Historique des révisions, informations sur l'imprimante
- Outils : `exiftool`, `FOCA`

## Énumération de sous-domaines {#subdomain-enumeration}
```bash
sublist3r -d example.com            # Brute-force + public sources
amass enum -d example.com           # Comprehensive enumeration
subfinder -d example.com            # Fast passive enumeration
```
Sources complémentaires : Certificate Transparency (crt.sh), tentatives de transfert de zone DNS, dorks de moteurs de recherche (`site:*.example.com`).

## Investigation sur les noms d'utilisateur et les e-mails {#username-email-investigation}

### Recherche de noms d'utilisateur multi-plateformes {#cross-platform-username-search}
- **Sherlock** - vérifie plus de 300 plateformes
- **Maigret** - recherche avancée avec analyse des profils
- **Holehe** - vérifie si une adresse e-mail est enregistrée sur des services (sans alerter l'utilisateur)

### Investigation sur les e-mails {#email-investigation}
- **Have I Been Pwned** - vérification légitime des fuites de données
- **DeHashed / IntelX** - recherche avancée dans les données de fuites
- L'analyse des en-têtes d'e-mail révèle : le chemin de routage, l'adresse IP de l'expéditeur, les résultats SPF/DKIM, le client de messagerie

### Énumération de comptes {#account-enumeration}
De nombreux services révèlent l'existence d'un compte lors :
- de la réinitialisation de mot de passe (« e-mail introuvable » ou « lien de réinitialisation envoyé »)
- de l'inscription (« e-mail déjà utilisé »)
- des différences de délai dans les réponses d'authentification

## Analyse des archives web {#web-archive-analysis}
- **archive.org** (Wayback Machine) - instantanés historiques de sites web
- Révèle : anciens propriétaires, anciens contacts, contenus supprimés, profils modifiés
- **archive.is** et **Google Web Cache** comme alternatives
- Les images des réseaux sociaux restent stockées sur des CDN pendant des années, même après « suppression »
- Utiliser `web.archive.org/save/URL` pour conserver les preuves avant leur suppression

## Détection de la pile technologique {#technology-stack-detection}
- **Wappalyzer / BuiltWith** - identifient CMS, frameworks, outils d'analyse et CDN
- Les en-têtes de réponse HTTP révèlent le logiciel serveur et ses versions
- `robots.txt` et `sitemap.xml` divulguent la structure du site
- Les commentaires du code source peuvent contenir des identifiants, des chemins internes et des informations de débogage

## Reconnaissance DNS {#dns-reconnaissance}
```bash
dig example.com ANY
dig axfr @ns1.example.com example.com   # Zone transfer attempt
fierce --domain example.com             # DNS enumeration
```

## Découverte d'adresses IP {#ip-address-discovery}
- Recherche DNS pour le domaine
- Les enregistrements DNS historiques révèlent les IP réelles derrière les CDN
- Contournement de CDN : vérifier les sous-domaines non proxifiés, les en-têtes d'e-mail, l'historique des certificats SSL
- Outils : SecurityTrails, ViewDNS.info, DNSdumpster

## Pièges à éviter {#gotchas}
- Les données Shodan peuvent être obsolètes : vérifier systématiquement que les résultats sont toujours valables
- Les résultats de Google Dorking évoluent au fil de la réindexation : sauvegarder les preuves immédiatement
- La suppression des métadonnées EXIF est courante sur les téléversements vers les réseaux sociaux (Facebook, Twitter), mais pas sur toutes les plateformes
- Les transferts de zone (AXFR) sont presque toujours refusés sur des serveurs correctement configurés
- Holehe peut déclencher des limitations de débit et des verrouillages temporaires de comptes sur certaines plateformes
- Toujours distinguer l'OSINT passif du balayage actif pour respecter les limites légales

## Voir aussi {#see-also}
- [[penetration-testing-methodology]] - la reconnaissance comme première phase
- [[browser-and-device-fingerprinting]] - méthodes de fingerprinting technique
- [[deepfake-and-document-forensics]] - analyse d'images et de documents
- [[network-traffic-analysis]] - nmap, balayage actif
