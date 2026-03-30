---
title: Android XML Layouts
category: concepts
tags: [android, xml, layout, view, viewgroup, linear-layout, relative-layout, constraint-layout]
---
# Android XML Layouts

## Key Facts

- Android UI is built with Views (individual UI elements) and ViewGroups (containers for views)
- XML layout files live in `res/layout/` directory and are inflated at runtime
- **LinearLayout** - arranges children in single row (horizontal) or column (vertical)
- **RelativeLayout** - positions children relative to parent or sibling views
- **ConstraintLayout** - flexible positioning with constraints (recommended, best performance)
- Views have `layout_width` and `layout_height`: `match_parent`, `wrap_content`, or fixed dp
- `dp` (density-independent pixels) for sizes, `sp` (scale-independent pixels) for text sizes
- `findViewById<T>(R.id.viewId)` connects XML views to Java/Kotlin code; View Binding is the modern alternative
- Common Views: `TextView`, `EditText`, `Button`, `ImageView`, `Spinner`, `RecyclerView`
- See [[android-architecture]] for how layouts fit into MVVM architecture
- See [[android-room-database]] for data-driven UIs

## Patterns

### LinearLayout (vertical)

```xml
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/titleText"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Welcome"
        android:textSize="24sp"
        android:textStyle="bold" />

    <EditText
        android:id="@+id/usernameInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter username"
        android:inputType="textPersonName" />

    <EditText
        android:id="@+id/passwordInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter password"
        android:inputType="textPassword" />

    <Button
        android:id="@+id/loginButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Login" />
</LinearLayout>
```

### RelativeLayout

```xml
<RelativeLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/productImage"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:layout_alignParentStart="true"
        android:src="@drawable/product" />

    <TextView
        android:id="@+id/productName"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_toEndOf="@id/productImage"
        android:layout_marginStart="16dp"
        android:text="Product Name"
        android:textSize="18sp" />

    <TextView
        android:id="@+id/productPrice"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_toEndOf="@id/productImage"
        android:layout_below="@id/productName"
        android:layout_marginStart="16dp"
        android:text="$29.99" />
</RelativeLayout>
```

### ConstraintLayout

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/avatar"
        android:layout_width="80dp"
        android:layout_height="80dp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        android:layout_margin="16dp" />

    <TextView
        android:id="@+id/userName"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        app:layout_constraintStart_toEndOf="@id/avatar"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="@id/avatar"
        android:layout_marginStart="12dp" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

### Connecting views in Activity (Java)

```java
public class MainActivity extends AppCompatActivity {
    private TextView titleText;
    private EditText usernameInput;
    private Button loginButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        titleText = findViewById(R.id.titleText);
        usernameInput = findViewById(R.id.usernameInput);
        loginButton = findViewById(R.id.loginButton);

        loginButton.setOnClickListener(v -> {
            String username = usernameInput.getText().toString();
            titleText.setText("Hello, " + username + "!");
        });
    }
}
```

### View Binding (modern approach)

```kotlin
// build.gradle
android {
    buildFeatures {
        viewBinding = true
    }
}

// Activity
class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.loginButton.setOnClickListener {
            val username = binding.usernameInput.text.toString()
            binding.titleText.text = "Hello, $username!"
        }
    }
}
```

### Spinner (dropdown)

```java
Spinner spinner = findViewById(R.id.spinner);
ArrayList<String> items = new ArrayList<>(List.of("Guitar", "Drums", "Keyboard"));

ArrayAdapter<String> adapter = new ArrayAdapter<>(
    this, android.R.layout.simple_spinner_item, items);
adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
spinner.setAdapter(adapter);

spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        String selected = items.get(position);
        // update UI based on selection
    }
    @Override
    public void onNothingSelected(AdapterView<?> parent) {}
});
```

## Gotchas

- **Symptom**: Layout looks different on different screen sizes -> **Cause**: Using fixed px sizes instead of dp/sp -> **Fix**: Always use `dp` for dimensions, `sp` for text sizes; test on multiple screen densities
- **Symptom**: Deep nested layouts cause slow rendering -> **Cause**: Multiple nested LinearLayouts/RelativeLayouts -> **Fix**: Use ConstraintLayout for flat view hierarchies; use Hierarchy Viewer to analyze
- **Symptom**: `NullPointerException` on `findViewById()` -> **Cause**: View ID doesn't exist in current layout, or `setContentView()` not called first -> **Fix**: Verify ID exists in XML; call `setContentView()` before `findViewById()`
- **Symptom**: Keyboard covers input fields -> **Cause**: No scroll container -> **Fix**: Wrap layout in `ScrollView` or set `android:windowSoftInputMode="adjustResize"` in AndroidManifest

## See Also

- [[android-architecture]] - How layouts connect to ViewModels and data binding
- [[android-room-database]] - Loading data to display in layouts
- Android Docs: [Layouts](https://developer.android.com/develop/ui/views/layout/declaring-layout)
- Android Docs: [ConstraintLayout](https://developer.android.com/develop/ui/views/layout/constraint-layout)
