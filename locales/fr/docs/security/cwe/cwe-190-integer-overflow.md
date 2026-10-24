---
description: "CWE-190 : l'arithmétique produit un résultat hors plage, avec rebouclage ou troncature. Conduit à une allocation de tampon sous-dimensionnée, au contournement de contrôles de sécurité et à une corruption mémoire."
date: 2026-04-16
tags: [security, cwe, integer-overflow, buffer-overflow, c, cpp, go, java, rust, memory-safety]
level: Advanced
source_sha256: e10946a8eab72d3863c2828da5a9668701d94e38f4bb7ca0e0c6c72162f47b99
translation: machine
translated_at: '2026-10-24'
---
# CWE-190 : Dépassement d'entier ou rebouclage (Integer Overflow or Wraparound) {#cwe-190-integer-overflow-or-wraparound}

**CWE-190** | Plage du score de base CVSS : 5.9-9.8 (lorsqu'il conduit à une corruption du tas) | Rang 23 du CWE Top 25

## Sémantique fonctionnelle {#functional-semantics}

Un dépassement d'entier se produit lorsqu'une opération arithmétique produit un résultat mathématique qui ne peut pas être représenté dans le type entier cible. La valeur stockée reboucle (non signé), est indéfinie (C/C++ signé) ou saturée (selon le matériel). La valeur corrompue se propage ensuite vers des opérations sensibles pour la sécurité : tailles d'allocation mémoire, calculs d'indices de tableau, bornes de boucles et comparaisons de seuils de sécurité. La conséquence directe n'est généralement pas exploitable ; la condition exploitable apparaît lorsque la valeur rebouclée est utilisée comme taille (CWE-131/CWE-787), comme indice (CWE-129) ou comme point de contrôle de sécurité (contrôle contourné).

## Cause racine {#root-cause}

Les types entiers ont une largeur de bits fixe. Aucun mécanisme de détection de dépassement n'existe par défaut au niveau du langage en C, C++, Go ou Java. Le programmeur suppose que les résultats arithmétiques restent dans la plage ; l'attaquant fournit des entrées qui violent cette hypothèse. La vulnérabilité est structurelle : l'opération et son utilisation sont logiquement liées, mais le système de types n'impose pas leur sûreté combinée.

## Taxonomie des dépassements {#overflow-taxonomy}

| Type | Comportement | Langage | Exploitabilité |
|---|---|---|---|
| Dépassement signé | Comportement indéfini (C/C++) — l'optimiseur peut éliminer la vérification | C, C++ | Élevée — le comportement indéfini permet à l'optimiseur de supprimer les vérifications de bornes |
| Rebouclage non signé | Bien défini : `(UINT_MAX + 1) → 0` | C, C++, Go | Élevée — prévisible, souvent exploité |
| Troncature d'entier | Perte des bits de poids fort lors d'un cast réducteur : `(uint8_t)256 → 0` | Tous | Élevée — survient souvent lors d'un cast de paramètre de fonction |
| Dépassement de multiplication | `size_t count * size_t element_size` reboucle vers une petite valeur | C, C++ | Élevée — allocation de tas sous-dimensionnée classique |
| Comparaison signé/non signé | Un négatif signé comparé comme un grand positif non signé | C, C++ | Moyenne — contourne les contrôles `< MAX_SIZE` |

## Conditions de déclenchement {#trigger-conditions}

- L'utilisateur contrôle une valeur utilisée dans : `malloc(n)`, `new T[n]`, un indice de tableau `arr[n]`, `memcpy(dst, src, n)`, une borne de boucle `for(i=0; i<n; i++)`
- Une arithmétique est effectuée sur une entrée utilisateur avant l'usage sensible pour la sécurité : `malloc(user_count * element_size)`
- Cast réducteur d'un type large vers un type plus étroit : `int n = (int) user_supplied_size_t`
- Une comparaison mélange signé et non signé : `if (user_int < MAX_UNSIGNED)` où `user_int` est signé

## Comportement spécifique aux langages {#language-specific-behavior}

| Langage | Dépassement signé | Dépassement non signé | Cast réducteur | Vérification intégrée |
|---|---|---|---|---|
| C | **Comportement indéfini** (UB) | Rebouclage (défini) | Dépend de l'implémentation | Option `-ftrapv` (coût en performance) |
| C++ | **Comportement indéfini** | Rebouclage (défini) | Dépend de l'implémentation | `-fsanitize=integer` (AddressSanitizer) |
| Go | Rebouclage (défini) | Rebouclage (défini) | Tronque, sans panique | Aucune ; `math/bits.Add` pour des opérations sûres vis-à-vis du dépassement |
| Java | Rebouclage (défini) | N/A (pas de non signé) | `(int) longValue` tronque silencieusement | `Math.addExact()` lève `ArithmeticException` |
| Rust | Panique en debug, **rebouclage en release** | Idem | Erreur de compilation (cast explicite requis) | `checked_add()`, `saturating_add()`, `wrapping_add()` |
| Python | Entiers à précision arbitraire — pas de dépassement | Pas de dépassement | N/A | N/A — immunisé |

## Motifs vulnérables {#vulnerable-patterns}

### C — dépassement de multiplication dans l'allocation {#c-multiplication-overflow-in-allocation}

```c
// VULNERABLE: count=65537, size=65536 → 65537*65536 = 4,295,032,832
// On 32-bit: wraps to 65536 — allocates 64KB instead of 4GB
// memcpy then writes 4GB into 64KB buffer → heap overflow
void process_records(size_t count, size_t record_size, const char *src) {
    char *buf = malloc(count * record_size); // OVERFLOW: no check
    if (!buf) return;
    memcpy(buf, src, count * record_size);   // writes to undersized buffer
    free(buf);
}
```

### C — dépassement signé dans une boucle (UB → l'optimiseur supprime la vérification) {#c-signed-overflow-in-loop-ub-optimizer-removes-check}

```c
// VULNERABLE: signed integer overflow is UB in C
// Compiler may optimize: since i+1 > i is always true (no UB assumed),
// the loop continuation check may be removed entirely
int i;
for (i = 0; i <= INT_MAX; i++) { // compiler may prove i <= INT_MAX always, infinite loop or skip
    process(buf[i]);
}
```

### Java — troncature silencieuse d'un int lors d'une multiplication de long {#java-silent-int-truncation-on-long-multiplication}

```java
// VULNERABLE: count * PAGE_SIZE overflows int if count > 2^21 (page size = 1024)
public byte[] allocateBuffer(int count, int pageSize) {
    int totalSize = count * pageSize; // wraps negative if > Integer.MAX_VALUE
    return new byte[totalSize]; // NegativeArraySizeException or undersized
}

// Example: count=2097153, pageSize=1024 → 2097153*1024 = 2,147,484,672 > INT_MAX
// Actual stored value: -2146482624 → NegativeArraySizeException → DoS
```

### Go — rebouclage silencieux, sans panique {#go-silent-wraparound-no-panic}

```go
// VULNERABLE: Go integers wrap silently in all builds
func allocate(count, size int) []byte {
    total := count * size // wraps if count*size > MaxInt64
    return make([]byte, total) // panic: runtime: out of memory (if large) or undersized alloc
}

// More insidious: security bypass
func checkQuota(used, delta int64) bool {
    newUsed := used + delta // if delta is negative: used + large_negative = bypasses quota
    return newUsed <= QUOTA_MAX // attacker passes negative delta
}
```

## Motifs corrigés {#fixed-patterns}

### C — multiplication sûre avec vérification de dépassement {#c-safe-multiplication-with-overflow-check}

```c
#include <stdint.h>
#include <stddef.h>

// Method 1: __builtin_mul_overflow (GCC/Clang)
void process_records_safe(size_t count, size_t record_size, const char *src) {
    size_t total;
    if (__builtin_mul_overflow(count, record_size, &total)) {
        return; // overflow detected, reject
    }
    char *buf = malloc(total);
    if (!buf) return;
    memcpy(buf, src, total);
    free(buf);
}

// Method 2: pre-division check (portable C99)
void process_records_safe_v2(size_t count, size_t record_size, const char *src) {
    if (count > 0 && record_size > SIZE_MAX / count) {
        return; // would overflow
    }
    char *buf = malloc(count * record_size);
    if (!buf) return;
    memcpy(buf, src, count * record_size);
    free(buf);
}
```

### Java — Math.addExact / multiplyExact {#java-mathaddexact-multiplyexact}

```java
// FIXED: Math.multiplyExact throws ArithmeticException on overflow
public byte[] allocateBuffer(int count, int pageSize) {
    try {
        int totalSize = Math.multiplyExact(count, pageSize);
        if (totalSize > MAX_ALLOWED_SIZE) throw new IllegalArgumentException("Too large");
        return new byte[totalSize];
    } catch (ArithmeticException e) {
        throw new IllegalArgumentException("Buffer size overflow", e);
    }
}

// Alternative: promote to long before multiply, check, then cast
public byte[] allocateBuffer2(long count, long pageSize) {
    long totalSize = count * pageSize; // long multiplication — overflow at 2^63
    if (totalSize < 0 || totalSize > Integer.MAX_VALUE || totalSize > MAX_ALLOWED_SIZE) {
        throw new IllegalArgumentException("Invalid size");
    }
    return new byte[(int) totalSize];
}
```

### Rust — arithmétique contrôlée (gestion explicite du dépassement) {#rust-checked-arithmetic-explicit-overflow-handling}

```rust
// VULNERABLE in release builds (wraps silently):
fn allocate(count: usize, size: usize) -> Vec<u8> {
    vec![0u8; count * size] // wraps in release, panics in debug
}

// FIXED: checked_mul returns None on overflow
fn allocate_safe(count: usize, size: usize) -> Result<Vec<u8>, &'static str> {
    let total = count.checked_mul(size).ok_or("size overflow")?;
    if total > MAX_ALLOCATION {
        return Err("allocation too large");
    }
    Ok(vec![0u8; total])
}

// For financial: saturating_add prevents wraparound, caps at MAX
fn add_to_balance(balance: u64, amount: u64) -> u64 {
    balance.saturating_add(amount) // returns u64::MAX instead of wrapping
}
```

### Go — pré-vérification explicite du dépassement {#go-explicit-overflow-pre-check}

```go
import "math"

// FIXED: check before multiply
func allocateSafe(count, size int) ([]byte, error) {
    if count > 0 && size > math.MaxInt/count {
        return nil, fmt.Errorf("allocation overflow: count=%d size=%d", count, size)
    }
    total := count * size
    if total > MaxAllocationSize {
        return nil, fmt.Errorf("allocation too large: %d", total)
    }
    return make([]byte, total), nil
}
```

## Heuristiques de détection {#detection-heuristics}

**Déclencheurs d'analyse statique :**
- `malloc(a * b)` ou `calloc(a, b)` où `a` ou `b` dérive d'une entrée utilisateur sans vérification préalable de dépassement
- `new T[user_value]` ou `make([]T, user_value)` sans contrôle de bornes
- Arithmétique sur des valeurs contrôlées par l'utilisateur précédant un indice de tableau : `arr[user_a + user_b]`
- Cast réducteur d'une valeur fournie par l'utilisateur : `(int)userLong`, `(uint8_t)userInt`, `(short)userInt`
- Comparaison signé/non signé mixte : `if (signed_var < unsigned_constant)` — la promotion implicite peut inverser la logique
- Java : `int result = (int)(userLong * constant)` sans `Math.multiplyExact`

**Déclencheurs par conséquence :**
- Allocation sous-dimensionnée : résultat arithmétique utilisé comme taille d'allocation
- Dépassement de bornes d'indice : résultat arithmétique utilisé comme indice de tableau
- Contournement de contrôle de sécurité : résultat arithmétique utilisé dans `if (value < threshold)` ou `if (value == expected)`
- Calcul financier : arithmétique sur des valeurs monétaires où des résultats négatifs sont possibles

**Indicateurs de faux positifs :**
- Multiplication dont les deux opérandes sont des constantes de compilation ou des valeurs d'énumération aux plages connues
- Valeur fournie par l'utilisateur déjà validée par rapport au maximum avant l'arithmétique : `if (n > 1000) return error; buf = malloc(n * 8);` — sûr si `1000 * 8 < SIZE_MAX`
- Code Rust utilisant volontairement `wrapping_add`/`wrapping_mul` (par exemple fonctions de hachage, sommes de contrôle) — le rebouclage sémantique est le comportement attendu
- Code Go opérant sur des valeurs bornées par une validation préalable

## Mesures de mitigation du compilateur {#compiler-mitigations}

| Mitigation | Effet | Coût |
|---|---|---|
| `-ftrapv` (GCC/Clang) | Déclenche un trap sur dépassement signé à l'exécution | 5-30 % de performance |
| `-fsanitize=integer` (UBSan) | Détecte les opérations entières en comportement indéfini | Uniquement pour les tests |
| `FORTIFY_SOURCE=2` | Renforce les fonctions de la bibliothèque standard (chaînes, mémoire) | Minimal |
| Java `-ea` (assertions) | Active les vérifications d'assertions ; utiliser `assert Math.multiplyExact(a,b) > 0` | Uniquement pour les tests |
| Builds de débogage Rust | Panique en cas de dépassement | Débogage uniquement par défaut |
| `overflow-checks = true` dans Cargo.toml | Panique en cas de dépassement en release | Environ 5-10 % de performance |

## Pièges {#gotchas}

- **Le dépassement signé est un comportement indéfini en C/C++, pas un rebouclage.** Les passes d'optimisation du compilateur (notamment la réduction de force des boucles) exploitent l'hypothèse selon laquelle le dépassement signé ne se produit jamais. Du code comme `if (i + 1 < i) { handle_overflow(); }` peut être entièrement supprimé, car le compilateur suppose que `i + 1 < i` est toujours faux (dépassement signé → UB → condition toujours fausse selon le compilateur). Utiliser `-fwrapv` pour traiter le dépassement signé comme un rebouclage, ou employer une arithmétique non signée avec des vérifications explicites.
- **calloc vs malloc :** `calloc(count, size)` effectue en interne la vérification de dépassement sur la plupart des plateformes. `malloc(count * size)` ne le fait pas. Préférer `calloc` pour les allocations de tableaux en C.
- **La taille de `int` en Go dépend de la plateforme :** `int` fait 32 bits sur les plateformes 32 bits et 64 bits sur les plateformes 64 bits. Du code qui passe les vérifications de dépassement sur des machines de développement 64 bits peut déborder sur des cibles 32 bits ou sur d'anciens appareils ARM.
- **Le mode release de Rust reboucle silencieusement par défaut.** De nombreux développeurs Rust supposent que le dépassement provoque une panique partout, comme en mode debug. Le code Rust critique pour la sécurité doit utiliser les opérations `checked_*` ou activer `overflow-checks = true` dans `Cargo.toml`.
- **Le calcul financier exige une précision arbitraire ou des types décimaux.** `float64` offre 15 à 17 chiffres décimaux significatifs mais accumule des erreurs d'arrondi. Utiliser `big.Int`/`big.Float` en Go, `decimal.Decimal` en Python, `BigDecimal` en Java pour les calculs monétaires. Un dépassement d'entier dans du code financier peut produire des soldes incorrects, et pas seulement des plantages.

## Voir aussi {#see-also}

- CWE-787 : Écriture hors limites (Out Of Bounds Write) — conséquence la plus fréquente d'une allocation sous-dimensionnée due à un dépassement
- CWE-125 : Lecture hors limites (Out Of Bounds Read) — dépassement d'indice conduisant à une lecture au-delà de la fin du tampon
- CWE-369 : Division par zéro (Divide By Zero) — erreur arithmétique apparentée ; diviseur contrôlé par l'attaquant à 0
- CWE-020 : Validation des entrées (Input Validation) — contrôle en amont : valider les plages numériques avant l'arithmétique
