---
title: Android Architecture (MVVM, Clean Architecture)
category: concepts
tags: [android, mvvm, viewmodel, livedata, stateflow, clean-architecture, fragments, navigation]
---
# Android Architecture (MVVM, Clean Architecture)

## Key Facts

- Modern Android uses **MVVM** (Model-View-ViewModel) architecture - separates UI from business logic
- **ViewModel** survives configuration changes (screen rotation); holds UI state, NOT references to Views
- **LiveData** - lifecycle-aware observable; **StateFlow** (Kotlin) - coroutine-based alternative, preferred in new code
- **Fragment** - reusable UI component with its own lifecycle, hosted inside an Activity
- Three-layer **Clean Architecture**: Presentation (UI/ViewModel), Domain (use cases), Data (repositories/DB/network)
- **Navigation Component** manages fragment transitions, back stack, and deep links via nav_graph.xml
- **Data Binding** / **View Binding** connects XML layouts to data sources declaratively
- **RecyclerView** + **DiffUtil** for efficient list rendering with automatic change detection
- Events flow from View -> ViewModel -> Repository; data flows Repository -> ViewModel -> View
- See [[android-layouts]] for XML layout structure
- See [[android-room-database]] for local data persistence

## Patterns

### ViewModel with StateFlow

```kotlin
class CharacterListViewModel(
    private val repository: CharacterRepository
) : ViewModel() {

    // Internal mutable state
    private val _characters = MutableStateFlow<List<Character>>(emptyList())
    // External read-only state
    val characters: StateFlow<List<Character>> = _characters.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        loadCharacters()
    }

    fun loadCharacters() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _characters.value = repository.getCharacters()
                _error.value = null
            } catch (e: Exception) {
                _error.value = e.message
            } finally {
                _isLoading.value = false
            }
        }
    }
}
```

### Fragment observing ViewModel

```kotlin
class CharacterListFragment : Fragment(R.layout.fragment_character_list) {

    private val viewModel: CharacterListViewModel by viewModels()
    private lateinit var adapter: CharacterAdapter

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        adapter = CharacterAdapter { character ->
            // Navigate to detail
            val action = CharacterListFragmentDirections
                .actionListToDetail(character.id)
            findNavController().navigate(action)
        }

        binding.recyclerView.adapter = adapter
        binding.recyclerView.layoutManager = LinearLayoutManager(requireContext())

        // Collect StateFlow in lifecycle-aware scope
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                launch { viewModel.characters.collect { adapter.submitList(it) } }
                launch { viewModel.isLoading.collect { binding.progress.isVisible = it } }
                launch { viewModel.error.collect { it?.let { showError(it) } } }
            }
        }
    }
}
```

### RecyclerView Adapter with DiffUtil

```kotlin
class CharacterAdapter(
    private val onClick: (Character) -> Unit
) : ListAdapter<Character, CharacterAdapter.ViewHolder>(DiffCallback) {

    class ViewHolder(val binding: ItemCharacterBinding) : RecyclerView.ViewHolder(binding.root)

    object DiffCallback : DiffUtil.ItemCallback<Character>() {
        override fun areItemsTheSame(old: Character, new: Character) = old.id == new.id
        override fun areContentsTheSame(old: Character, new: Character) = old == new
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemCharacterBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = getItem(position)
        holder.binding.nameText.text = item.name
        holder.binding.houseText.text = item.house
        Glide.with(holder.itemView).load(item.imageUrl).into(holder.binding.avatar)
        holder.itemView.setOnClickListener { onClick(item) }
    }
}
```

### Clean Architecture layers

```
Presentation Layer (UI)
  - Fragment / Activity
  - ViewModel
  - Adapters

Domain Layer (Business Logic)
  - Use Cases / Interactors
  - Domain Models
  - Repository Interfaces

Data Layer
  - Repository Implementations
  - Network (Retrofit)
  - Local DB (Room)
  - Mappers (Entity <-> Domain)
```

```kotlin
// Domain layer - repository interface
interface CharacterRepository {
    suspend fun getCharacters(): List<Character>
    suspend fun getCharacterById(id: Int): Character
}

// Data layer - implementation
class CharacterRepositoryImpl(
    private val api: HarryPotterApi,
    private val dao: CharacterDao,
    private val mapper: CharacterMapper
) : CharacterRepository {

    override suspend fun getCharacters(): List<Character> {
        return try {
            val remote = api.getCharacters()
            dao.insertAll(remote.map { mapper.toEntity(it) })
            remote.map { mapper.toDomain(it) }
        } catch (e: Exception) {
            // Fallback to cached data
            dao.getAll().map { mapper.toDomain(it) }
        }
    }
}
```

### Navigation Component

```xml
<!-- res/navigation/nav_graph.xml -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    app:startDestination="@id/characterListFragment">

    <fragment
        android:id="@+id/characterListFragment"
        android:name="com.example.CharacterListFragment"
        android:label="Characters">
        <action
            android:id="@+id/action_list_to_detail"
            app:destination="@id/characterDetailFragment" />
    </fragment>

    <fragment
        android:id="@+id/characterDetailFragment"
        android:name="com.example.CharacterDetailFragment"
        android:label="Detail">
        <argument
            android:name="characterId"
            app:argType="integer" />
    </fragment>
</navigation>
```

### Retrofit for network calls

```kotlin
interface HarryPotterApi {
    @GET("characters")
    suspend fun getCharacters(): List<CharacterDto>

    @GET("characters/{id}")
    suspend fun getCharacterById(@Path("id") id: Int): CharacterDto
}

// Setup
val retrofit = Retrofit.Builder()
    .baseUrl("https://hp-api.herokuapp.com/api/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(HarryPotterApi::class.java)
```

## Gotchas

- **Symptom**: ViewModel holds reference to Activity/Fragment and causes memory leak -> **Cause**: Passing Context or View to ViewModel -> **Fix**: ViewModel must NEVER reference Views or Activity; use `AndroidViewModel` if Application context is needed
- **Symptom**: UI doesn't update on configuration change -> **Cause**: Data stored in Fragment/Activity instead of ViewModel -> **Fix**: Move all UI state to ViewModel; observe from View layer
- **Symptom**: StateFlow doesn't emit to new subscribers -> **Cause**: StateFlow replays only last value; events (like toast) get lost -> **Fix**: Use `SharedFlow` for one-time events, or Channel with `receiveAsFlow()`
- **Symptom**: Fragment transactions crash with "state loss" -> **Cause**: Committing after `onSaveInstanceState()` -> **Fix**: Use `commitAllowingStateLoss()` or Navigation Component (handles this automatically)
- **Symptom**: RecyclerView items don't update -> **Cause**: DiffUtil `areContentsTheSame` returns true incorrectly -> **Fix**: Implement data class with proper `equals()`, or compare all relevant fields

## See Also

- [[android-layouts]] - XML layout structure for fragments
- [[android-room-database]] - Local persistence in data layer
- [[kotlin-fundamentals]] - Kotlin coroutines power ViewModel async operations
- [[design-patterns-behavioral]] - Observer pattern underlies LiveData/StateFlow
- Android Docs: [App Architecture](https://developer.android.com/topic/architecture)
- Android Docs: [ViewModel](https://developer.android.com/topic/libraries/architecture/viewmodel)
- Android Docs: [Navigation](https://developer.android.com/guide/navigation)
