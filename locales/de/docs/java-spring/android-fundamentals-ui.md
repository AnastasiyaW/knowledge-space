---
title: "Android-Grundlagen – Projektstruktur und XML-Layouts"
category: concepts
tags: [java-spring, android, xml-layouts, views, ui, android-studio]
level: 2
source_sha256: b4723c798ed42ad55e21d986e390691355906c4c4ec204db8bbca6d6bf1a70b8
translation: machine
translated_at: '2026-10-24'
---
# Android-Grundlagen – Projektstruktur und XML-Layouts {#android-fundamentals-project-structure-and-xml-layouts}

Android-Projektstruktur, XML-Layoutsystem, View-Hierarchie, gängige Widgets und ViewGroups (LinearLayout, RelativeLayout, ConstraintLayout).

## Wichtige Fakten {#key-facts}

- `app/src/main/java/` – Quellcode; `res/layout/` – XML-Layouts; `res/values/` – Strings, Farben, Styles
- `AndroidManifest.xml` deklariert Activities, Berechtigungen und die App-Konfiguration
- Alle UI-Elemente sind Unterklassen von `View`; Container sind `ViewGroup`
- Einheiten: `dp` (density-independent pixels) für das Layout, `sp` (scale-independent) für Text
- `wrap_content` = Größe an den Inhalt anpassen; `match_parent` = das übergeordnete Element ausfüllen
- ConstraintLayout ist das modern empfohlene Layout für komplexe UIs
- Build-System: Gradle mit `build.gradle`-Dateien

## Muster {#patterns}

### Gängige Views {#common-views}
```xml
<TextView android:id="@+id/textView"
    android:text="Hello" android:textSize="24sp" android:textColor="#FF0000" />

<EditText android:id="@+id/input"
    android:hint="Enter name" android:inputType="text" />

<Button android:id="@+id/button"
    android:text="Click Me" android:onClick="onButtonClick" />

<ImageView android:id="@+id/image"
    android:src="@drawable/photo" android:scaleType="centerCrop" />

<Spinner android:id="@+id/spinner" />
```

### Layout-Typen {#layout-types}
```xml
<!-- LinearLayout - vertical/horizontal stacking -->
<LinearLayout android:orientation="vertical" android:padding="16dp">
    <TextView ... />
    <Button ... />
</LinearLayout>

<!-- ConstraintLayout - flexible constraint-based positioning -->
<androidx.constraintlayout.widget.ConstraintLayout>
    <Button
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

### Interaktion zwischen Activity und View {#activity-view-interaction}
```java
public class MainActivity extends AppCompatActivity {
    private TextView quantityText;
    private int quantity = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        quantityText = findViewById(R.id.quantityText);
    }

    public void increaseQuantity(View view) {
        quantity++;
        quantityText.setText(String.valueOf(quantity));
    }
}
```

### Einrichtung eines Spinners (Dropdown) {#spinner-dropdown-setup}
```java
ArrayAdapter<String> adapter = new ArrayAdapter<>(
    this, android.R.layout.simple_spinner_item, items);
adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
spinner.setAdapter(adapter);
spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
    @Override
    public void onItemSelected(AdapterView<?> parent, View v, int pos, long id) {
        String selected = parent.getItemAtPosition(pos).toString();
    }
    @Override public void onNothingSelected(AdapterView<?> p) {}
});
```

## Fallstricke {#gotchas}

- `dp` vs. `sp`: `sp` nur für Text verwenden (berücksichtigt die Schriftskalierung des Nutzers), `dp` für alles andere
- `findViewById` gibt null zurück, wenn die ID im aktuellen Layout nicht existiert – führt zur Laufzeit zu einer NPE
- Das Attribut `android:onClick` funktioniert nur für Activities, nicht für Fragments – stattdessen programmatische Listener verwenden
- RelativeLayout kann bei komplexen Layouts langsamer sein als ConstraintLayout (mehrere Measure-Durchgänge)

## Siehe auch {#see-also}

- [[android-activity-lifecycle]] – Activity-Lebenszyklus und Intent-Navigation
- [[android-recyclerview]] – Effizientes Rendern von Listen
- [[android-jetpack-compose]] – Moderne deklarative UI-Alternative
