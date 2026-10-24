---
title: "Spring Security - Authentifizierung und Autorisierung"
category: concepts
tags: [java-spring, spring, security, authentication, authorization, bcrypt, session]
level: 3
source_sha256: 22f5c3958159531ea57c6e232e7e6e7683b2ffeedc30c28716a3c0f3fd56ce5e
translation: machine
translated_at: '2026-10-24'
---
# Spring Security - Authentifizierung und Autorisierung {#spring-security-authentication-and-authorization}

Das Spring-Security-Framework deckt Passwortkodierung mit BCrypt, die Konfiguration der SecurityFilterChain, rollenbasierte Zugriffskontrolle, Sitzungsverwaltung und die Integration des UserDetailsService ab.

## Wichtige Fakten {#key-facts}

- Das Hinzufügen von `spring-boot-starter-security` sichert alle Endpunkte automatisch mit einem Anmeldeformular ab
- Standard: Benutzername `user`, automatisch generiertes Passwort wird auf der Konsole ausgegeben
- BCrypt erzeugt für dieselbe Eingabe unterschiedliche Hashes (ein zufälliger Salt ist im Hash eingebettet)
- Immer `encoder.matches(raw, encoded)` verwenden, Hashes niemals mit `equals()` vergleichen
- CSRF-Schutz ist standardmäßig aktiviert
- `SecurityFilterChain` ist die moderne Art, Security zu konfigurieren (ersetzt `WebSecurityConfigurerAdapter`)

## Muster {#patterns}

### BCrypt-Passwortkodierung {#bcrypt-password-encoding}
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

### SecurityFilterChain (moderne Konfiguration) {#securityfilterchain-modern-configuration}
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

### Manuelle sitzungsbasierte Authentifizierung {#manual-session-based-authentication}
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

## Stolperfallen {#gotchas}

- Passwörter niemals im Klartext speichern - immer BCryptPasswordEncoder oder Argon2 verwenden
- BCrypt `matches()` extrahiert den Salt aus dem gespeicherten Hash - deshalb stimmen unterschiedliche Hashes für dieselbe Eingabe trotzdem überein
- Die Reihenfolge der `requestMatchers` ist wichtig - spezifischere Regeln zuerst, `anyRequest()` zuletzt
- CSRF-Token ist für POST-Formulare mit Thymeleaf erforderlich (wird automatisch eingefügt); bei REST-APIs mit Token-Authentifizierung deaktivieren
- `@PreAuthorize("hasRole('ADMIN')")` erfordert `@EnableMethodSecurity` in der Konfigurationsklasse

## Siehe auch {#see-also}

- [[spring-mvc-rest]] - Controller, die durch Security geschützt werden
- [[spring-ioc-beans]] - Security-Beans und Konfiguration
- [[spring-validation]] - Eingabevalidierung als Sicherheitsschicht
