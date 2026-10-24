---
title: "Android-Fragments und Navigation Component"
category: concepts
tags: [java-spring, android, fragments, navigation, view-binding, back-stack]
level: 3
source_sha256: bd97da5e6a0668990e24cc5eb374e074663a604a4be2d8eef5a822bf37a61e6c
translation: machine
translated_at: '2026-10-24'
---
# Android-Fragments und Navigation Component {#android-fragments-and-navigation-component}

Fragment-Lebenszyklus, Fragment-Kommunikation über ein gemeinsames ViewModel, Jetpack Navigation Component, Safe Args, View Binding und das Architekturmuster einer einzigen Activity.

## Key Facts {#key-facts}

- Fragment = wiederverwendbarer UI-Teil innerhalb einer Activity, besitzt einen eigenen Lebenszyklus
- Fragment-Lebenszyklus: `onAttach` -> `onCreate` -> `onCreateView` -> `onViewCreated` -> ... -> `onDestroyView` -> `onDestroy` -> `onDetach`
- `onDestroyView` zerstört die View, das Fragment bleibt jedoch bestehen - die View kann später neu erstellt werden
- Navigation Component verwaltet Fragment-Transaktionen, den Back Stack und die Übergabe von Argumenten
- Safe-Args-Plugin erzeugt typsichere Klassen für die Übergabe von Argumenten zwischen Destinations
- View Binding ersetzt `findViewById` durch generierte Binding-Klassen
- Modernes Muster: Single Activity + mehrere Fragments

## Patterns {#patterns}

### Fragment with View Binding {#fragment-with-view-binding}
```kotlin
class UserListFragment : Fragment() {
    private var _binding: FragmentUserListBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                               savedInstanceState: Bundle?): View {
        _binding = FragmentUserListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.recyclerView.adapter = adapter
        binding.recyclerView.layoutManager = LinearLayoutManager(requireContext())
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null  // prevent memory leak
    }
}
```

### Shared ViewModel for Fragment Communication {#shared-viewmodel-for-fragment-communication}
```kotlin
class SharedViewModel : ViewModel() {
    val selectedUser = MutableLiveData<User>()
}

// Fragment A - sets data
class ListFragment : Fragment() {
    private val sharedVM: SharedViewModel by activityViewModels()
    fun onUserClicked(user: User) { sharedVM.selectedUser.value = user }
}

// Fragment B - observes data
class DetailFragment : Fragment() {
    private val sharedVM: SharedViewModel by activityViewModels()
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        sharedVM.selectedUser.observe(viewLifecycleOwner) { user ->
            binding.tvName.text = user.name
        }
    }
}
```

### Navigation Graph {#navigation-graph}
```xml
<navigation app:startDestination="@id/listFragment">
    <fragment android:id="@+id/listFragment"
        android:name="com.example.ListFragment">
        <action android:id="@+id/action_list_to_detail"
            app:destination="@id/detailFragment" />
    </fragment>
    <fragment android:id="@+id/detailFragment"
        android:name="com.example.DetailFragment">
        <argument android:name="userId" app:argType="integer" />
    </fragment>
</navigation>
```

### Safe Args Navigation {#safe-args-navigation}
```kotlin
// Navigate with type-safe args
val action = ListFragmentDirections.actionListToDetail(userId = user.id)
findNavController().navigate(action)

// Receive args
class DetailFragment : Fragment() {
    private val args: DetailFragmentArgs by navArgs()
    override fun onViewCreated(...) { val id = args.userId }
}
```

### Bottom Navigation with NavController {#bottom-navigation-with-navcontroller}
```kotlin
val navController = findNavController(R.id.navHostFragment)
binding.bottomNav.setupWithNavController(navController)
```

### View Binding Setup {#view-binding-setup}
```gradle
android { buildFeatures { viewBinding true } }
```

## Gotchas {#gotchas}

- `_binding = null` in `onDestroyView()` ist entscheidend - ohne diesen Schritt hält das Fragment eine Referenz auf zerstörte Views
- Verwende `viewLifecycleOwner` (nicht `this`), wenn LiveData in Fragments beobachtet wird - so werden Aktualisierungen auf losgelöste Views verhindert
- `requireContext()` wirft eine Exception, wenn das Fragment nicht angehängt ist - in Callbacks stattdessen `context` (nullable) verwenden
- `addToBackStack(null)` in manuellen Fragment-Transaktionen ermöglicht die Rücknavigation
- Fragment-Neuerstellung bei Konfigurationsänderung: Für persistenten Zustand ein ViewModel verwenden, nicht Argumente

## See Also {#see-also}

- [[android-activity-lifecycle]] - Activity, die Fragments hostet
- [[android-architecture-mvvm]] - ViewModel-Integration
- [[android-jetpack-compose]] - Compose Navigation als Alternative
