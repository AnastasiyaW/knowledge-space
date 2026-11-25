---
title: "Contrôleurs Spring MVC, REST et Thymeleaf"
category: concepts
tags: [java-spring, spring, mvc, rest, controllers, thymeleaf, i18n]
level: 3
source_sha256: 8add8bd1855174bbbf21a7bcbe3d113a915a731880e93182904dca53017736f5
translation: machine
translated_at: '2026-10-24'
---
# Contrôleurs Spring MVC, REST et Thymeleaf {#spring-mvc-controllers-rest-and-thymeleaf}

Traitement des requêtes Spring MVC avec `@Controller` et `@RestController`, moteur de templates Thymeleaf, traitement des formulaires, internationalisation et le pattern PRG (Post-Redirect-Get).

## Points clés {#key-facts}

- `@Controller` retourne des noms de vues (templates) ; `@RestController` retourne des données (JSON/XML)
- `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` associent des méthodes HTTP à des méthodes de traitement
- L'objet `Model` transporte les données du contrôleur vers la vue
- `@ModelAttribute` lie les champs de formulaire à un objet
- Pattern PRG : le handler POST redirige vers un GET pour éviter la soumission en double du formulaire
- Les templates Thymeleaf se trouvent dans `src/main/resources/templates/`
- `BindingResult` doit immédiatement suivre le paramètre `@Valid` dans la signature de la méthode

## Patterns {#patterns}

### Contrôleur MVC {#mvc-controller}
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

### Panneau d'administration avec filtrage par statut {#admin-panel-with-status-filtering}
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

### Expressions Thymeleaf {#thymeleaf-expressions}
| Expression | Syntaxe | Rôle |
|-----------|--------|---------|
| Variable | `${variable}` | Attributs du Model |
| Sélection | `*{field}` | Champs de `th:object` |
| Message | `#{key}` | Recherche de message i18n |
| Lien | `@{/path}` | Génération d'URL |

### Formulaire Thymeleaf {#thymeleaf-form}
```html
<form th:action="@{/register}" th:object="${user}" method="post">
    <input type="text" th:field="*{name}" />
    <span th:if="${#fields.hasErrors('name')}"
          th:errors="*{name}" class="error"></span>
    <button type="submit" th:text="#{register.submit}">Submit</button>
</form>
```

### Itération et conditions {#iteration-and-conditionals}
```html
<div th:each="item : ${menuItems}">
    <span th:text="${item.name}"></span>
    <span th:text="${item.price}"></span>
</div>
<div th:if="${user != null}">Welcome, <span th:text="${user.name}"></span></div>
<div th:unless="${user != null}">Please log in</div>
```

### Internationalisation (i18n) {#internationalization-i18n}
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

### Données de session (panier d'achat) {#session-scoped-data-shopping-cart}
```java
@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionInfo {
    private User currentUser;
    private List<MenuItem> selectedItems = new ArrayList<>();
    private Integer totalPrice = 0;
}
```

## Pièges {#gotchas}

- `BindingResult` doit être le paramètre immédiatement après `@Valid` : tout autre ordre lève une exception
- `redirect:/path` envoie une réponse HTTP 302 ; retourner un nom de vue affiche directement le template
- `th:field` définit automatiquement les attributs `name`, `id` et `value` : ne les définissez pas manuellement
- Un bean à portée session utilisé dans un contrôleur singleton nécessite `proxyMode = TARGET_CLASS`
- `@RequestParam(required = false)` avec des types primitifs provoque une NPE : utilisez les types enveloppes

## Voir aussi {#see-also}

- [[spring-validation]] - Annotations de validation des DTO
- [[spring-ioc-beans]] - Portées des beans (session, requête)
- [[spring-security]] - Sécurisation des endpoints des contrôleurs
