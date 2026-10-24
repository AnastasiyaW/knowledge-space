---
title: "Android-Activity-Lebenszyklus und Intent-Navigation"
category: concepts
tags: [java-spring, android, activity, lifecycle, intent, navigation]
level: 3
source_sha256: f359b31888718fcfdda832d2c419285538ae29948fbcf7f92ed2a2ea97a712ba
translation: machine
translated_at: '2026-10-24'
---
# Android-Activity-Lebenszyklus und Intent-Navigation {#android-activity-lifecycle-and-intent-navigation}

Lebenszyklus-Callbacks von Activities, explizite und implizite Intents, Datenübergabe zwischen Activities, Activity Result API sowie Deklarationen im AndroidManifest.

## Wichtige Fakten {#key-facts}

- Activity = einzelner Bildschirm mit UI; besitzt definierte Lebenszyklus-Callbacks
- Lebenszyklus-Reihenfolge: `onCreate` -> `onStart` -> `onResume` (Vordergrund) -> `onPause` -> `onStop` -> `onDestroy`
- Ein expliziter Intent zielt auf eine bestimmte Activity; ein impliziter Intent gibt eine Aktion an (ACTION_VIEW, ACTION_SEND)
- Daten werden über `intent.putExtra(key, value)` übergeben und mit `getIntent().getXxxExtra(key)` abgerufen
- `startActivityForResult` ist veraltet - stattdessen die Activity Result API (`registerForActivityResult`) verwenden
- Im Manifest hat nur eine Activity den Intent-Filter `MAIN` + `LAUNCHER` (Einstiegspunkt)

## Muster {#patterns}

### Lebenszyklus-Callbacks {#lifecycle-callbacks}
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

### Expliziter Intent (Navigation zu einer bekannten Activity) {#explicit-intent-navigate-to-known-activity}
```java
Intent intent = new Intent(MainActivity.this, SecondActivity.class);
intent.putExtra("user_name", "Alice");
intent.putExtra("user_age", 25);
startActivity(intent);

// Receiving in SecondActivity
String name = getIntent().getStringExtra("user_name");
int age = getIntent().getIntExtra("user_age", 0);
```

### Impliziter Intent (aktionsbasiert) {#implicit-intent-action-based}
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

### Activity Result API (modern) {#activity-result-api-modern}
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

### Deklaration im Manifest {#manifest-declaration}
```xml
<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
<activity android:name=".DetailActivity" android:label="Details" />
```

## Stolperfallen {#gotchas}

- Eine Konfigurationsänderung (Rotation) zerstört die Activity und erzeugt sie neu - Zustand in `onSaveInstanceState` sichern oder ein ViewModel verwenden
- `getIntent().getStringExtra()` liefert `null`, wenn der Schlüssel nicht existiert - für Primitive immer Standardwerte angeben
- `finish()` zerstört die aktuelle Activity und kehrt zur vorherigen Activity im Back Stack zurück
- Anonyme innere Klassen (Listener) können eine Referenz auf die Activity festhalten (Leak) - Lambdas oder schwache Referenzen verwenden

## Siehe auch {#see-also}

- [[android-fragments-navigation]] - Fragments als wiederverwendbare UI-Teile
- [[android-architecture-mvvm]] - ViewModel übersteht Konfigurationsänderungen
- [[android-fundamentals-ui]] - XML-Layouts innerhalb von Activities
