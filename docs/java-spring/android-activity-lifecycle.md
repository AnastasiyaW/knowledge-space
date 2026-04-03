---
title: Android Activity Lifecycle and Intent Navigation
category: concepts
tags: [java-spring, android, activity, lifecycle, intent, navigation]
---

# Android Activity Lifecycle and Intent Navigation

Activity lifecycle callbacks, explicit and implicit Intents, data passing between Activities, Activity Result API, and AndroidManifest declarations.

## Key Facts

- Activity = single screen with UI; has defined lifecycle callbacks
- Lifecycle order: `onCreate` -> `onStart` -> `onResume` (foreground) -> `onPause` -> `onStop` -> `onDestroy`
- Explicit Intent targets a specific Activity; Implicit Intent specifies an action (ACTION_VIEW, ACTION_SEND)
- Data passed via `intent.putExtra(key, value)` and retrieved with `getIntent().getXxxExtra(key)`
- `startActivityForResult` is deprecated - use Activity Result API (`registerForActivityResult`)
- Only one activity in manifest has `MAIN` + `LAUNCHER` intent filter (entry point)

## Patterns

### Lifecycle Callbacks
```java
@Override protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    // Initialize UI, restore state
}
@Override protected void onResume() {
    super.onResume();   // Activity interactive
}
@Override protected void onPause() {
    super.onPause();    // Save transient data, stop animations
}
@Override protected void onDestroy() {
    super.onDestroy();  // Release resources
}
```

### Explicit Intent (Navigate to Known Activity)
```java
Intent intent = new Intent(MainActivity.this, SecondActivity.class);
intent.putExtra("user_name", "Alice");
intent.putExtra("user_age", 25);
startActivity(intent);

// Receiving in SecondActivity
String name = getIntent().getStringExtra("user_name");
int age = getIntent().getIntExtra("user_age", 0);
```

### Implicit Intent (Action-Based)
```java
// Open URL
startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://example.com")));

// Share text
Intent share = new Intent(Intent.ACTION_SEND);
share.setType("text/plain");
share.putExtra(Intent.EXTRA_TEXT, "Check this out!");
startActivity(Intent.createChooser(share, "Share via"));

// Dial phone
startActivity(new Intent(Intent.ACTION_DIAL, Uri.parse("tel:+1234567890")));
```

### Activity Result API (Modern)
```java
ActivityResultLauncher<Intent> launcher = registerForActivityResult(
    new ActivityResultContracts.StartActivityForResult(),
    result -> {
        if (result.getResultCode() == RESULT_OK) {
            String value = result.getData().getStringExtra("result_key");
        }
    });
launcher.launch(new Intent(this, SecondActivity.class));

// In called activity
setResult(RESULT_OK, new Intent().putExtra("result_key", "value"));
finish();
```

### Manifest Declaration
```xml
<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
<activity android:name=".DetailActivity" android:label="Details" />
```

## Gotchas

- Configuration change (rotation) destroys and recreates Activity - save state in `onSaveInstanceState` or use ViewModel
- `getIntent().getStringExtra()` returns null if key doesn't exist - always provide defaults for primitives
- `finish()` destroys the current Activity and returns to the previous one on the back stack
- Anonymous inner classes (listeners) can leak Activity reference - use lambdas or weak references

## See Also

- [[android-fragments-navigation]] - Fragments as reusable UI portions
- [[android-architecture-mvvm]] - ViewModel survives config changes
- [[android-fundamentals-ui]] - XML layouts within Activities
