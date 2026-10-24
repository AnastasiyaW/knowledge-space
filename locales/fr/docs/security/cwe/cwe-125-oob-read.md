---
description: "CWE-125 : Lecture hors limites - les lectures au-delà des bornes d'un tampon divulguent des secrets, des clés et le contenu adjacent du tas. Archétype de Heartbleed. La détection reprend celle du CWE-787 dans les contextes de lecture."
date: 2026-04-16
tags: [security, cwe, memory-corruption, information-disclosure, c, cpp, heartbleed]
level: Advanced
source_sha256: cf9c8c46bb4a2c50cbc6260b374edd8841d4a2d2ec216a0c094a40afdf2ea7a0
translation: machine
translated_at: '2026-10-24'
---
# CWE-125 : Lecture hors limites {#cwe-125-out-of-bounds-read}

**Rang dans le CWE Top 25 :** 6 (2024).
**Impact principal :** divulgation d'informations (secrets, clés, contenu adjacent du tas ou de la pile). Impact secondaire : plantage et déni de service.
**Distinction clé avec [[cwe-787-oob-write]] :** les lectures ne corrompent pas l'état du processus ; elles renvoient silencieusement des octets provenant de la mémoire adjacente. Le processus continue de s'exécuter normalement tout en divulguant des données.

---

## Sémantique fonctionnelle {#functional-semantics}

Une opération de lecture accède à la mémoire à l'adresse `base + offset` où `offset >= allocated_size`. Le CPU récupère des octets dans les régions mémoire adjacentes (une autre allocation, un cadre de pile, une région mappée) et les renvoie comme s'ils faisaient partie du tampon prévu. Aucune exception ne se produit, sauf si l'adresse franchit la frontière d'une page non mappée.

**Ce qui se trouve à côté d'une allocation sur le tas :**
- d'autres allocations vivantes (contenant des mots de passe, des clés, des jetons, des données personnelles)
- de la mémoire libérée (pouvant contenir d'anciennes données sensibles non effacées)
- les métadonnées de l'allocateur (en-têtes de blocs contenant des pointeurs, utiles pour contourner l'ASLR)
- des pages de garde (provoquent un plantage - SIGBUS/SIGSEGV - détectable)

**Ce qui se trouve à côté d'un tampon sur la pile :**
- d'autres variables locales de la même fonction
- les registres sauvegardés (RBP, RBX, R12-R15)
- l'adresse de retour (la divulguer permet de contourner l'ASLR/PIE)
- le cadre de pile de l'appelant (permet de divulguer les valeurs de canari)

---

## Heartbleed : l'étude de cas canonique du CWE-125 {#heartbleed-the-canonical-cwe-125-case-study}

CVE-2014-0160. OpenSSL 1.0.1 à 1.0.1f. CVSS 7.5.

```c
// OpenSSL tls1_process_heartbeat() - simplified
int tls1_process_heartbeat(SSL *s) {
    unsigned char *p = &s->s3->rrec.data[0];
    unsigned int payload;

    // Read payload length from the TLS record (attacker-controlled)
    n2s(p, payload);   // reads 2 bytes from network, assigns to payload
                       // attacker sends: type=heartbeat, length=65535, actual_data=1_byte

    // Allocate response buffer
    unsigned char *buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    unsigned char *bp = buffer;

    // Copy payload bytes from request into response - NO bounds check
    memcpy(bp, p, payload);   // copies 65535 bytes from a 1-byte buffer
                              // reads 65534 bytes of adjacent heap memory
    // Send buffer back to client
    ssl3_write_bytes(s, TLS1_RT_HEARTBEAT, buffer, 3 + payload + padding);
}
```

**Correctif :**
```c
// Check actual record length vs claimed payload length
if (1 + 2 + payload + 16 > s->s3->rrec.length) {
    return 0;  // Silently discard malformed heartbeat
}
```

La leçon : le *champ de longueur présent dans les données* et la *longueur réelle des données* sont deux valeurs distinctes. Chaque fois qu'un protocole permet à un client de spécifier la longueur des données qu'il fournit, il faut vérifier la longueur annoncée par rapport à la longueur réellement reçue.

---

## Causes racines {#root-causes}

### 1. Un champ de longueur provenant d'une source non fiable contrôle la taille de la lecture {#1-length-field-from-untrusted-source-controls-read-size}

```c
// VULNERABLE: network-supplied length drives memcpy source
void process_packet(const uint8_t *pkt, size_t pkt_len) {
    uint16_t claimed_len = *(uint16_t *)(pkt + 2);  // from packet header
    uint8_t *data_section = pkt + 4;

    uint8_t response[256];
    memcpy(response, data_section, claimed_len);     // reads claimed_len bytes
    // if claimed_len > pkt_len - 4: reads past end of pkt into adjacent memory
}
```

