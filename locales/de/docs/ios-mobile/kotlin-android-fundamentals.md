---
title: "Kotlin und Android-Grundlagen"
category: concepts
tags: [ios-mobile, android, kotlin, project-structure, build-gradle, data-class, coroutines]
level: 3
source_sha256: e65fcc18363ad1c4dd8a7c87e42f942cd52af8113962974ae5e6189907c2de99
translation: machine
translated_at: '2026-10-24'
---
# Kotlin und Android-Grundlagen {#kotlin-and-android-fundamentals}

Kotlin ist die primäre Sprache für die Android-Entwicklung. Dieser Eintrag behandelt die Grundlagen der Kotlin-Sprache, die Struktur von Android-Projekten, die Konfiguration von build.gradle, Activities, Fragments, Navigation und UI-Komponenten.

## Wichtige Fakten {#key-facts}

- `data class` generiert automatisch `equals()`, `hashCode()`, `toString()`, `copy()`
- `companion object` stellt statisch wirkende Member bereit, die über den Klassennamen angesprochen werden
- `lateinit var` deklariert eine nicht-nullable Property, die später initialisiert wird (nicht im Konstruktor)
- `@Volatile` garantiert, dass der Wert aus dem Hauptspeicher gelesen wird und nicht aus dem CPU-Cache - entscheidend für Singletons
- `synchronized(this)` verhindert gleichzeitigen Zugriff aus mehreren Threads
- Android verwendet XML-Layouts (`res/layout/`), während SwiftUI deklarativen Code nutzt
- `SharedPreferences` bietet einfache persistente Key-Value-Speicherung

## Muster {#patterns}

### Projektstruktur {#project-structure}

```hcl
app/
  src/main/
    java/com.example.app/
      di/           - dependency injection (Dagger 2)
      database/     - Room entities, DAOs, database class
      rest/         - Retrofit API interfaces and data models
      fragments/    - Fragment classes
      activities/   - Activity classes
      viewmodel/    - ViewModel classes
    res/
      layout/       - XML layout files
      drawable/     - images and vector assets
      values/       - strings.xml, colors.xml, styles.xml
      menu/         - menu XML files
      navigation/   - Navigation graph XML
  build.gradle      - module-level dependencies
build.gradle        - project-level repository settings
```

### Wichtige Abhängigkeiten in build.gradle {#buildgradle-key-dependencies}

```groovy
apply plugin: 'kotlin-kapt'

android {
    compileSdkVersion 34
    defaultConfig {
        applicationId "com.example.app"
        minSdkVersion 21
        targetSdkVersion 34
    }
}

dependencies {
    // Coroutines
    implementation "org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.0"
    implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.0"

    // Architecture components
    implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.0"
    implementation "androidx.lifecycle:lifecycle-livedata-ktx:2.6.0"

    // Room
    implementation "androidx.room:room-runtime:2.5.0"
    kapt "androidx.room:room-compiler:2.5.0"

    // Retrofit + Gson
    implementation "com.squareup.retrofit2:retrofit:2.9.0"
    implementation "com.squareup.retrofit2:converter-gson:2.9.0"

    // Glide (image loading)
    implementation "com.github.bumptech.glide:glide:4.15.0"

    // Navigation
    implementation "androidx.navigation:navigation-fragment-ktx:2.6.0"
    implementation "androidx.navigation:navigation-ui-ktx:2.6.0"

    // RecyclerView
    implementation "androidx.recyclerview:recyclerview:1.3.0"
}
```

### data class {#data-class}

```kotlin
data class GeckoCoin(
    val id: String,
    val symbol: String,
    val name: String,
    val image: String,
    val current_price: Float,
    val market_cap: Float,
    val market_cap_rank: Int
)
```

### Fragment-Lebenszyklus {#fragment-lifecycle}

```kotlin
class RecordFragment : Fragment() {
    private lateinit var viewModel: RecordViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_record, container, false)
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        val application = requireNotNull(activity).application
        viewModel = ViewModelProviders.of(this,
            RecordViewModelFactory(application))
            .get(RecordViewModel::class.java)

        viewModel.elapsedTime.observe(viewLifecycleOwner, Observer { time ->
            timerText.text = time
        })
    }
}
```

### Activity-Navigation {#activity-navigation}

```kotlin
// Start another Activity
val intent = Intent(this, SettingsActivity::class.java)
intent.putExtra("KEY", value)
startActivity(intent)

// Receive in destination
val value = intent.getStringExtra("KEY")

// Go back
finish()
```

