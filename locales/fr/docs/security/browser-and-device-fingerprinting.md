---
title: "Empreinte numérique du navigateur et de l'appareil"
category: concepts
tags: [security, fingerprinting, canvas, webgl, anti-fraud, tracking, privacy]
level: 3
source_sha256: 3423d6d4bb174649600e279d686e8018e5a48d427c698bad65b9d1f01cbb6058
translation: machine
translated_at: '2026-10-24'
---
# Empreinte numérique du navigateur et de l'appareil {#browser-and-device-fingerprinting}

Méthodes d'empreinte technique utilisées par les systèmes anti-fraude et de suivi : empreinte canvas, WebGL, AudioContext, énumération des polices, signaux matériels, empreinte de la pile TCP/IP, fuites WebRTC, et mécanismes de suivi persistants (evercookies).

## Points clés {#key-facts}
- L'empreinte canvas exploite les différences de rendu entre GPU et OS, invisibles à l'œil humain
- WebGL expose directement le modèle de GPU via l'extension `WEBGL_debug_renderer_info`
- L'empreinte AudioContext repose sur les différences de traitement de l'API Web Audio
- L'empreinte de la pile TCP/IP (p0f) détecte l'OS, même à travers un VPN
- Les requêtes STUN de WebRTC peuvent divulguer l'IP réelle derrière un VPN
- Les evercookies stockent des identifiants à plus de 10 emplacements pour survivre à l'effacement

## Empreinte canvas {#canvas-fingerprinting}
Le navigateur dessine du texte et des graphiques dans un `<canvas>` à l'aide du GPU et des bibliothèques de rendu de l'OS. Des combinaisons matériel + logiciel différentes produisent des écarts au niveau du pixel.

Processus : forcer le rendu d'un texte spécifique et de formes géométriques -> `toDataURL()` ou `getImageData()` -> calculer un hash des données de pixels.

Facteurs : modèle de GPU, version du pilote, rendu des polices de l'OS (DirectWrite/CoreText/FreeType), antialiasing, rendu sous-pixel.

Contournement : les navigateurs anti-détection injectent du bruit dans les données de pixels. Un bruit cohérent est essentiel : un bruit aléatoire à chaque appel paraît suspect.

## Empreinte WebGL {#webgl-fingerprinting}
- `UNMASKED_VENDOR_WEBGL` et `UNMASKED_RENDERER_WEBGL` révèlent directement le GPU
- Paramètres supplémentaires : taille maximale des textures, dimensions maximales du viewport, précision des shaders, extensions prises en charge
- Combinée à des tests de rendu 3D, elle produit une empreinte très unique

## Empreinte AudioContext {#audiocontext-fingerprinting}
`OscillatorNode` -> `DynamicsCompressorNode` -> `AnalyserNode` -> extraction du tampon audio traité. Les différences de calcul en virgule flottante lors du traitement audio selon les plateformes créent des signatures uniques.

## Énumération des polices {#font-enumeration}
- Canal latéral : rendre le texte dans les polices candidates et dans la police de repli, puis mesurer les écarts de largeur et de hauteur
- Les ensembles de polices sont très révélateurs : les polices d'Adobe Creative Suite diffèrent de celles de Windows par défaut
- Les polices propres à une langue révèlent la locale

## Signaux matériels {#hardware-signals}
- `screen.width`, `screen.height`, `screen.colorDepth`, `devicePixelRatio`
- `navigator.hardwareConcurrency` (nombre de cœurs CPU logiques)
- `navigator.deviceMemory` (RAM approximative, en Go)
- API Battery Status (largement dépréciée ou restreinte)
- Les décalages de calibration des capteurs (accéléromètre, gyroscope) sont propres à chaque appareil
- `navigator.mediaDevices.enumerateDevices()` renvoie les identifiants des périphériques audio et vidéo

## Identifiants d'appareil au niveau de l'OS {#os-level-device-identifiers}
- **Windows** : GUID de la machine (`HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`), numéros de série des disques, UUID du BIOS
- **Linux** : `/etc/machine-id`, `/var/lib/dbus/machine-id`
- **Adresses MAC** : faciles à falsifier, mais collectées lorsqu'elles sont disponibles
- **Clé d'approbation TPM** : liée au matériel, impossible à falsifier

## Empreinte de la pile TCP/IP {#tcpip-stack-fingerprinting}
Les détails d'implémentation de l'OS fuient dans les paquets :
- TTL initial (Linux : 64, Windows : 128)
- Taille de la fenêtre TCP et ordre des options
- Génération de la séquence d'identifiants IP
- Comportement du bit Don't Fragment

Outil : `p0f` — détection passive de l'OS. Fonctionne même à travers un VPN, car les paramètres TCP proviennent de l'OS source.

## Fuites WebRTC {#webrtc-leaks}
ICE (Interactive Connectivity Establishment) collecte les IP candidates :
- IP publique via la réponse du serveur STUN
- IP locale/privée provenant des interfaces réseau
- Même derrière un VPN, peut révéler l'IP réelle ou la plage du réseau local

Atténuation : désactiver WebRTC (`media.peerconnection.enabled = false` dans Firefox), extensions de navigateur.

## Suivi persistant (Evercookies) {#persistent-tracking-evercookies}
Stocker des identifiants à plusieurs emplacements pour survivre à l'effacement :
- Cookies HTTP, LSO Flash, stockage Silverlight
- `localStorage`, `sessionStorage`, `IndexedDB`, Web SQL
- ETags HTTP (basés sur le cache)
- Supercookies HSTS (encodage de bits par sous-domaine)
- `window.name`, cache de favicon

Lors d'une nouvelle visite : vérifier tous les emplacements ; si l'un survit, restaurer les autres.

### Stockage du navigateur {#browser-storage}
- `localStorage` : persiste jusqu'à effacement explicite, 5 à 10 Mo par origine
- `sessionStorage` : par onglet, effacé à la fermeture
- `IndexedDB` : structuré, grande capacité
- API Cache / Service Workers : persiste entre les sessions

### Synchronisation des cookies {#cookie-syncing}
Les régies publicitaires synchronisent leurs identifiants via des chaînes de redirections. ITP (Safari) et ETP (Firefox) restreignent progressivement cette pratique.

## Pièges {#gotchas}
- Les navigateurs anti-détection peuvent falsifier la plupart des empreintes, mais une falsification cohérente sur tous les vecteurs est extrêmement difficile
- Un bruit canvas variant à chaque appel est plus suspect qu'une empreinte constante
- Le mode privé/incognito n'empêche PAS l'empreinte numérique : il efface seulement le stockage
- Plusieurs vecteurs d'empreinte se combinent : neutraliser l'un laisse des dizaines d'autres en place
- Tor Browser vise spécifiquement l'uniformité de l'empreinte (tous les utilisateurs paraissent identiques)

## Voir aussi {#see-also}
- [[anti-fraud-behavioral-analysis]] - schémas comportementaux complétant les empreintes
- [[tls-fingerprinting-and-network-identifiers]] - analyse des IP, géolocalisation
- [[osint-and-reconnaissance]] - utilisation des données d'empreinte pour une enquête
- [[web-application-security-fundamentals]] - CSP, cookies, stockage
