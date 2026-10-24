---
title: "Empreintes TLS et identifiants réseau"
category: concepts
tags: [security, fingerprinting, ip-analysis, geolocation, vpn-detection, anti-fraud]
level: 2
source_sha256: 0ba041e9294f711b5385621849ec87bc0887e722d0b1c6b2f9c86b5fa19c71be
translation: machine
translated_at: '2026-10-24'
---
# Empreintes TLS et identifiants réseau {#tls-fingerprinting-and-network-identifiers}

Techniques d'identification au niveau réseau : classification et réputation des adresses IP, méthodes de géolocalisation et détection d'usurpation, détection des VPN, proxys et Tor, implications pour la vie privée de l'IPv6, et analyse des signaux Wi-Fi.

## Faits clés {#key-facts}
- Classification IP : résidentielle (risque faible), datacenter (risque élevé), mobile/CGNAT (modéré), sortie Tor (très élevé)
- La géolocalisation IP est précise au niveau de la ville à ~80 % pour les IP résidentielles
- Comparer la localisation déclarée, la localisation IP, le fuseau horaire et les paramètres de langue permet de détecter une usurpation
- L'IPv6 peut divulguer des informations réelles sur le réseau, même lorsque l'IPv4 est acheminé via un VPN
- Détection de « voyage impossible » : utilisateur à Moscou puis à Tokyo en 5 minutes = signal de fraude
- L'analyse des BSSID Wi-Fi peut confirmer ou contredire la localisation physique déclarée

## Classification des adresses IP {#ip-address-classification}
Le service anti-fraude classe les IP par type :

| Type | Niveau de risque | Remarques |
|------|-----------|-------|
| Résidentielle | Faible | IP grand public attribuées par le FAI |
| Datacenter/hébergement | Élevé | Indique un VPN, un proxy ou un bot |
| Opérateur mobile (CGNAT) | Modéré | Partagée entre de nombreux utilisateurs |
| Nœuds de sortie Tor | Très élevé | Listes de nœuds de sortie connus |

Exemple : un administrateur système qui accède à PayPal depuis le Wi-Fi d'un datacenter est signalé, car l'IP appartient à un hébergeur et non à un FAI résidentiel.

## Géolocalisation IP {#ip-geolocation}
- **Niveau ville** - ~80 % de précision pour les IP résidentielles
- **Identification du FAI** - très fiable
- **Détection VPN/proxy** - bases de données de réputation IP (MaxMind, IP2Proxy)
- Recoupement : localisation déclarée vs localisation IP vs fuseau horaire (`Intl.DateTimeFormat().resolvedOptions().timeZone`) vs langue du navigateur

## Méthodes de géolocalisation {#geolocation-methods}
1. **GPS** - le plus précis (quelques mètres), mobile uniquement
2. **Positionnement Wi-Fi** - trilatération à partir des positions connues des points d'accès, précision de 10 à 50 m
3. **Antenne-relais** - basé sur l'opérateur, 100 à 300 m en zone urbaine, plusieurs km en zone rurale
4. **Géolocalisation IP** - niveau ville, peu fiable pour les opérateurs mobiles
5. **Balises Bluetooth** - positionnement en intérieur

## Détection d'usurpation {#spoofing-detection}
- **Recoupement** : le GPS indique New York mais l'IP provient d'Allemagne
- **Incohérence de fuseau horaire** : fuseau horaire JavaScript vs fuseau horaire déduit de l'IP
- **Voyage impossible** : position A puis position B dans un délai physiquement impossible
- **Incohérence des BSSID Wi-Fi** : localisation X déclarée mais connexion à des points d'accès situés en Y

## Implications de sécurité de l'IPv6 {#ipv6-security-implications}
- Espace d'adressage de 128 bits (contre 32 bits pour l'IPv4)
- Prise en charge native d'IPsec intégrée dans les en-têtes de paquets
- De nombreux outils VPN et proxy ne prennent pas pleinement en charge l'IPv6 : le trafic IPv6 peut contourner le VPN
- Les environnements en double pile créent une surface d'empreinte supplémentaire
- Une adresse IPv6 intégrant l'adresse MAC (SLAAC sans extensions de confidentialité) peut identifier l'appareil

## Analyse des signaux Wi-Fi {#wi-fi-signal-analysis}
- **Atténuation du signal** - les atténuateurs USB permettent de modifier l'intensité du signal, ce qui fausse la distance perçue par rapport aux points d'accès
- **Blindage** - peinture ou tissu conducteur bloquant le Wi-Fi (nécessite une mise à la terre)
- **Usurpation d'adresse MAC** - modification de la MAC de l'adaptateur pour échapper au suivi

## Technique de la « bombe à retardement » des cookies {#cookie-time-bomb-technique}
La manipulation de l'horloge système avant la visite de sites entraîne l'émission de cookies avec des dates passées, donnant l'impression que l'appareil a déjà visité ces sites. Cette technique fonctionne sur les sites qui font confiance à l'heure transmise par le client pour horodater les cookies.

## Pièges à éviter {#gotchas}
- Les IP de datacenter ne sont pas toujours malveillantes : télétravailleurs utilisant un VPN, proxys d'entreprise
- Le CGNAT des opérateurs mobiles signifie que des milliers d'utilisateurs partagent une même IP : impossible de l'attribuer à un individu
- Les bases de données de réputation IP ont une latence : les nouvelles IP de VPN/proxy mettent de quelques jours à quelques semaines à être signalées
- L'usurpation GPS est triviale sur les appareils rootés ou jailbreakés
- Les extensions de confidentialité IPv6 génèrent des identifiants d'interface aléatoires, mais le préfixe /64 identifie toujours le réseau

## Voir aussi {#see-also}
- [[browser-and-device-fingerprinting]] - empreintes au niveau du navigateur
- [[anti-fraud-behavioral-analysis]] - signaux comportementaux
- [[network-security-and-protocols]] - fondamentaux TCP/IP
- [[cryptography-and-pki]] - détails du protocole TLS
