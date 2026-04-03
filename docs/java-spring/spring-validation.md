---
title: Spring Validation and DTOs
category: reference
tags: [java-spring, spring, validation, dto, bean-validation, jakarta]
---

# Spring Validation and DTOs

Bean Validation (Jakarta Validation) annotations, DTO pattern for separating domain models from input/output, and validation error handling in controllers and templates.

## Key Facts

- Validation annotations go on DTOs, NOT domain models - keep domain framework-free
- Dependency: `spring-boot-starter-validation`
- `@Valid` on controller parameter triggers validation; `BindingResult` captures errors
- Jakarta Validation (was javax.validation) is the standard, Hibernate Validator is the default implementation
- Custom validators can be created with `@Constraint` and `ConstraintValidator`

## Patterns

### DTO with Validation
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

### Common Validation Annotations
| Annotation | Applies to | Purpose |
|-----------|-----------|---------|
| `@NotBlank` | String | Not null, not empty, not whitespace |
| `@NotNull` | Any | Not null (but can be empty) |
| `@NotEmpty` | String/Collection | Not null and not empty |
| `@Email` | String | Valid email format |
| `@Size(min=, max=)` | String/Collection | Length/size bounds |
| `@Min` / `@Max` | Number | Numeric range |
| `@Digits(integer=, fraction=)` | Number | Digit count |
| `@Pattern(regexp=)` | String | Regex match |
| `@Past` / `@Future` | Date/Time | Temporal constraints |
| `@CreditCardNumber` | String | Luhn algorithm check |

### Controller Validation Flow
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

### Displaying Errors in Thymeleaf
```html
<input type="text" th:field="*{name}" />
<span th:if="${#fields.hasErrors('name')}"
      th:errors="*{name}" class="error"></span>
```

### REST API Validation
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

## Gotchas

- `BindingResult` MUST immediately follow the `@Valid` parameter - placing it elsewhere causes Spring exception
- `@NotBlank` only works on String - use `@NotNull` for other types
- `@Email` allows empty strings - combine with `@NotBlank` for required email
- `@Size` on String counts characters; on Collection counts elements
- Validation messages can use message keys for i18n: `@NotBlank(message = "{user.name.required}")`

## See Also

- [[spring-mvc-rest]] - Controllers that use validation
- [[spring-boot-configuration]] - DTO and domain model separation
- [[spring-security]] - Security-related validation
