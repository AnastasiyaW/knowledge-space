---
title: "Conception d'API SOAP"
category: reference
tags: [soap, xml, wsdl, web-services, enterprise]
level: 3
source_sha256: d6eb4e05dc9e4a543c27c0088fcbf582945c93b9c80ee4860fae646159c12569
translation: machine
translated_at: '2026-10-24'
---
# Conception d'API SOAP {#soap-api-design}

SOAP (Simple Object Access Protocol) est un protocole de messagerie basé sur XML pour l'échange de données. Puissant mais lourd : il est utilisé principalement dans les systèmes d'entreprise et financiers, où les contrats stricts et la sécurité sont essentiels.

## Structure des messages {#message-structure}

Toutes les requêtes sont envoyées vers un point de terminaison unique. Les messages sont des enveloppes XML.

```xml
<Envelope>
  <Header>
    <SecurityToken>user_token_here</SecurityToken>
  </Header>
  <Body>
    <getBalanceRequest>
      <number>12345</number>
    </getBalanceRequest>
  </Body>
</Envelope>
```

### Éléments {#elements}

| Élément | Obligatoire | Rôle |
|---------|-------------|------|
| **Envelope** | Oui | Élément racine, définit le XML comme message SOAP |
| **Body** | Oui | Message effectif contenant les appels de fonction et les paramètres |
| **Header** | Non | Informations propres à l'application (jetons de sécurité, authentification) |
| **Fault** | Non | Informations d'erreur (enfant de Body, au maximum une fois par message) |

### Structure de Fault {#fault-structure}

- `faultcode` - type d'erreur (`soap:Sender` = erreur côté client)
- `reason` - explication lisible par un humain
- `detail` - informations supplémentaires de débogage

### Transport HTTP {#http-transport}

```http
POST /soap HTTP/1.1
Host: api.example.com
Content-Type: text/xml; charset=utf-8
SOAPAction: "doBalanceTransfer"
```

**Important :** HTTP 200 est renvoyé à la fois en cas de succès et d'erreurs métier. Seules les erreurs techniques/de protocole utilisent un code 4xx avec un SOAP Fault.

## WSDL (documentation) {#wsdl-documentation}

WSDL (Web Services Description Language) décrit l'API en XML. Il contient :

1. **Types** - types de données (schéma XSD)
2. **Interface** - méthodes/opérations disponibles et leurs entrées
3. **Binding** - méthode HTTP et protocole
4. **Service** - URL du point de terminaison

Comme SOAP est entièrement décrit par WSDL + XSD, aucune documentation supplémentaire n'est nécessaire. Il suffit de donner aux développeurs le fichier WSDL pour qu'ils comprennent l'API.

## Avantages {#advantages}

- **Format de données strict** - XML + schémas XSD réduisent le risque de données non sûres
- **Indépendance vis-à-vis du langage** - création de services à partir d'un WSDL, sans langage particulier requis
- **Indépendance vis-à-vis du protocole** - fonctionne sur HTTP, SMTP, FTP
- **WS-Security** - sécurité au niveau des messages, au-delà de HTTPS
- **Fiabilité** - messagerie robuste avec détection et reprise sur erreur

## Inconvénients {#disadvantages}

- **Implémentation complexe** - nécessite une connaissance approfondie de XML, WSDL et XSD
- **Performances** - plus lent que REST/gRPC en raison du surcoût de traitement XML
- **Consommation de ressources** - surcoût élevé de traitement XML, de bande passante et de charge serveur
- **Peu adapté au mobile** - difficile à mettre en œuvre sur des appareils aux ressources limitées

## Quand l'utiliser {#when-to-use}

- **Opérations financières** - où chaque unité compte et où le coût d'une erreur est élevé
- **Environnements d'entreprise** - contrats d'API liés à des contrats juridiques
- **Systèmes existants** - infrastructure SOAP déjà en place
- **Données structurées en grand volume** - format rigide requis (administrations, systèmes fiscaux)

## Tests avec SoapUI {#testing-with-soapui}

1. Créer un projet SOAP à partir de l'URL du WSDL
2. Créer une TestSuite et des TestCases
3. Ajouter des étapes SOAP Request
4. Configurer les assertions (validation de la réponse, validation du schéma)
5. Exécuter les tests - vert (réussi) ou rouge (échec)

## Pièges courants {#gotchas}

- **HTTP 200 pour les erreurs métier** - SOAP renvoie 200 OK même lorsque l'opération métier échoue. Seules les erreurs de protocole/techniques utilisent des codes 4xx
- **Complexité du WSDL** - les fichiers WSDL peuvent devenir extrêmement volumineux et difficiles à lire. Utilisez des outils, ne les modifiez jamais à la main
- **Verbosité XML** - les messages SOAP sont nettement plus volumineux que leur équivalent JSON, ce qui affecte la bande passante et le temps d'analyse
- **Enfer des espaces de noms** - des déclarations d'espaces de noms incorrectes sont la cause la plus fréquente des erreurs « message rejected »

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - comparaison REST vs SOAP
- [[data-serialization-formats]] - détails sur XML, JSON, XSD
- [[enterprise-integration]] - ESB, patterns d'intégration
