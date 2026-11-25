---
title: "Tests mobiles"
category: tool
tags: [mobile, android, kaspresso, espresso, xctest, emulator, screen-objects, ci]
level: 3
source_sha256: f00fa945f75803a9855f6785702786311231cfd53f508db8308d20c4c6518480
translation: machine
translated_at: '2026-10-24'
---
# Tests mobiles {#mobile-testing}

Les tests d'interface Android utilisent Kaspresso (DSL Kotlin par-dessus Espresso et UI Automator). Les objets d'écran (screen objects) sont l'équivalent du POM. Les émulateurs en CI nécessitent une accélération matérielle (runners macOS). iOS utilise XCTest avec des identifiants d'accessibilité. Les deux plateformes partagent le même modèle : des objets d'écran pour la maintenabilité, et une structure par étapes pour le reporting Allure.

## Points clés {#key-facts}

- **Kaspresso** : framework de test Android, DSL au-dessus d'Espresso, gestion intégrée des tests instables (flaky)
- Objets d'écran = Page Object Model pour le mobile (une classe par écran, éléments exposés en propriétés)
- `ActivityScenarioRule` lance l'activité testée
- Permissions de l'émulateur : `GrantPermissionRule.grant(...)` pour les permissions à l'exécution
- CI : action `android-emulator-runner` sur macOS pour l'accélération matérielle
- Désactiver les animations sur l'émulateur : `adb shell settings put global window_animation_scale 0`

## Modèles {#patterns}

### Test Kaspresso {#kaspresso-test}

```kotlin
@RunWith(AndroidJUnit4::class)
class MainScreenTest : TestCase() {
    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun testMainScreen() = run {
        step("Check title") {
            onScreen<MainScreen> {
                title {
                    isVisible()
                    hasText("Welcome")
                }
            }
        }
        step("Click submit") {
            onScreen<MainScreen> {
                submitButton.click()
            }
        }
    }
}
```

### Objets d'écran {#screen-objects}

```kotlin
object MainScreen : KScreen<MainScreen>() {
    override val layoutId = R.layout.activity_main
    override val viewClass = MainActivity::class.java

    val title = KTextView { withId(R.id.title) }
    val submitButton = KButton { withId(R.id.submit_button) }
    val inputField = KEditText { withId(R.id.input_field) }
}
```

### Intégration Allure {#allure-integration}

```kotlin
class MainScreenTest : TestCase(
    kaspressoBuilder = Kaspresso.Builder.withAllureSupport()
) {
    // Steps automatically appear in Allure report
    // Screenshots captured on failure
}
```

### Dépendances Gradle {#gradle-dependencies}

```kotlin
androidTestImplementation("com.kaspersky.android-components:kaspresso:1.5.3")
androidTestImplementation("com.kaspersky.android-components:kaspresso-allure-support:1.5.3")
androidTestImplementation("androidx.test:runner:1.5.2")
```

## Pièges courants {#gotchas}

- La plupart des exemples Kaspresso en ligne ne fonctionnent pas : un seul mauvais paramètre casse tout, avec des erreurs trompeuses
- Les permissions de stockage ont changé selon les niveaux d'API : à partir du SDK 29, on utilise `MANAGE_EXTERNAL_STORAGE`
- Délai de démarrage de l'émulateur en CI : augmenter le paramètre `boot-timeout`
- Chaque test doit réinitialiser l'état de l'application ou utiliser une installation fraîche (`clearAllData()`) pour garantir l'isolation
- iOS : XCTest + identifiants d'accessibilité, modèle d'objets d'écran similaire, Xcode Test Recorder comme point de départ

## Voir aussi {#see-also}

- [[page-object-model]] - les principes du POM s'appliquent aux objets d'écran
- [[ci-cd-test-automation]] - exécution d'émulateurs dans GitHub Actions
- [[allure-reporting]] - reporting des tests mobiles
