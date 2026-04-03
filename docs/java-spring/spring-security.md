---
title: Spring Security - Authentication and Authorization
category: concepts
tags: [java-spring, spring, security, authentication, authorization, bcrypt, session]
---

# Spring Security - Authentication and Authorization

Spring Security framework covering password encoding with BCrypt, SecurityFilterChain configuration, role-based access control, session management, and UserDetailsService integration.

## Key Facts

- Adding `spring-boot-starter-security` auto-secures all endpoints with a login form
- Default: username `user`, auto-generated password printed to console
- BCrypt generates different hashes for the same input (random salt embedded in hash)
- Always use `encoder.matches(raw, encoded)`, never compare hashes with `equals()`
- CSRF protection enabled by default
- `SecurityFilterChain` is the modern way to configure security (replacing `WebSecurityConfigurerAdapter`)

## Patterns

### BCrypt Password Encoding
```java
@Configuration
public class SecurityConfig {
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}

// Registration: encode before saving
String encoded = passwordEncoder.encode(dto.getPassword());

// Login: match raw against stored hash
boolean valid = passwordEncoder.matches(rawPassword, storedHash);
```

### SecurityFilterChain (Modern Configuration)
```java
@Configuration @EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/register", "/login", "/css/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/menu")
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/login")
            );
        return http.build();
    }
}
```

### UserDetailsService
```java
@Bean
public UserDetailsService userDetailsService(UserRepo userRepo) {
    return email -> {
        User user = userRepo.getUserByEmail(email);
        if (user == null) throw new UsernameNotFoundException(email);
        return org.springframework.security.core.userdetails.User
            .withUsername(user.getEmail())
            .password(user.getPassword())
            .roles("USER")
            .build();
    };
}
```

### Manual Session-Based Authentication
```java
@PostMapping("/login")
public String login(@ModelAttribute UserDto dto, HttpSession session, Model model) {
    User user = userService.getUserByEmail(dto.getEmail());
    if (user != null && passwordEncoder.matches(dto.getPassword(), user.getPassword())) {
        session.setAttribute("currentUser", user);
        return "redirect:/menu";
    }
    model.addAttribute("error", "Invalid credentials");
    return "login";
}
```

## Gotchas

- Never store passwords in plain text - always use BCryptPasswordEncoder or Argon2
- BCrypt `matches()` extracts salt from the stored hash - that's why different hashes for same input still match
- `requestMatchers` order matters - more specific rules first, `anyRequest()` last
- CSRF token required for POST forms with Thymeleaf (auto-included); disable for REST APIs if using token auth
- `@PreAuthorize("hasRole('ADMIN')")` requires `@EnableMethodSecurity` on configuration class

## See Also

- [[spring-mvc-rest]] - Controllers that security protects
- [[spring-ioc-beans]] - Security beans and configuration
- [[spring-validation]] - Input validation as security layer
