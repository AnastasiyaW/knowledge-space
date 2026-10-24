---
description: "CWE-787 : écriture hors limites (Out-of-bounds Write), corruption mémoire par écritures au-delà des bornes d'un tampon. Causes racines, heuristiques de détection, facteurs d'exploitabilité et schémas de correction."
date: 2026-04-16
tags: [security, cwe, memory-corruption, buffer-overflow, c, cpp, rust]
level: Advanced
source_sha256: 13a326398df3cff31ce6d13423735f18bdb93338fdbfc28898f31505fdf40f17
translation: machine
translated_at: '2026-10-24'
---
# CWE-787 : écriture hors limites (Out-of-bounds Write) {#cwe-787-out-of-bounds-write}

**Classement CWE Top 25 :** 2 (2024). Figure constamment dans le top 3 depuis 2019.
**Profil CVSS :** généralement entre 7.5 et 10.0. Une écriture hors limites sur le tas constitue une primitive d'exécution de code dans les exploits modernes.

---

## Sémantique fonctionnelle {#functional-semantics}

Une opération d'écriture cible l'adresse mémoire `base + offset` où `offset >= allocated_size`. L'écriture atterrit dans la mémoire adjacente : les métadonnées d'un autre bloc du tas, l'adresse de retour d'une trame de pile ou une variable globale. La sémantique est la suivante : le programme croit écrire dans ses propres données, le CPU exécute l'écriture sans lever de faute, et l'état du processus est corrompu silencieusement.

Il s'agit d'un phénomène distinct d'une faute de segmentation (segfault), qui ne survient que lorsque l'adresse cible n'est pas mappée. Les écritures hors limites à l'intérieur d'une même zone d'allocation réussissent silencieusement.

**Chaîne de conséquences :**
```text
OOB write → corrupt adjacent data
           → if metadata (heap chunk header): heap corruption → malloc/free crash or controlled allocation
           → if return address (stack): control flow hijack
           → if vtable pointer: type confusion → arbitrary virtual dispatch
           → if adjacent buffer: data corruption, logic errors, secondary vulnerabilities
```

---

## Causes racines {#root-causes}

### 1. Erreur de un (off-by-one) dans les bornes de boucle {#1-off-by-one-in-loop-bounds}

```c
// VULNERABLE: writes index n into buffer of size n
void copy_path(char *dst, const char *src, size_t n) {
    size_t i;
    for (i = 0; i <= n; i++) {   // <= should be <
        dst[i] = src[i];
    }
}
```

`dst[n]` écrit un octet au-delà de l'allocation. Sur la pile, cela écrase la variable locale suivante ou le pointeur de trame sauvegardé.

```c
// FIXED
void copy_path(char *dst, const char *src, size_t n) {
    size_t i;
    for (i = 0; i < n; i++) {
        dst[i] = src[i];
    }
    dst[n - 1] = '\0';  // explicit null termination within bounds
}
```

### 2. Dépassement d'entier dans le calcul de taille {#2-integer-overflow-in-size-calculation}

```c
// VULNERABLE: attacker controls nmemb and size
void *make_grid(size_t nmemb, size_t size) {
    void *buf = malloc(nmemb * size);   // overflow if nmemb=0x80000001, size=2 → allocates 2 bytes
    if (!buf) return NULL;
    memset(buf, 0, nmemb * size);       // writes nmemb*size bytes into 2-byte buffer
    return buf;
}
```

```c
// FIXED: use calloc (handles overflow internally) or check explicitly
#include <stdint.h>
void *make_grid(size_t nmemb, size_t size) {
    if (nmemb && size > SIZE_MAX / nmemb) return NULL;  // overflow check
    return calloc(nmemb, size);  // calloc zeroes + checks overflow
}
```

### 3. Copie de chaîne sans borne {#3-unbounded-string-copy}

```c
// VULNERABLE: strcpy/sprintf without length limit
char hostname[64];
void set_hostname(const char *user_input) {
    strcpy(hostname, user_input);   // OOB if input > 63 chars
}
```

