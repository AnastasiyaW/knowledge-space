---
title: Android Fundamentals - Project Structure and XML Layouts
category: concepts
tags: [java-spring, android, xml-layouts, views, ui, android-studio]
---

# Android Fundamentals - Project Structure and XML Layouts

Android project structure, XML layout system, View hierarchy, common widgets, and ViewGroups (LinearLayout, RelativeLayout, ConstraintLayout).

## Key Facts

- `app/src/main/java/` - source code; `res/layout/` - XML layouts; `res/values/` - strings, colors, styles
- `AndroidManifest.xml` declares activities, permissions, and app configuration
- All UI elements are subclasses of `View`; containers are `ViewGroup`
- Units: `dp` (density-independent pixels) for layout, `sp` (scale-independent) for text
- `wrap_content` = size to fit content; `match_parent` = fill parent
- ConstraintLayout is the modern recommended layout for complex UIs
- Build system: Gradle with `build.gradle` files

## Patterns

### Common Views
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

### Layout Types
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

### Activity-View Interaction
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

### Spinner (Dropdown) Setup
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

## Gotchas

- `dp` vs `sp`: use `sp` only for text (respects user font scale), `dp` for everything else
- `findViewById` returns null if ID doesn't exist in the current layout - causes NPE at runtime
- `android:onClick` attribute only works for Activities, not Fragments - use programmatic listeners
- RelativeLayout can be slower than ConstraintLayout for complex layouts (multiple measure passes)

## See Also

- [[android-activity-lifecycle]] - Activity lifecycle and Intent navigation
- [[android-recyclerview]] - Efficient list rendering
- [[android-jetpack-compose]] - Modern declarative UI alternative
