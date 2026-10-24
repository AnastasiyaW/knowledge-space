---
level: 3
source_sha256: 73ec683ba86c71539fe850da09b20d0cb603af76eaf07269c9850d43244a267b
translation: machine
translated_at: '2026-10-24'
---
# Obfuscation du calcul : découpage de l'inférence et architectures à convertisseur {#computation-obfuscation-split-inference-and-converter-architectures}

Date : 2026-04-03
Contexte : produit d'inférence ML pour ordinateur de bureau. Protection de la propriété intellectuelle du modèle en rendant les poids bruts insuffisants pour la piraterie : la sortie nécessite une transformation distincte pour être utilisable.

---

## Problème central {#core-problem}

Chiffrer les poids empêche leur extraction, mais une fois déchiffrés pour l'inférence, le modèle s'exécute dans le processus de l'attaquant. Les approches d'obfuscation du calcul rendent la sortie du modèle elle-même inutilisable sans un second composant que l'attaquant ne contrôle pas.

---

## Variante A : service de conversion local {#variant-a-local-converter-service}

La couche finale du modèle produit un tenseur encodé non RGB (canaux mélangés, transformation affine, combiné par XOR avec une clé). Un processus séparé et signé convertit ce tenseur en image utilisable.

**Architecture :**
```text
ONNX model -> encoded_tensor (not RGB) -> Converter.exe -> JPEG/PNG
```

**Caractéristiques du binaire de conversion :**
- Processus séparé, signature séparée (Authenticode sous Windows, notarisation sous macOS)
- Contient la transformation de décodage, obfusquée (passes LLVM, chiffrement des chaînes)
- Valide périodiquement la licence auprès du serveur de licences ; cesse la conversion en cas d'échec
- Vérifie sa propre intégrité et détecte les débogueurs

**Pile d'obfuscation (C++) :**
```text
LLVM passes:
  - Control Flow Flattening (CFF): state machine replaces conditional branches
  - Bogus Control Flow: dead code inserted with opaque predicates
  - String Encryption: all plaintext constants encrypted, decrypted at runtime
  
Binary protection (post-compile):
  - VMProtect / Themida: wraps critical functions in VM bytecode
  - Custom packer: compresses + encrypts PE/Mach-O sections
  - Anti-debug: TLS callbacks fire before main(), detect and exit
```

**Efficacité : 5/10.** Dès qu'un attaquant a rétro-conçu la transformation à partir d'une version du binaire, toutes les copies précédentes et actuelles sont compromises. La transformation est fixe pour chaque version du modèle. Elle retarde la piraterie occasionnelle de quelques semaines à quelques mois ; les attaquants motivés disposant de compétences en rétro-ingénierie finiront par l'extraire.

**Le versionnement du modèle crée une re-protection naturelle :**
- Chaque mise à jour du modèle modifie le format de sortie, ce qui impose un nouveau convertisseur
- L'ancien convertisseur ne fonctionne plus avec le nouveau binaire du modèle
- La version crackée devient obsolète après un cycle de mise à jour (2 à 4 semaines)

---

## Variante B : inférence découpée (couches côté serveur) {#variant-b-split-inference-server-side-layers}

Les couches critiques s'exécutent sur un serveur distant. Le client ne peut pas terminer l'inférence sans la participation du serveur.

**Stratégies de découpage :**

