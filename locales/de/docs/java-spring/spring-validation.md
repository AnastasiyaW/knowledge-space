---
title: "Spring-Validierung und DTOs"
category: reference
tags: [java-spring, spring, validation, dto, bean-validation, jakarta]
level: 3
source_sha256: f5eb29dc61b945e2c0584930f55fcd9588facd166cb2b0742c37533b8e04f524
translation: machine
translated_at: '2026-10-24'
---
# Spring-Validierung und DTOs {#spring-validation-and-dtos}

Bean-Validation-Annotationen (Jakarta Validation), das DTO-Muster zur Trennung von Domänenmodellen und Ein-/Ausgabe sowie die Behandlung von Validierungsfehlern in Controllern und Templates.

## Wichtige Fakten {#key-facts}

- Validierungsannotationen gehören auf DTOs, NICHT auf Domänenmodelle – das Domänenmodell bleibt frei von Framework-Abhängigkeiten
- Abhängigkeit: `spring-boot-starter-validation`
- `@Valid` an einem Controller-Parameter löst die Validierung aus; `BindingResult` erfasst die Fehler
- Jakarta Validation (vormals javax.validation) ist der Standard, Hibernate Validator ist die Standardimplementierung
- Eigene Validatoren lassen sich mit `@Constraint` und `ConstraintValidator` erstellen

## Muster {#patterns}

### DTO mit Validierung {#dto-with-validation}
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

### Gängige Validierungs-Annotationen {#common-validation-annotations}
| Annotation | Gilt für | Zweck |
|-----------|-----------|---------|
| `@NotBlank` | String | Nicht null, nicht leer, nicht nur Leerzeichen |
| `@NotNull` | Beliebig | Nicht null (darf aber leer sein) |
| `@NotEmpty` | String/Collection | Nicht null und nicht leer |
| `@Email` | String | Gültiges E-Mail-Format |
| `@Size(min=, max=)` | String/Collection | Längen- bzw. Größengrenzen |
| `@Min` / `@Max` | Zahl | Zahlenbereich |
| `@Digits(integer=, fraction=)` | Zahl | Anzahl der Ziffern |
| `@Pattern(regexp=)` | String | Regex-Übereinstimmung |
| `@Past` / `@Future` | Datum/Zeit | Zeitliche Einschränkungen |
| `@CreditCardNumber` | String | Prüfung nach Luhn-Algorithmus |

### Ablauf der Validierung im Controller {#controller-validation-flow}
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

### Fehler in Thymeleaf anzeigen {#displaying-errors-in-thymeleaf}
```html
<input type="text" th:field="*{name}" />
<span th:if="${#fields.hasErrors('name')}"
      th:errors="*{name}" class="error"></span>
```

### Validierung in REST-APIs {#rest-api-validation}
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

## Fallstricke {#gotchas}

- `BindingResult` MUSS unmittelbar auf den `@Valid`-Parameter folgen – an anderer Stelle platziert löst es eine Spring-Exception aus
- `@NotBlank` funktioniert nur für String – für andere Typen `@NotNull` verwenden
- `@Email` akzeptiert leere Strings – für eine Pflicht-E-Mail mit `@NotBlank` kombinieren
- `@Size` zählt bei String Zeichen, bei Collection Elemente
- Validierungsmeldungen können Message-Keys für i18n verwenden: `@NotBlank(message = "{user.name.required}")`

## Siehe auch {#see-also}

- [[spring-mvc-rest]] – Controller, die Validierung verwenden
- [[spring-boot-configuration]] – Trennung von DTO und Domänenmodell
- [[spring-security]] – Sicherheitsbezogene Validierung
