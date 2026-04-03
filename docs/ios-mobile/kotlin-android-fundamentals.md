---
title: Kotlin and Android Fundamentals
category: concepts
tags: [ios-mobile, android, kotlin, project-structure, build-gradle, data-class, coroutines]
---

# Kotlin and Android Fundamentals

Kotlin is the primary language for Android development. This entry covers Kotlin language basics, Android project structure, build.gradle configuration, Activities, Fragments, navigation, and UI components.

## Key Facts

- `data class` auto-generates `equals()`, `hashCode()`, `toString()`, `copy()`
- `companion object` provides static-like members accessed via class name
- `lateinit var` declares a non-nullable property initialized later (not in constructor)
- `@Volatile` guarantees value is read from main memory, not CPU cache - critical for singletons
- `synchronized(this)` prevents simultaneous access from multiple threads
- Android uses XML layouts (`res/layout/`) while SwiftUI uses declarative code
- `SharedPreferences` provides simple key-value persistent storage

## Patterns

### Project Structure

```
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

### build.gradle Key Dependencies

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

### data class

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

### Fragment Lifecycle

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

### Activity Navigation

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

### Navigation Component

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

### ConstraintLayout XML

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

### RecyclerView Adapter

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

### Setup in Fragment

```kotlin
val adapter = CurrencyAdapter(emptyList(), requireContext())
recyclerView.layoutManager = LinearLayoutManager(context)
recyclerView.adapter = adapter

viewModel.coins.observe(viewLifecycleOwner) { coins ->
    adapter.updateItems(coins)
}
```

### AlertDialog

```kotlin
AlertDialog.Builder(activity)
    .setTitle(R.string.dialog_title)
    .setMessage(R.string.dialog_message)
    .setPositiveButton(R.string.yes) { dialog, _ -> dialog.cancel() }
    .setNegativeButton(R.string.no) { dialog, _ -> dialog.cancel() }
    .show()
```

### SharedPreferences

```kotlin
val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
prefs.edit().putLong("TRIGGER_TIME", value).apply()  // write
val time = prefs.getLong("TRIGGER_TIME", 0L)          // read with default
```

### Toast

```kotlin
Toast.makeText(context, "Message", Toast.LENGTH_SHORT).show()
```

### String Resources

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

### Glide (Image Loading)

```kotlin
Glide.with(context)
    .load(imageUrl)
    .placeholder(R.drawable.placeholder)
    .error(R.drawable.error_image)
    .into(imageView)
```

## Gotchas

- `lateinit` properties crash with `UninitializedPropertyAccessException` if accessed before initialization
- `notifyDataSetChanged()` redraws all items - use `DiffUtil` for efficient partial updates in production
- `onActivityCreated()` is deprecated - use `onViewCreated()` for modern Fragment lifecycle
- Android XML layouts are verbose compared to SwiftUI declarative code
- `kapt` plugin required for annotation processing (Room, Dagger) - without it, code generation fails
- `startActivityForResult()` is deprecated - use Activity Result API in modern code

## See Also

- [[android-mvvm-architecture]] - ViewModel, LiveData, Repository pattern
- [[android-room-database]] - Room persistence framework
- [[android-retrofit-networking]] - Retrofit REST API client
- [[android-dagger-dependency-injection]] - Dagger 2 DI setup