| Stratégie | Local | Serveur | Taille du tenseur intermédiaire | Surcoût de latence |
|-----------|-------|---------|----------------------------------|--------------------|
| Découpage précoce | encodeur uniquement | traitement principal | Grande (carte de caractéristiques non compressée) | 200-500 ms |
| Découpage tardif | 95 % des couches | 1-2 couches de finalisation | Petite (goulot d'étranglement) | 50-150 ms |
| Découpage intermédiaire | pré + post | couche goulot d'étranglement | Minimale | 50-100 ms |

**Le découpage tardif est préféré** pour les produits orientés bureau : la plupart des calculs restent en local (en exploitant le GPU de l'utilisateur), les données transmises sont minimales, et le serveur ne gère que la finalisation.

```text
Client GPU: layers 0..N-2 -> intermediate_tensor [B, C, H/8, W/8]
HTTP POST /finalize:
  body: {tensor: base64(gzip(intermediate_tensor)), license_token: ...}
  response: {output_tensor: ...}
Client: postprocess + decode output
```

**Points forts :**
- Les couches côté serveur sont physiquement absentes du client : elles ne sont pas « contournables », elles sont littéralement manquantes
- Le serveur peut être mis à jour indépendamment de la distribution du client
- La journalisation côté serveur des usages permet la détection d'anomalies

**Points faibles :**
- **Nécessite une connexion Internet.** Photographes sur le terrain, flux de travail hors ligne, proxys en Chine, en Russie ou en entreprise : tous bloqués.
- Latence : 50 à 200 ms par inférence est perceptible pour des outils interactifs.
- Coût d'infrastructure : inférence GPU côté serveur.
- Point de défaillance unique.

**Efficacité : protection 8/10, expérience utilisateur 4/10** pour un produit orienté bureau qui se veut « fonctionnel sur GPU modeste ».

---

## Variante C : hybride, modèle « amélioration serveur » {#variant-c-hybrid-server-enhancement-model}

Le modèle complet s'exécute en local à qualité standard. 1 à 2 couches d'amélioration sur le serveur produisent une qualité premium. Offre gratuite = local uniquement. Offre payante = local + amélioration serveur.

```text
Local inference -> "good" output (usable, watermarked)
         +
Server enhancement request (paid, requires active license)
         -> "premium" output (higher PSNR, finer detail, no visible watermark)
```

**Freemium par écart de qualité :**
- Les pirates utilisent la version locale : ils reçoivent une sortie « correcte » avec un filigrane visible
- Les utilisateurs payants obtiennent une sortie améliorée par le serveur : nettement meilleure, sans superposition
- Le point d'accès serveur n'est pas accessible sans jeton de licence valide
- Les copies piratées ne peuvent pas accéder au point d'accès premium, même en cas de crack du binaire local

**Exigence sur l'écart de qualité :** si la différence entre la version locale et la version améliorée par le serveur n'est pas visible dans une sortie professionnelle, il n'y a aucune incitation à l'achat. Objectif : gain de 2 à 3 dB de PSNR, ou différence de détail visible à 100 % de zoom sur des images au format d'impression.

**Efficacité : 7/10.** Cela n'empêche pas totalement la piraterie, mais rend le paiement le choix rationnel. Le mode hors ligne fonctionne toujours. En cas de panne du serveur, le produit se dégrade vers « correct » plutôt que vers un échec total.

---

## Matrice de recommandation {#recommendation-matrix}

| Scénario | Variante recommandée |
|----------|----------------------|
| Orienté bureau, hors ligne requis, faible tolérance au coût serveur | A (convertisseur) + C (qualité freemium) |
| Produit cloud d'abord ou API, latence acceptable | B (inférence découpée) |
| SaaS avec offre premium | C (amélioration hybride) |
| Protection maximale de la PI, quelle que soit l'expérience utilisateur | B (inférence découpée) |

**Combinaison pratique pour un produit de bureau :** Variante A comme première couche peu coûteuse (elle retarde 80 % des pirates occasionnels), Variante C pour monétiser les utilisateurs restants qui piratent mais paieraient pour la qualité.

---

## Référence de durcissement des binaires {#binary-hardening-reference}

### Obfuscation LLVM (Ollvm / Hikari / O-MVLL) {#llvm-obfuscation-ollvm-hikari-o-mvll}

```cmake
# CMake: add obfuscation passes via Clang plugin
target_compile_options(converter PRIVATE
  -mllvm -fla          # Control Flow Flattening
  -mllvm -bcf          # Bogus Control Flow
  -mllvm -sub          # Instruction Substitution
  -mllvm -sobf         # String Obfuscation
)
```

**O-MVLL** (commercial, prend en charge Android NDK, iOS, macOS, Windows) :
- Protection basée sur une machine virtuelle : encapsule les fonctions sensibles dans du bytecode interprété
- Trampolines qui déjouent la résolution des symboles
- Obfuscation des constantes : constantes découpées et reconstruites à l'exécution

### Anti-débogage dans un callback TLS (Windows) {#anti-debug-in-tls-callback-windows}

```cpp
// Fires before main() - attacker cannot skip
void NTAPI tls_callback(PVOID, DWORD reason, PVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        if (IsDebuggerPresent()) ExitProcess(0);
        BOOL remote = FALSE;
        CheckRemoteDebuggerPresent(GetCurrentProcess(), &remote);
        if (remote) ExitProcess(0);
    }
}
#pragma comment(linker, "/INCLUDE:_tls_used")
#pragma data_seg(".CRT$XLB")
PIMAGE_TLS_CALLBACK p_tls_callback = tls_callback;
#pragma data_seg()
```

---

## Pièges à éviter {#gotchas}

- **Le craquage du convertisseur ne se fait qu'une fois et se répercute sur tous.** Une fois qu'un cracker a rétro-conçu la transformation de sortie de la version 2.1.3, cette transformation devient publique. Contrairement au chiffrement (clé par utilisateur), la transformation du convertisseur est partagée par toutes les copies. Seules les mises à jour du modèle modifiant le format constituent une défense.
- **VMProtect et Themida ajoutent de la latence au démarrage.** L'initialisation protégée par machine virtuelle peut ajouter 0,5 à 3 secondes au premier lancement. Les utilisateurs le remarquent et le signalent. Profilez et ne protégez que le strict minimum : la vérification de licence et l'extraction de la clé, et non l'ensemble du binaire.
- **Le mode hors ligne est indispensable pour les outils photo professionnels.** La variante B (inférence découpée) contredit fondamentalement l'usage hors ligne. Si votre utilisateur cible est un photographe de mariage en déplacement sans réseau cellulaire, la variante B est inacceptable, quelle que soit la force de la protection.
- **Le point d'accès de l'inférence découpée peut être rejoué.** Si le tenseur intermédiaire n'est pas lié à un jeton de session ou à un nonce, un attaquant peut le capturer et le rejouer contre le serveur. Liez chaque requête d'inférence à un jeton de session signé avec une date d'expiration.
- **Faux positifs des antivirus causés par une obfuscation lourde.** L'aplatissement du flux de contrôle, le chiffrement des chaînes et le packer déclenchent des détections heuristiques dans Windows Defender, Kaspersky et BitDefender. Soumettez le binaire aux éditeurs d'antivirus avant la livraison, ou utilisez une signature de code avec un certificat Extended Validation (EV) pour réduire le taux de faux positifs.

## Voir aussi {#see-also}
- [[output-scrambling-antipiracy]]
- [[remote-kill-switch]]
- [[watermarking-encrypted-models]]
- [[model-weight-encryption]]
- [[licensing-implementation-cpp]]
