---
title: "Mobile-Tests"
category: tool
tags: [mobile, android, kaspresso, espresso, xctest, emulator, screen-objects, ci]
level: 3
source_sha256: f00fa945f75803a9855f6785702786311231cfd53f508db8308d20c4c6518480
translation: machine
translated_at: '2026-10-24'
---
# Mobile-Tests {#mobile-testing}

Android-UI-Tests verwenden Kaspresso (Kotlin-DSL über Espresso + UI Automator). Screen Objects entsprechen dem POM. Emulatoren in der CI benötigen Hardwarebeschleunigung (macOS-Runner). iOS verwendet XCTest mit Accessibility Identifiers. Beide Plattformen teilen das Muster: Screen Objects für Wartbarkeit, schrittbasierte Struktur für das Allure-Reporting.

## Key Facts {#key-facts}

- **Kaspresso**: Android-Testframework, DSL über Espresso, integrierte Behandlung flaky Tests
- Screen Objects = Page Object Model für Mobile (eine Klasse pro Screen, Elemente als Properties)
- `ActivityScenarioRule` startet die zu testende Activity
- Emulator-Berechtigungen: `GrantPermissionRule.grant(...)` für Laufzeitberechtigungen
- CI: `android-emulator-runner`-Action auf macOS für Hardwarebeschleunigung
- Animationen auf dem Emulator deaktivieren: `adb shell settings put global window_animation_scale 0`

## Patterns {#patterns}

### Kaspresso Test {#kaspresso-test}

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

### Screen Objects {#screen-objects}

```kotlin
object MainScreen : KScreen<MainScreen>() {
    override val layoutId = R.layout.activity_main
    override val viewClass = MainActivity::class.java

    val title = KTextView { withId(R.id.title) }
    val submitButton = KButton { withId(R.id.submit_button) }
    val inputField = KEditText { withId(R.id.input_field) }
}
```

### Allure Integration {#allure-integration}

```kotlin
class MainScreenTest : TestCase(
    kaspressoBuilder = Kaspresso.Builder.withAllureSupport()
) {
    // Steps automatically appear in Allure report
    // Screenshots captured on failure
}
```

### Gradle Dependencies {#gradle-dependencies}

```kotlin
androidTestImplementation("com.kaspersky.android-components:kaspresso:1.5.3")
androidTestImplementation("com.kaspersky.android-components:kaspresso-allure-support:1.5.3")
androidTestImplementation("androidx.test:runner:1.5.2")
```

## Gotchas {#gotchas}

- Die meisten Kaspresso-Beispiele online funktionieren nicht – eine falsche Einstellung bricht alles mit irreführenden Fehlermeldungen
- Speicherberechtigungen haben sich über API-Level hinweg geändert: SDK 29+ verwendet `MANAGE_EXTERNAL_STORAGE`
- Timeout beim Booten des Emulators in der CI – den Parameter `boot-timeout` erhöhen
- Jeder Test sollte den App-Zustand zurücksetzen oder eine frische Installation verwenden (`clearAllData()`), um Isolation sicherzustellen
- iOS: XCTest + Accessibility Identifiers, ähnliches Screen-Object-Muster, Xcode Test Recorder als Ausgangspunkt

## See Also {#see-also}

- [[page-object-model]] - POM-Prinzipien gelten für Screen Objects
- [[ci-cd-test-automation]] - Emulatoren in GitHub Actions ausführen
- [[allure-reporting]] - Reporting für Mobile-Tests
