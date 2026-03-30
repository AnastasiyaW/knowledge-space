---
title: Spring MVC
category: concepts
tags: [spring, mvc, controller, rest-api, thymeleaf, request-mapping, model-view]
---
# Spring MVC

## Key Facts

- MVC = Model-View-Controller architecture: separates data, presentation, and request handling
- `@Controller` returns view names (rendered via template engine); `@RestController` returns data directly (JSON/XML)
- Request mapping annotations: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`
- `Model` object passes data from controller to view template; `@ModelAttribute` binds form data to objects
- `@RequestBody` deserializes JSON request body to Java object; `@ResponseBody` serializes response to JSON
- `@PathVariable` extracts URL segments; `@RequestParam` extracts query parameters
- Thymeleaf is the most common template engine for server-side rendering with Spring Boot
- `@Valid` + Bean Validation annotations (`@NotNull`, `@Size`, `@Email`) enable request validation
- `ResponseEntity<T>` gives full control over HTTP status code, headers, and body
- See [[spring-ioc-container]] for how controllers are managed as beans
- See [[spring-security]] for securing endpoints

## Patterns

### REST Controller

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserDto> getAllUsers() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<UserDto> createUser(@Valid @RequestBody CreateUserRequest request) {
        UserDto created = userService.create(request);
        URI location = URI.create("/api/users/" + created.getId());
        return ResponseEntity.created(location).body(created);
    }

    @PutMapping("/{id}")
    public UserDto updateUser(@PathVariable Long id,
                              @Valid @RequestBody UpdateUserRequest request) {
        return userService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

### MVC Controller with Thymeleaf

```java
@Controller
public class MenuController {

    private final MenuService menuService;

    @GetMapping("/menu")
    public String showMenu(Model model) {
        Map<String, List<MenuItem>> sections = menuService.getMenuBySection();
        model.addAttribute("sections", sections);
        return "menu";  // resolves to templates/menu.html
    }

    @GetMapping("/register")
    public String showRegisterForm(Model model) {
        model.addAttribute("user", new UserForm());
        return "register";
    }

    @PostMapping("/register")
    public String registerUser(@ModelAttribute UserForm user, Model model) {
        userService.register(user);
        return "redirect:/login";
    }
}
```

### Thymeleaf template (menu.html)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head><title>Menu</title></head>
<body>
    <div th:each="entry : ${sections}">
        <h2 th:text="${entry.key}">Section</h2>
        <div th:each="item : ${entry.value}">
            <span th:text="${item.name}">Item</span>
            <span th:text="${item.price}">0.00</span>
            <a th:href="@{/order/add(itemId=${item.id})}">Add to Order</a>
        </div>
    </div>
</body>
</html>
```

### Form handling with registration

```html
<form method="post" th:action="@{/register}" th:object="${user}">
    <input type="text" th:field="*{username}" placeholder="Username"/>
    <input type="email" th:field="*{email}" placeholder="Email"/>
    <input type="password" th:field="*{password}" placeholder="Password"/>
    <button type="submit">Register</button>
</form>
```

### Exception handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(UserNotFoundException ex) {
        return new ErrorResponse("NOT_FOUND", ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .toList();
        return new ErrorResponse("VALIDATION_ERROR", errors.toString());
    }
}
```

### Request params and path variables

```java
// /api/products?category=electronics&page=2&size=20
@GetMapping("/api/products")
public Page<Product> search(
    @RequestParam String category,
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size) { }

// /api/users/42/orders/7
@GetMapping("/api/users/{userId}/orders/{orderId}")
public Order getOrder(
    @PathVariable Long userId,
    @PathVariable Long orderId) { }
```

## Gotchas

- **Symptom**: 406 Not Acceptable for REST response -> **Cause**: Missing Jackson dependency on classpath for JSON serialization -> **Fix**: Add `spring-boot-starter-web` (includes Jackson)
- **Symptom**: Form data not binding to object -> **Cause**: Field names in HTML don't match Java object property names -> **Fix**: Use `th:field="*{propertyName}"` in Thymeleaf, or `@RequestParam` names must match
- **Symptom**: Redirect loses model attributes -> **Cause**: `redirect:` creates new request, `Model` is request-scoped -> **Fix**: Use `RedirectAttributes.addFlashAttribute()` for one-time redirect data
- **Symptom**: `@Valid` does nothing -> **Cause**: Missing `spring-boot-starter-validation` dependency -> **Fix**: Add validation starter to pom.xml/build.gradle

## See Also

- [[spring-ioc-container]] - Controllers are Spring beans
- [[spring-security]] - Securing MVC endpoints
- [[spring-data-jpa]] - Repository layer that controllers call
- Spring Docs: [Web MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html)
- Thymeleaf Docs: [Tutorial](https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html)