```c
// FIXED
void set_hostname(const char *user_input) {
    snprintf(hostname, sizeof(hostname), "%s", user_input);
    // OR: strlcpy(hostname, user_input, sizeof(hostname));
}
```

### 4. Indexation de tranche dans un bloc `unsafe` en Rust {#4-rust-unsafe-slice-indexing}

```rust
// VULNERABLE
unsafe fn write_header(buf: &mut [u8], offset: usize, value: u32) {
    let ptr = buf.as_mut_ptr().add(offset);  // no bounds check
    *(ptr as *mut u32) = value;              // UB if offset + 4 > buf.len()
}
```

```rust
// FIXED: bounds check before unsafe, or use safe API
fn write_header(buf: &mut [u8], offset: usize, value: u32) -> Option<()> {
    buf.get_mut(offset..offset + 4)?
       .copy_from_slice(&value.to_le_bytes());
    Some(())
}
```

---

## Conditions de déclenchement {#trigger-conditions}

| Condition | Mécanisme |
|-----------|-----------|
| Une entrée externe contrôle l'indice du tableau | Injection directe d'indice |
| Une entrée externe contrôle la taille d'allocation | Dépassement d'entier dans `n * sizeof(T)` |
| Une entrée externe contrôle la borne de boucle | Erreur de un via un champ de longueur forgé |
| Champ de longueur fourni par le réseau ou un fichier < données réelles | Écriture au-delà d'une allocation tronquée |
| Non-concordance signé/non signé dans l'indice | Un indice négatif se transforme en grande valeur positive |

**Exemple de non-concordance signé/non signé :**

```c
// VULNERABLE: signed comparison with unsigned loop variable
int8_t index = get_user_index();  // attacker sends -1
if (index < MAX_ITEMS) {           // -1 < 10 → true
    table[index] = value;          // table[-1] = write before array
}
```

---

## Écosystèmes concernés {#affected-ecosystems}

| Langage | Risque | Remarques |
|---------|--------|-----------|
| C | Critique | Aucune vérification de bornes dans la bibliothèque standard par défaut |
| C++ | Critique | `operator[]` de la STL non vérifié ; `.at()` lève une exception mais est rarement utilisé |
| Rust (safe) | Aucun | Provoque un panic à l'exécution en cas de dépassement |
| Rust (unsafe) | Élevé | `ptr::write` et `slice::from_raw_parts_mut` ne effectuent aucune vérification |
| Go | Faible | Panic à l'exécution en cas d'écriture hors tranche ; l'arithmétique sur `unsafe.Pointer` contourne cette protection |
| Java/Python/JS | Très faible | Environnements d'exécution gérés ; un dépassement de tableau lève une exception, sans corruption |
| Assembleur | Critique | Aucune protection à l'exécution |

---

## Heuristiques de détection {#detection-heuristics}

**Motifs à fort signal (à examiner immédiatement) :**

1. `memcpy(dst, src, len)` où `len` provient d'une entrée externe sans garde `len <= sizeof(dst)` immédiatement avant.
2. `strcpy`, `strcat`, `gets`, `sprintf` (sans variantes `n`) : à traiter comme des constats automatiques.
3. Indexation de tableau `arr[i]` où `i` est un `int` ou un `size_t` dérivé d'une source réseau, fichier ou IPC.
4. `malloc(a * b)` ou `malloc(a + b)` où l'un des opérandes est une entrée externe : dépassement possible.
5. Arithmétique de pointeurs : `ptr + offset` où `offset` est externe et il n'existe aucune vérification `ptr + offset < ptr + alloc_size`.
6. `for (i = 0; i <= len; i++)` : erreur de un ; `<=` devrait presque toujours être `<`.

**Points d'ancrage pour l'analyse statique :**
- Taint : source = `read()`, `recv()`, `fread()`, `getenv()`, `argv[]`
- Puits : écriture `memcpy dst`, `strcpy dst`, écriture par indexation de tableau, écriture par déréférencement de pointeur
- Vérification : la donnée contaminée est-elle assainie (bornes vérifiées) sur tous les chemins entre la source et le puits ?