```c
// FIXED: clamp to actual available bytes
void process_packet(const uint8_t *pkt, size_t pkt_len) {
    if (pkt_len < 4) return;
    uint16_t claimed_len = *(uint16_t *)(pkt + 2);
    size_t available = pkt_len - 4;
    size_t read_len = (claimed_len < available) ? claimed_len : available;

    uint8_t response[256];
    if (read_len > sizeof(response)) return;
    memcpy(response, pkt + 4, read_len);
}
```

### 2. Confusion de signe dans le calcul d'indice {#2-signedness-confusion-in-index-computation}

```c
// VULNERABLE: signed index, negative wraps to huge positive
char lookup_table[256];

char get_char(int8_t user_input) {
    // user_input = -1 → (int8_t)(-1) = 255 as unsigned, but...
    // user_input = -128 → index becomes 128 + huge_offset in some contexts
    return lookup_table[(unsigned char)user_input];  // seems safe
}

// More dangerous pattern:
char get_at_offset(char *buf, size_t buf_size, int offset) {
    if (offset < buf_size) {          // offset=-1 passes this check (signed < unsigned)
        return buf[offset];           // buf[-1] reads before the buffer
    }
    return 0;
}
```

```c
// FIXED: explicit sign check
char get_at_offset(char *buf, size_t buf_size, int offset) {
    if (offset < 0 || (size_t)offset >= buf_size) return 0;
    return buf[offset];
}
```

### 3. Opération sur chaîne sans limite de longueur {#3-string-operation-without-length-limit}

```c
// VULNERABLE: reads past end of non-null-terminated buffer
void log_field(const char *data, size_t data_len) {
    char field[128];
    strncpy(field, data, sizeof(field));   // may not null-terminate if data_len >= 128
    printf("Field: %s\n", field);           // printf reads until null - past field boundary
}
```

```c
// FIXED: explicit null-termination
void log_field(const char *data, size_t data_len) {
    char field[128];
    size_t copy_len = (data_len < sizeof(field) - 1) ? data_len : sizeof(field) - 1;
    memcpy(field, data, copy_len);
    field[copy_len] = '\0';   // explicit null termination
    printf("Field: %s\n", field);
}
```

### 4. Lecture excessive due à une chaîne de format {#4-format-string-over-read}

```c
// VULNERABLE: format string from user causes OOB reads of stack
void log_request(const char *user_fmt) {
    printf(user_fmt);   // %s %s %s reads stack values as pointers, then dereferences them
                        // %x %x %x leaks stack values as hex integers
}
```

```c
// FIXED: never use user data as format string
void log_request(const char *user_input) {
    printf("%s", user_input);  // user_input is a value, not a format specifier
}
```

---

## Taxonomie des fuites d'informations {#information-leakage-taxonomy}

| Zone mémoire lue | Données généralement divulguées | Usage dans une exploitation |
|------------------|---------------------------------|-----------------------------|
| Bloc adjacent du tas | Chaînes, clés, jetons dans les allocations vivantes | Vol direct d'identifiants |
| Bloc libéré du tas | Anciennes données sensibles (si non effacées) | Vol d'identifiants historiques |
| Cadre de pile au-dessus de l'appelant | Variables locales des appelants situés plus haut dans la pile d'appels | Matériel cryptographique, pointeurs |
| RIP sauvegardé sur la pile | Adresse de retour (pointeur vers le segment de code) | Contournement de l'ASLR/PIE |
| Canari de pile | Valeur du canari | Contournement de la protection de pile avant une écriture hors limites |
| Métadonnées de l'allocateur du tas | Pointeurs du tas | Contournement de l'ASLR pour le tas ; combiné à une écriture hors limites |
| État de session TLS/SSL | Clés de session, secret maître | Déchiffrement du trafic |

---

## Écosystèmes concernés {#affected-ecosystems}

| Langage | Risque | Remarques |
|---------|--------|-----------|
| C | Critique | `memcpy`, `strcpy`, `printf(%s)` ne disposent d'aucune vérification de bornes intégrée |
| C++ | Critique | Idem que C, plus `std::string::operator[]` (non vérifié) |
| Rust (sûr) | Aucun | Provoque une panique en cas de lecture hors limites d'une tranche |
| Rust (unsafe) | Élevé | `ptr::read` et `slice::from_raw_parts` contournent les vérifications |
| Go | Faible | Bornes des slices vérifiées à l'exécution ; `unsafe.Slice` ne vérifie rien |
| Java | Très faible | Lève `ArrayIndexOutOfBoundsException` au lieu de lire silencieusement |
| Python (extension C) | Moyen | Le code d'extension CPython peut présenter des lectures hors limites |
| WASM | Moyen | La mémoire linéaire est partagée ; les lectures hors limites restent dans la mémoire linéaire |

---

## Heuristiques de détection {#detection-heuristics}

**Motifs à signaler en C/C++ :**

