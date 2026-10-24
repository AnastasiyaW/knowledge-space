---
title: "Spring Security - Authentification et autorisation"
category: concepts
tags: [java-spring, spring, security, authentication, authorization, bcrypt, session]
level: 3
source_sha256: 22f5c3958159531ea57c6e232e7e6e7683b2ffeedc30c28716a3c0f3fd56ce5e
translation: machine
translated_at: '2026-10-24'
---
# Spring Security - Authentification et autorisation {#spring-security-authentication-and-authorization}

Framework Spring Security couvrant l'encodage des mots de passe avec BCrypt, la configuration de SecurityFilterChain, le contrôle d'accès basé sur les rôles, la gestion des sessions et l'intégration de UserDetailsService.

## Points clés {#key-facts}

- Ajouter `spring-boot-starter-security` sécurise automatiquement tous les endpoints avec un formulaire de connexion
- Par défaut : nom d'utilisateur `user`, mot de passe généré automatiquement et affiché dans la console
- BCrypt génère des hachages différents pour une même entrée (un sel aléatoire est intégré au hachage)
- Utiliser systématiquement `encoder.matches(raw, encoded)`, ne jamais comparer des hachages avec `equals()`
- Protection CSRF activée par défaut
- `SecurityFilterChain` est la manière moderne de configurer la sécurité (en remplacement de `WebSecurityConfigurerAdapter`)

## Patterns {#patterns}

### Encodage des mots de passe avec BCrypt {#bcrypt-password-encoding}
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

### SecurityFilterChain (configuration moderne) {#securityfilterchain-modern-configuration}
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

### UserDetailsService {#userdetailsservice}
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

### Authentification manuelle basée sur la session {#manual-session-based-authentication}
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

## Pièges à éviter {#gotchas}

- Ne jamais stocker les mots de passe en clair : utiliser systématiquement BCryptPasswordEncoder ou Argon2
- La méthode `matches()` de BCrypt extrait le sel du hachage stocké : c'est pourquoi des hachages différents pour une même entrée correspondent quand même
- L'ordre des `requestMatchers` est important : les règles les plus spécifiques en premier, `anyRequest()` en dernier
- Un jeton CSRF est requis pour les formulaires POST avec Thymeleaf (inclus automatiquement) ; le désactiver pour les API REST si une authentification par jeton est utilisée
- `@PreAuthorize("hasRole('ADMIN')")` nécessite `@EnableMethodSecurity` sur la classe de configuration

## Voir aussi {#see-also}

- [[spring-mvc-rest]] - Contrôleurs protégés par la sécurité
- [[spring-ioc-beans]] - Beans de sécurité et configuration
- [[spring-validation]] - Validation des entrées comme couche de sécurité