### Navigation Component {#navigation-component}

```xml
<!-- nav_graph.xml -->
<navigation app:startDestination="@id/recordFragment">
    <fragment android:id="@+id/recordFragment"
              android:name=".record.RecordFragment" />
    <fragment android:id="@+id/listFragment"
              android:name=".list.ListFragment" />
</navigation>
```

```kotlin
// Navigate between fragments
findNavController().navigate(R.id.action_listFragment_to_playerFragment)

// With arguments
val bundle = bundleOf("itemPath" to filePath)
findNavController().navigate(R.id.action, bundle)

// Receive arguments
val itemPath = arguments?.getString("itemPath")
```

### ConstraintLayout XML {#constraintlayout-xml}

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:id="@+id/tvTitle"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <Button
        android:id="@+id/btnAction"
        app:layout_constraintTop_toBottomOf="@id/tvTitle"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

### RecyclerView Adapter {#recyclerview-adapter}

```kotlin
class CurrencyAdapter(
    private var items: List<GeckoCoin>,
    private val context: Context
) : RecyclerView.Adapter<CurrencyAdapter.ViewHolder>() {

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvName: TextView = itemView.findViewById(R.id.tvName)
        val ivIcon: ImageView = itemView.findViewById(R.id.ivIcon)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.recycler_view_item, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val coin = items[position]
        holder.tvName.text = coin.name
        Glide.with(context).load(coin.image).into(holder.ivIcon)

        holder.itemView.setOnClickListener { /* handle click */ }
    }

    override fun getItemCount() = items.size

    fun updateItems(newItems: List<GeckoCoin>) {
        items = newItems
        notifyDataSetChanged()
    }
}
```

### Einrichtung im Fragment {#setup-in-fragment}

```kotlin
val adapter = CurrencyAdapter(emptyList(), requireContext())
recyclerView.layoutManager = LinearLayoutManager(context)
recyclerView.adapter = adapter

viewModel.coins.observe(viewLifecycleOwner) { coins ->
    adapter.updateItems(coins)
}
```

### AlertDialog {#alertdialog}

```kotlin
AlertDialog.Builder(activity)
    .setTitle(R.string.dialog_title)
    .setMessage(R.string.dialog_message)
    .setPositiveButton(R.string.yes) { dialog, _ -> dialog.cancel() }
    .setNegativeButton(R.string.no) { dialog, _ -> dialog.cancel() }
    .show()
```

### SharedPreferences {#sharedpreferences}

```kotlin
val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
prefs.edit().putLong("TRIGGER_TIME", value).apply()  // write
val time = prefs.getLong("TRIGGER_TIME", 0L)          // read with default
```

### Toast {#toast}

```kotlin
Toast.makeText(context, "Message", Toast.LENGTH_SHORT).show()
```

### String-Ressourcen {#string-resources}

```xml
<!-- res/values/strings.xml -->
<resources>
    <string name="app_name">MyApp</string>
    <string name="recording_started">Recording started</string>
</resources>
```

```kotlin
getString(R.string.recording_started)   // in code
// android:text="@string/recording_started"  in XML
```

### Glide (Bildladen) {#glide-image-loading}

```kotlin
Glide.with(context)
    .load(imageUrl)
    .placeholder(R.drawable.placeholder)
    .error(R.drawable.error_image)
    .into(imageView)
```

## Stolperfallen {#gotchas}

- `lateinit`-Properties führen zu `UninitializedPropertyAccessException`, wenn sie vor der Initialisierung zugegriffen werden
- `notifyDataSetChanged()` zeichnet alle Elemente neu - in Produktivcode `DiffUtil` für effiziente partielle Aktualisierungen verwenden
- `onActivityCreated()` ist veraltet - im modernen Fragment-Lebenszyklus `onViewCreated()` verwenden
- Android-XML-Layouts sind im Vergleich zum deklarativen Code von SwiftUI ausführlich
- Das `kapt`-Plugin ist für Annotation Processing (Room, Dagger) erforderlich - ohne es schlägt die Code-Generierung fehl
- `startActivityForResult()` ist veraltet - im modernen Code die Activity Result API verwenden

## Siehe auch {#see-also}

- [[android-mvvm-architecture]] - ViewModel, LiveData, Repository-Muster
- [[android-room-database]] - Room-Persistenz-Framework
- [[android-retrofit-networking]] - Retrofit REST-API-Client
- [[android-dagger-dependency-injection]] - Dagger-2-DI-Einrichtung
