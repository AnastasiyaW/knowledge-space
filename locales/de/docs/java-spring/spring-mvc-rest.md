---
title: "Spring-MVC-Controller, REST und Thymeleaf"
category: concepts
tags: [java-spring, spring, mvc, rest, controllers, thymeleaf, i18n]
level: 3
source_sha256: 8add8bd1855174bbbf21a7bcbe3d113a915a731880e93182904dca53017736f5
translation: machine
translated_at: '2026-10-24'
---
# Spring-MVC-Controller, REST und Thymeleaf {#spring-mvc-controllers-rest-and-thymeleaf}

Anfrageverarbeitung in Spring MVC mit `@Controller` und `@RestController`, die Thymeleaf-Template-Engine, Formularverarbeitung, Internationalisierung und das PRG-Muster (Post-Redirect-Get).

## Kernfakten {#key-facts}

- `@Controller` gibt View-Namen (Templates) zurück; `@RestController` gibt Daten (JSON/XML) zurück
- `@GetMapping`, `@PostMapping`, `@PutMapping` und `@DeleteMapping` ordnen HTTP-Methoden Handler-Methoden zu
- Das `Model`-Objekt transportiert Daten vom Controller zur View
- `@ModelAttribute` bindet Formularfelder an ein Objekt
- PRG-Muster: Der POST-Handler leitet per Redirect auf GET weiter, um doppelte Formularübermittlungen zu verhindern
- Thymeleaf-Templates liegen in `src/main/resources/templates/`
- `BindingResult` muss in der Methodensignatur unmittelbar auf den `@Valid`-Parameter folgen

## Muster {#patterns}

### MVC-Controller {#mvc-controller}
```java
@Controller
public class UserController {
    private final UserService userService;

    @GetMapping("/register")
    public String showRegisterForm(Model model) {
        model.addAttribute("user", new UserDto());
        return "register";  // -> templates/register.html
    }

    @PostMapping("/register")
    public String register(@ModelAttribute @Valid UserDto dto,
                           BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "register";  // re-render with errors
        }
        userService.saveUser(dto);
        return "redirect:/login";  // PRG pattern
    }
}
```

### Admin-Panel mit Statusfilter {#admin-panel-with-status-filtering}
```java
@Controller @RequestMapping("/admin")
public class AdminController {
    @GetMapping
    public String showOrders(@RequestParam(required = false) String status,
                              Model model) {
        List<Order> orders = (status != null)
            ? orderService.getByStatus(OrderStatus.valueOf(status))
            : orderService.getByStatus(OrderStatus.NEW);
        model.addAttribute("orders", orders);
        model.addAttribute("statuses", OrderStatus.values());
        return "admin";
    }

    @PostMapping("/update-status")
    public String updateStatus(@RequestParam Long orderId,
                                @RequestParam String newStatus) {
        orderService.updateStatus(orderId, OrderStatus.valueOf(newStatus));
        return "redirect:/admin";
    }
}
```

### Thymeleaf-Ausdrücke {#thymeleaf-expressions}
| Ausdruck | Syntax | Zweck |
|-----------|--------|---------|
| Variable | `${variable}` | Model-Attribute |
| Selektion | `*{field}` | Felder von `th:object` |
| Nachricht | `#{key}` | i18n-Nachschlag für Nachrichten |
| Link | `@{/path}` | URL-Erzeugung |

### Thymeleaf-Formular {#thymeleaf-form}
```html
<form th:action="@{/register}" th:object="${user}" method="post">
    <input type="text" th:field="*{name}" />
    <span th:if="${#fields.hasErrors('name')}"
          th:errors="*{name}" class="error"></span>
    <button type="submit" th:text="#{register.submit}">Submit</button>
</form>
```

### Iteration und Bedingungen {#iteration-and-conditionals}
```html
<div th:each="item : ${menuItems}">
    <span th:text="${item.name}"></span>
    <span th:text="${item.price}"></span>
</div>
<div th:if="${user != null}">Welcome, <span th:text="${user.name}"></span></div>
<div th:unless="${user != null}">Please log in</div>
```

### Internationalisierung (i18n) {#internationalization-i18n}
```properties
# messages_en.properties
register.title=Registration
register.submit=Register

# messages_ru.properties
register.title=Registratsiya
register.submit=Zaregistrirovat'sya
```

```java
@Configuration
public class LocaleConfig implements WebMvcConfigurer {
    @Bean
    public LocaleResolver localeResolver() {
        SessionLocaleResolver r = new SessionLocaleResolver();
        r.setDefaultLocale(new Locale("en"));
        return r;
    }
    @Bean
    public LocaleChangeInterceptor localeInterceptor() {
        LocaleChangeInterceptor i = new LocaleChangeInterceptor();
        i.setParamName("lang");  // switch with ?lang=ru
        return i;
    }
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localeInterceptor());
    }
}
```

### Sitzungsbezogene Daten (Warenkorb) {#session-scoped-data-shopping-cart}
```java
@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionInfo {
    private User currentUser;
    private List<MenuItem> selectedItems = new ArrayList<>();
    private Integer totalPrice = 0;
}
```

## Fallstricke {#gotchas}

- `BindingResult` muss der Parameter unmittelbar nach `@Valid` sein – jede andere Reihenfolge löst eine Exception aus
- `redirect:/path` sendet HTTP 302; die Rückgabe eines View-Namens rendert das Template direkt
- `th:field` setzt die Attribute `name`, `id` und `value` automatisch – sie nicht manuell setzen
- Eine sitzungsbezogene Bean in einem Singleton-Controller erfordert `proxyMode = TARGET_CLASS`
- `@RequestParam(required = false)` mit primitiven Typen verursacht eine NPE – Wrapper-Typen verwenden

## Siehe auch {#see-also}

- [[spring-validation]] – DTO-Validierungsannotationen
- [[spring-ioc-beans]] – Bean-Scopes (session, request)
- [[spring-security]] – Absicherung von Controller-Endpunkten
