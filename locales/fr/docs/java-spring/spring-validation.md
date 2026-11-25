---
title: "Validation Spring et DTO"
category: reference
tags: [java-spring, spring, validation, dto, bean-validation, jakarta]
level: 3
source_sha256: f5eb29dc61b945e2c0584930f55fcd9588facd166cb2b0742c37533b8e04f524
translation: machine
translated_at: '2026-10-24'
---
# Validation Spring et DTO {#spring-validation-and-dtos}

Annotations Bean Validation (Jakarta Validation), patron DTO pour séparer les modèles de domaine des entrées/sorties, et gestion des erreurs de validation dans les contrôleurs et les templates.

## Points clés {#key-facts}

- Les annotations de validation se placent sur les DTO, PAS sur les modèles de domaine : le domaine doit rester indépendant du framework
- Dépendance : `spring-boot-starter-validation`
- `@Valid` sur un paramètre de contrôleur déclenche la validation ; `BindingResult` capture les erreurs
- Jakarta Validation (anciennement javax.validation) est le standard, Hibernate Validator en est l'implémentation par défaut
- Des validateurs personnalisés peuvent être créés avec `@Constraint` et `ConstraintValidator`

## Patterns {#patterns}

### DTO avec validation {#dto-with-validation}
```java
public class UserDto {
    @NotBlank(message = "Name is required")
    private String name;

    @NotBlank @Email(message = "Email should be valid")
    private String email;

    @NotBlank @Size(min = 6, message = "Password must be at least 6 chars")
    private String password;

    @NotBlank @Pattern(regexp = "^[+]?[0-9]{9,12}$", message = "Invalid phone")
    private String phone;

    @NotBlank @Size(min = 7, message = "Address too short")
    private String address;
}
```

### Annotations de validation courantes {#common-validation-annotations}
| Annotation | S'applique à | Rôle |
|-----------|-----------|---------|
| `@NotBlank` | String | Non nul, non vide, sans espaces uniquement |
| `@NotNull` | Tout | Non nul (mais peut être vide) |
| `@NotEmpty` | String/Collection | Non nul et non vide |
| `@Email` | String | Format d'e-mail valide |
| `@Size(min=, max=)` | String/Collection | Bornes de longueur/taille |
| `@Min` / `@Max` | Nombre | Plage numérique |
| `@Digits(integer=, fraction=)` | Nombre | Nombre de chiffres |
| `@Pattern(regexp=)` | String | Correspondance avec une expression régulière |
| `@Past` / `@Future` | Date/Heure | Contraintes temporelles |
| `@CreditCardNumber` | String | Vérification par algorithme de Luhn |

### Flux de validation dans le contrôleur {#controller-validation-flow}
```java
@PostMapping("/register")
public String register(@ModelAttribute @Valid UserDto dto,
                        BindingResult result, Model model) {
    if (result.hasErrors()) {
        return "register";  // re-render form with errors
    }
    userService.saveUser(dto);
    return "redirect:/login";
}
```

### Affichage des erreurs dans Thymeleaf {#displaying-errors-in-thymeleaf}
```html
<input type="text" th:field="*{name}" />
<span th:if="${#fields.hasErrors('name')}"
      th:errors="*{name}" class="error"></span>
```

### Validation d'une API REST {#rest-api-validation}
```java
@RestController
public class UserApiController {
    @PostMapping("/api/users")
    public ResponseEntity<?> create(@RequestBody @Valid UserDto dto) {
        // If validation fails, Spring returns 400 with error details
        return ResponseEntity.ok(userService.create(dto));
    }
}
```

## Pièges {#gotchas}

- `BindingResult` DOIT suivre immédiatement le paramètre `@Valid` : le placer ailleurs provoque une exception Spring
- `@NotBlank` ne fonctionne que sur les String : utilisez `@NotNull` pour les autres types
- `@Email` accepte les chaînes vides : combinez-le avec `@NotBlank` pour un e-mail obligatoire
- `@Size` sur une String compte les caractères ; sur une Collection, il compte les éléments
- Les messages de validation peuvent utiliser des clés de message pour l'i18n : `@NotBlank(message = "{user.name.required}")`

## Voir aussi {#see-also}

- [[spring-mvc-rest]] - Contrôleurs qui utilisent la validation
- [[spring-boot-configuration]] - Séparation entre DTO et modèle de domaine
- [[spring-security]] - Validation liée à la sécurité