---

## Facteurs d'exploitabilité {#exploitability-factors}

| Facteur | Impact sur l'exploitabilité |
|---------|-----------------------------|
| Débordement sur le tas vs sur la pile | Tas : contournement d'ASLR/PIE nécessaire ; pile : souvent contrôle direct de RIP/EIP |
| Taille de l'écriture | 1 octet (erreur de un) : difficile mais possible (House of Einherjar) ; arbitraire : direct |
| Données adjacentes | En termes de contrôle : métadonnées du tas > pointeur de table virtuelle > adresse de retour |
| ASLR/PIE activés | Augmente la difficulté ; une fuite d'information (CWE-125) est généralement utilisée pour la contourner |
| Canaris de pile | Détecte le débordement de tampon sur la pile avant le retour ; sans effet sur un débordement sur le tas |

---

## Schémas de correction {#fixing-patterns}

| Schéma | Application |
|--------|-------------|
| Utiliser des fonctions bornées par `n` | `strncpy`, `snprintf`, `strncat`, `fgets` à la place des équivalents non bornés |
| `calloc` pour l'allocation de tableaux | Gère la vérification de dépassement de `nmemb * size` selon C11 |
| Vérification explicite de précondition | `assert(offset + len <= buf_size)` ou garde `if` renvoyant une erreur |
| Address Sanitizer (ASan) dans les tests | `-fsanitize=address` détecte les écritures hors limites à l'exécution dans les suites de tests |
| Fortify Source | `-D_FORTIFY_SOURCE=2` ajoute des vérifications à la compilation et à l'exécution pour les fonctions de chaînes |
| Analyse statique | Coverity, CodeQL `cpp/overflow-buffer`, PVS-Studio V531, Semgrep `c.lang.security.buffer-not-null-terminated` |
| Wrappers sûrs | `strlcpy`/`strlcat` (OpenBSD), `memcpy_s` (C11 Annexe K) |

---

## Pièges : indicateurs de faux positifs {#gotchas-false-positive-indicators}

- **Modulo de tampon circulaire :** `buf[i % SIZE]` est toujours dans les bornes si `SIZE` correspond à `sizeof(buf)/sizeof(buf[0])`. Vérifier que le modulo correspond exactement à la taille de l'allocation.
- **Copie terminée par sentinelle :** `while (*src) dst[i++] = *src++;` paraît dangereux, mais l'appelant peut garantir `strlen(src) < sizeof(dst)`. Vérifier le contrat au site d'appel.
- **Variable locale de taille connue sur la pile avec garde sizeof :** `memcpy(local, src, sizeof(local))` où `local` est un tableau fixe sur la pile est sûr ; `sizeof` donne la taille à la compilation.
- **Allocation puis remplissage en deux temps :** `malloc(n)` suivi de `memset(p, 0, n)` avec le même `n` est sûr ; le schéma dangereux courant est celui où le remplissage utilise un `n` *différent* de celui de l'allocation.
- **Taille de tableau insérée par le compilateur :** `-Warray-bounds` de GCC/Clang peut détecter certains cas, mais pas les cas dynamiques ; l'absence d'avertissement ne signifie pas l'absence de bogue.

---

## Voir aussi {#see-also}

- CWE-125 : lecture hors limites (Out-of-Bounds Read) : pendant en lecture, souvent associé aux bogues de type Heartbleed
- CWE-416 : utilisation après libération (Use After Free) : autre classe de corruption mémoire, souvent enchaînée avec l'écriture hors limites
- CWE-190 : dépassement d'entier (Integer Overflow) : cause racine des écritures hors limites dues au calcul de taille
- CWE-119 : erreurs de tampon (Buffer Errors) : CWE parent
- CWE-121 : débordement de pile (Stack Overflow) : sous-type spécifique à la pile
- CWE-122 : débordement de tas (Heap Overflow) : sous-type spécifique au tas
