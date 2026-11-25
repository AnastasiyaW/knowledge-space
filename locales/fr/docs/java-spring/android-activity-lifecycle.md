---
title: "Cycle de vie des Activity Android et navigation par Intent"
category: concepts
tags: [java-spring, android, activity, lifecycle, intent, navigation]
level: 3
source_sha256: f359b31888718fcfdda832d2c419285538ae29948fbcf7f92ed2a2ea97a712ba
translation: machine
translated_at: '2026-10-24'
---
# Cycle de vie des Activity Android et navigation par Intent {#android-activity-lifecycle-and-intent-navigation}

Callbacks du cycle de vie des Activity, Intent explicites et implicites, transmission de données entre Activity, API Activity Result et déclarations dans AndroidManifest.

## Points clés {#key-facts}

- Activity = écran unique avec interface utilisateur ; dispose de callbacks de cycle de vie définis
- Ordre du cycle de vie : `onCreate` -> `onStart` -> `onResume` (premier plan) -> `onPause` -> `onStop` -> `onDestroy`
- Un Intent explicite cible une Activity précise ; un Intent implicite spécifie une action (ACTION_VIEW, ACTION_SEND)
- Les données sont transmises via `intent.putExtra(key, value)` et récupérées avec `getIntent().getXxxExtra(key)`
- `startActivityForResult` est déprécié : utiliser l'API Activity Result (`registerForActivityResult`)
- Une seule activity dans le manifeste possède le filtre d'Intent `MAIN` + `LAUNCHER` (point d'entrée)

## Modèles {#patterns}

### Callbacks du cycle de vie {#lifecycle-callbacks}
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

### Intent explicite (naviguer vers une Activity connue) {#explicit-intent-navigate-to-known-activity}
```java
Intent intent = new Intent(MainActivity.this, SecondActivity.class);
intent.putExtra("user_name", "Alice");
intent.putExtra("user_age", 25);
startActivity(intent);

// Receiving in SecondActivity
String name = getIntent().getStringExtra("user_name");
int age = getIntent().getIntExtra("user_age", 0);
```

### Intent implicite (basé sur une action) {#implicit-intent-action-based}
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

### API Activity Result (moderne) {#activity-result-api-modern}
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

### Déclaration dans le manifeste {#manifest-declaration}
```xml
<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
<activity android:name=".DetailActivity" android:label="Details" />
```

## Pièges {#gotchas}

- Un changement de configuration (rotation) détruit puis recrée l'Activity : sauvegarder l'état dans `onSaveInstanceState` ou utiliser un ViewModel
- `getIntent().getStringExtra()` renvoie null si la clé n'existe pas : toujours fournir des valeurs par défaut pour les types primitifs
- `finish()` détruit l'Activity courante et revient à la précédente dans la pile de retour
- Les classes internes anonymes (listeners) peuvent retenir une référence à l'Activity et provoquer une fuite mémoire : utiliser des lambdas ou des références faibles

## Voir aussi {#see-also}

- [[android-fragments-navigation]] - Fragments comme portions d'interface réutilisables
- [[android-architecture-mvvm]] - Le ViewModel survit aux changements de configuration
- [[android-fundamentals-ui]] - Layouts XML dans les Activities
