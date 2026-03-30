---
title: Spring Security
category: concepts
tags: [spring, security, authentication, authorization, bcrypt, session, csrf]
---
# Spring Security

## Key Facts

- Spring Security handles both **authentication** (who are you?) and **authorization** (what can you do?)
- Adding `spring-boot-starter-security` auto-protects all endpoints - requires login by default
- Passwords must NEVER be stored in plain text - use `BCryptPasswordEncoder` for hashing
- `SecurityFilterChain` bean configures URL-based security rules (replaces deprecated `WebSecurityConfigurerAdapter`)
- Session-based auth: server stores session after login; stateless JWT auth for REST APIs
- CSRF protection is enabled by default for form-based apps; usually disabled for stateless REST APIs
- `@PreAuthorize("hasRole('ADMIN')")` and `@Secured("ROLE_ADMIN")` for method-level authorization
- `UserDetailsService` interface loads user data for authentication from any source (DB, LDAP, etc.)
- Spring Security filter chain intercepts every request before it reaches controllers
- See [[spring-mvc]] for controllers that Spring Security protects
- See [[spring-data-jpa]] for storing user credentials in database

## Patterns

### Security configuration (Spring Boot 3.x)

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity  // enables @PreAuthorize, @Secured
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/", "/register", "/css/**", "/js/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/**").authenticated()
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/menu")
                .permitAll()
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/login?logout")
                .permitAll()
            );

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### UserDetailsService implementation

```java
@Service
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    public CustomUserDetailsService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username)
            throws UsernameNotFoundException {
        UserEntity user = userRepository.findByEmail(username)
            .orElseThrow(() ->
                new UsernameNotFoundException("User not found: " + username));

        return User.builder()
            .username(user.getEmail())
            .password(user.getPassword())  // already BCrypt-hashed
            .roles(user.getRole().name())
            .build();
    }
}
```

### User registration with BCrypt

```java
@Controller
public class RegistrationController {

    private final UserRepository userRepo;
    private final PasswordEncoder encoder;

    @GetMapping("/register")
    public String showForm(Model model) {
        model.addAttribute("user", new RegistrationForm());
        return "register";
    }

    @PostMapping("/register")
    public String register(@Valid @ModelAttribute RegistrationForm form) {
        UserEntity user = new UserEntity();
        user.setEmail(form.getEmail());
        user.setName(form.getName());
        user.setPassword(encoder.encode(form.getPassword())); // HASH!
        user.setRole(UserRole.USER);
        userRepo.save(user);
        return "redirect:/login";
    }
}
```

### REST API with stateless JWT (configuration)

```java
@Configuration
@EnableWebSecurity
public class JwtSecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())  // disable CSRF for REST APIs
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

### Method-level security

```java
@Service
public class AdminService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long id) {
        userRepo.deleteById(id);
    }

    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
    public UserDto getUser(Long userId) {
        return userRepo.findById(userId).map(this::toDto).orElseThrow();
    }

    @PreAuthorize("isAuthenticated()")
    public UserDto getCurrentUser() {
        // get current user from security context
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String email = auth.getName();
        return userRepo.findByEmail(email).map(this::toDto).orElseThrow();
    }
}
```

### Accessing current user in controller

```java
@GetMapping("/profile")
public String profile(@AuthenticationPrincipal UserDetails userDetails, Model model) {
    model.addAttribute("email", userDetails.getUsername());
    model.addAttribute("roles", userDetails.getAuthorities());
    return "profile";
}
```

## Gotchas

- **Symptom**: Password stored as plain text "1234" -> **Cause**: Not using `PasswordEncoder.encode()` at registration -> **Fix**: ALWAYS hash with `BCryptPasswordEncoder` before saving; never store raw passwords
- **Symptom**: 403 Forbidden on POST requests -> **Cause**: CSRF protection rejects forms without CSRF token -> **Fix**: Include `th:action="@{/path}"` in Thymeleaf (auto-adds token), or add `<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>`
- **Symptom**: Infinite redirect loop on login page -> **Cause**: Login page itself requires authentication -> **Fix**: Add `.requestMatchers("/login").permitAll()` in security config
- **Symptom**: `@PreAuthorize` not working -> **Cause**: Missing `@EnableMethodSecurity` on config class -> **Fix**: Add `@EnableMethodSecurity` annotation
- **Symptom**: CORS errors on REST API -> **Cause**: Browser blocks cross-origin requests -> **Fix**: Add `@CrossOrigin` on controllers, or configure `CorsConfigurationSource` bean

## See Also

- [[spring-mvc]] - Controllers protected by security
- [[spring-data-jpa]] - Storing user entities
- [[spring-ioc-container]] - Security beans and filter chain
- Spring Docs: [Spring Security](https://docs.spring.io/spring-security/reference/)
- OWASP: [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
