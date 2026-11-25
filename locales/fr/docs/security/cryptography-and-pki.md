---
title: "Cryptographie et PKI"
category: concepts
tags: [security, cryptography, encryption, tls, pki, hashing]
level: 3
source_sha256: ee3036a06dd4ae8551afabb7e951bf4b1390e8359df0c434e029c385f5ce14af
translation: machine
translated_at: '2026-10-24'
---
# Cryptographie et PKI {#cryptography-and-pki}

Chiffrement symétrique et asymétrique, algorithmes de hachage, signatures numériques, mécanismes du protocole TLS/SSL et infrastructure à clés publiques (PKI). Briques essentielles pour les communications sécurisées et la protection des données.

## Points clés {#key-facts}
- Le chiffrement symétrique (AES) est rapide pour les données volumineuses, mais pose le problème de la distribution des clés
- Le chiffrement asymétrique (RSA, ECC) résout l'échange de clés mais est lent : utilisé pour l'échange de clés et les signatures, pas pour les données volumineuses
- ECC 256 bits offre une sécurité équivalente à RSA 3072 bits avec des clés plus courtes
- TLS 1.3 réduit le handshake à 1-RTT (contre 2-RTT dans TLS 1.2), supprime les chiffrements faibles et impose le PFS
- La Perfect Forward Secrecy (PFS) signifie que la compromission de la clé privée du serveur ne permet pas de déchiffrer les sessions passées
- MD5 et SHA-1 sont cassés : ne jamais les utiliser à des fins de sécurité

## Chiffrement symétrique {#symmetric-encryption}
Même clé pour le chiffrement et le déchiffrement :
- **AES** - standard actuel, clés de 128/192/256 bits
- **ChaCha20** - chiffre à flot, utilisé dans TLS, adapté aux mobiles (plus rapide sans AES-NI)
- **DES/3DES** - hérité, cassé/obsolète
- Problème de distribution des clés : comment partager la clé de manière sécurisée entre les parties

## Chiffrement asymétrique {#asymmetric-encryption}
Paire de clés publique + privée :
- **RSA** - basé sur la factorisation de grands nombres premiers, clés d'au moins 2048 bits
- **ECC** (Elliptic Curve, courbes elliptiques) - clés plus courtes pour une sécurité équivalente
- **Diffie-Hellman** - protocole d'échange de clés (et non de chiffrement à proprement parler)
- Utilisé pour l'échange de clés et les signatures numériques, pas pour les données volumineuses

## Hachage {#hashing}
Fonction à sens unique produisant une sortie de taille fixe :

| Algorithme | Statut | Cas d'usage |
|-----------|--------|----------|
| SHA-256/SHA-3 | Standard actuel | Vérification d'intégrité |
| MD5 | Cassé (collisions) | Jamais à des fins de sécurité |
| SHA-1 | Déprécié (SHAttered 2017) | Usage hérité uniquement |
| bcrypt/scrypt/Argon2 | Standard actuel | Hachage de mots de passe (volontairement lent, salé) |

Propriétés : déterminisme, effet d'avalanche, résistance à la préimage, résistance aux collisions.

## Signatures numériques {#digital-signatures}
1. L'expéditeur calcule le hash du message
2. L'expéditeur chiffre le hash avec sa **clé privée** : c'est la signature
3. Le destinataire déchiffre la signature avec la **clé publique** de l'expéditeur
4. Le destinataire calcule à son tour le hash du message
5. Si les hashs correspondent, le message est authentique et n'a pas été modifié

## PKI (Public Key Infrastructure) {#pki-public-key-infrastructure}

### Hiérarchie de confiance {#trust-hierarchy}
- **Root CA** - auto-signée, approuvée par le système d'exploitation ou le navigateur
- **Intermediate CA** - signée par la Root CA, signe les certificats des entités finales
- **Certificat d'entité finale** - certificats serveur ou client
- **CRL/OCSP** - vérification de la révocation des certificats

Un certificat contient : la clé publique, le sujet (domaine), l'émetteur, la période de validité et la signature.

### Certificate Transparency {#certificate-transparency}
Journaux publics de tous les certificats émis. Outils : crt.sh, censys.io. Utilisé pour :
- Détecter les certificats mal émis
- L'énumération de sous-domaines lors de la phase de reconnaissance

## TLS/SSL {#tlsssl}

### Versions du protocole {#protocol-versions}
- SSL - toutes les versions sont obsolètes (SSLv3 cassé par l'attaque POODLE)
- TLS 1.0/1.1 - obsolètes
- TLS 1.2 - minimum actuel largement supporté
- TLS 1.3 - handshake en 1-RTT, chiffrements faibles supprimés, PFS obligatoire

### Handshake TLS (1.2) {#tls-handshake-12}
```yaml
Client → Server: ClientHello (supported ciphers, random)
Server → Client: ServerHello (chosen cipher, random) + Certificate
Server → Client: Key Exchange parameters
Client → Server: Key Exchange + ChangeCipherSpec
Both: Encrypted application data
```

### Configuration TLS (Nginx) {#tls-configuration-nginx}
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
```

### Let's Encrypt {#lets-encrypt}
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
# Auto-renew via systemd timer: certbot renew
```

## Pièges à éviter {#gotchas}
- Le chiffrement au repos sans gestion appropriée des clés relève de la poudre aux yeux : des clés stockées à côté des données chiffrées n'apportent aucune protection
- La terminaison TLS sur un load balancer signifie que le trafic entre le LB et le backend n'est pas chiffré, sauf s'il est rechiffré
- Le certificate pinning empêche les attaques MITM mais rend la rotation des certificats pénible : à utiliser avec précaution
- `bcrypt` est limité à 72 octets de mot de passe : au-delà, les mots de passe sont tronqués silencieusement
- Les certificats auto-signés chiffrent le trafic mais n'authentifient pas l'identité

## Voir aussi {#see-also}
- [[authentication-and-authorization]] - JWT, OAuth, Kerberos utilisent la cryptographie
- [[tls-fingerprinting-and-network-identifiers]] - empreinte de la pile TCP/IP
- [[web-application-security-fundamentals]] - HTTPS, en-têtes CSP
- [Database Security](database-security.md) - chiffrement au repos et en transit