1. `memcpy(dst, src, n)` où `n` provient du même flux de données que `src` - motif Heartbleed. Vérifier `n <= actual_src_len`.
2. `memcpy` / `memmove` avec `n` dérivé d'une entrée externe et sans contrôle préalable `n <= src_allocation_size`.
3. `strlen(buf)` où `buf` n'est pas garanti terminé par un caractère nul (champ de paquet de taille fixe, champ de format de fichier).
4. `printf(user_string)` ou `sprintf(dst, user_string)` sans argument de format - vulnérabilité de chaîne de format (provoque aussi des lectures hors limites).
5. Lecture de tableau `arr[i]` où `i` est déclaré `int` et dérivé d'une entrée externe avec seulement une vérification de borne supérieure (absence de vérification de borne inférieure pour les valeurs négatives).
6. `strncpy(dst, src, n)` suivi de l'utilisation de `dst` comme chaîne C - `strncpy` ne garantit pas la terminaison par un caractère nul.

**Flux de données contaminées :**
- Source : `recv()`, `read()`, `fread()`, `getenv()`, champs du contenu d'un fichier
- Puits : argument source de `memcpy`, argument de format de `printf`, indice de tableau dans une expression de lecture
- Contrôle : existe-t-il une garde `claimed_len <= actual_len` entre la source et le puits ?

**Motif propre aux protocoles :** dès qu'un message de protocole contient à la fois un champ `length` et un champ `data`, vérifier `length <= sizeof(remaining_data)` avant d'utiliser `length` pour piloter une lecture.

---

## Plantage ou fuite silencieuse {#crash-vs-silent-leak}

Une lecture hors limites qui franchit une frontière de page provoque une erreur de segmentation. Elle est ainsi détectable, mais elle révèle aussi la vulnérabilité (déni de service). Une lecture hors limites restant dans la même région mappée réussit silencieusement et renvoie des données parasites à l'appelant, qui les transmet ensuite à l'attaquant.

**Conséquence pour la détection :** AddressSanitizer (`-fsanitize=address`) détecte les lectures hors limites silencieuses qui ne provoqueraient pas de plantage. Valgrind `memcheck` les détecte également. Des tests réguliers sans ASan manqueront les lectures hors limites à l'intérieur d'une page.

---

## Motifs de correction {#fixing-patterns}

| Motif | Application |
|-------|-------------|
| Bornage de la longueur | `actual_len = min(claimed_len, available_bytes)` avant toute copie |
| Validation du protocole | Rejeter les paquets où `header.length > packet.total_bytes - header.size` |
| Terminaison explicite par un caractère nul | Après tout `strncpy` ou `memcpy` de données de chaîne, définir `buf[copy_len] = '\0'` |
| ASan en CI | `-fsanitize=address` détecte les lectures hors limites silencieuses ; exécuter tous les tests sous ASan |
| `__attribute__((format))` | Permet au compilateur de vérifier les appels de la famille `printf` (incohérence format/arguments) |
| Effacement de la mémoire à la libération | `memset(ptr, 0, size); free(ptr)` ou `explicit_bzero()` - réduit l'impact des fuites par lecture après libération |
| Fonctions de chaînes sûres | `strnlen()` au lieu de `strlen()` sur des tampons non fiables |

---

## Pièges - indicateurs de faux positifs {#gotchas-false-positive-indicators}

- **`memcpy(dst, src, sizeof(src))`** où `src` est un tableau de pile de taille fixe - `sizeof` donne une taille connue à la compilation ; c'est sûr tant que `dst` est au moins aussi grand.
- **Arithmétique de pointeurs avec des décalages sûrs connus :** `pkt + 4` lorsqu'un garde `if (pkt_len < 4) return` précède - c'est sûr ; vérifier que toutes les lectures suivantes contrôlent aussi la longueur restante.
- **`strncpy` avec la bonne taille :** `strncpy(dst, src, sizeof(dst))` - sûr pour la copie, mais la sortie peut ne pas être terminée par un caractère nul. Le risque réel réside dans les opérations en aval, `strlen(dst)` ou `printf("%s", dst)`.
- **Faux positifs d'analyse statique dans les boucles :** certains outils signalent `for(i=0; i<n; i++) use(buf[i])` lorsque `n` est un paramètre de fonction. Si l'appelant transmet toujours `n <= actual_buf_len`, c'est sûr. Il faut évaluer la convention d'appel.

---

## Voir aussi {#see-also}

- [[cwe-787-oob-write]] - pendant côté écriture ; souvent associé au CWE-125 (fuite d'une adresse → écriture à l'adresse divulguée)
- CWE-416 : Use After Free - variante de lecture hors limites sur de la mémoire libérée ; un pointeur périmé lit des allocations libérées
- CWE-134 : Chaîne de format non contrôlée - chaîne de format comme déclencheur du CWE-125
- CWE-119 : Erreurs de tampon - CWE parent
- CWE-200 : Exposition d'informations - CWE de conséquence lorsque des données sont divulguées
