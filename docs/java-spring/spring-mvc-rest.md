---
title: Spring MVC Controllers, REST, and Thymeleaf
category: concepts
tags: [java-spring, spring, mvc, rest, controllers, thymeleaf, i18n]
---

# Spring MVC Controllers, REST, and Thymeleaf

Spring MVC request handling with `@Controller` and `@RestController`, Thymeleaf template engine, form processing, internationalization, and the PRG (Post-Redirect-Get) pattern.

## Key Facts

- `@Controller` returns view names (templates); `@RestController` returns data (JSON/XML)
- `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` map HTTP methods to handler methods
- `Model` object carries data from controller to view
- `@ModelAttribute` binds form fields to an object
- PRG pattern: POST handler redirects to GET to prevent duplicate form submission
- Thymeleaf templates go in `src/main/resources/templates/`
- `BindingResult` must immediately follow `@Valid` parameter in method signature

## Patterns

### MVC Controller
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

### Admin Panel with Status Filtering
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

### Thymeleaf Expressions
| Expression | Syntax | Purpose |
|-----------|--------|---------|
| Variable | `${variable}` | Model attributes |
| Selection | `*{field}` | Fields of `th:object` |
| Message | `#{key}` | i18n message lookup |
| Link | `@{/path}` | URL generation |

### Thymeleaf Form
```html
<form th:action="@{/register}" th:object="${user}" method="post">
    <input type="text" th:field="*{name}" />
    <span th:if="${#fields.hasErrors('name')}"
          th:errors="*{name}" class="error"></span>
    <button type="submit" th:text="#{register.submit}">Submit</button>
</form>
```

### Iteration and Conditionals
```html
<div th:each="item : ${menuItems}">
    <span th:text="${item.name}"></span>
    <span th:text="${item.price}"></span>
</div>
<div th:if="${user != null}">Welcome, <span th:text="${user.name}"></span></div>
<div th:unless="${user != null}">Please log in</div>
```

### Internationalization (i18n)
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

### Session-Scoped Data (Shopping Cart)
```java
@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionInfo {
    private User currentUser;
    private List<MenuItem> selectedItems = new ArrayList<>();
    private Integer totalPrice = 0;
}
```

## Gotchas

- `BindingResult` must be the parameter immediately after `@Valid` - any other order throws exception
- `redirect:/path` sends HTTP 302; returning a view name renders the template directly
- `th:field` automatically sets `name`, `id`, and `value` attributes - don't set them manually
- Session-scoped bean in singleton controller requires `proxyMode = TARGET_CLASS`
- `@RequestParam(required = false)` with primitive types causes NPE - use wrapper types

## See Also

- [[spring-validation]] - DTO validation annotations
- [[spring-ioc-beans]] - Bean scopes (session, request)
- [[spring-security]] - Securing controller endpoints
