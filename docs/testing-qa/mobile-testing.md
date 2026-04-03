---
title: Mobile Testing
category: tool
tags: [mobile, android, kaspresso, espresso, xctest, emulator, screen-objects, ci]
---

# Mobile Testing

Android UI testing uses Kaspresso (Kotlin DSL over Espresso + UI Automator). Screen objects = POM equivalent. Emulators in CI require hardware acceleration (macOS runners). iOS uses XCTest with accessibility identifiers. Both platforms share the pattern: screen objects for maintainability, step-based structure for Allure reporting.

## Key Facts

- **Kaspresso**: Android testing framework, DSL over Espresso, built-in flaky test handling
- Screen objects = Page Object Model for mobile (class per screen, elements as properties)
- `ActivityScenarioRule` launches the activity under test
- Emulator permissions: `GrantPermissionRule.grant(...)` for runtime permissions
- CI: `android-emulator-runner` action on macOS for hardware acceleration
- Disable animations on emulator: `adb shell settings put global window_animation_scale 0`

## Patterns

### Kaspresso Test

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

### Screen Objects

```kotlin
object MainScreen : KScreen<MainScreen>() {
    override val layoutId = R.layout.activity_main
    override val viewClass = MainActivity::class.java

    val title = KTextView { withId(R.id.title) }
    val submitButton = KButton { withId(R.id.submit_button) }
    val inputField = KEditText { withId(R.id.input_field) }
}
```

### Allure Integration

```kotlin
class MainScreenTest : TestCase(
    kaspressoBuilder = Kaspresso.Builder.withAllureSupport()
) {
    // Steps automatically appear in Allure report
    // Screenshots captured on failure
}
```

### Gradle Dependencies

```kotlin
androidTestImplementation("com.kaspersky.android-components:kaspresso:1.5.3")
androidTestImplementation("com.kaspersky.android-components:kaspresso-allure-support:1.5.3")
androidTestImplementation("androidx.test:runner:1.5.2")
```

## Gotchas

- Most online Kaspresso examples are non-functional - one wrong setting breaks everything with misleading errors
- Storage permissions changed across API levels: SDK 29+ uses `MANAGE_EXTERNAL_STORAGE`
- Emulator boot timeout on CI - increase `boot-timeout` parameter
- Each test should clear app state or use fresh install (`clearAllData()`) for isolation
- iOS: XCTest + accessibility identifiers, similar screen object pattern, Xcode Test Recorder as starting point

## See Also

- [[page-object-model]] - POM principles apply to screen objects
- [[ci-cd-test-automation]] - running emulators in GitHub Actions
- [[allure-reporting]] - mobile test reporting
