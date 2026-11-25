---
title: "Fragments Android et Navigation Component"
category: concepts
tags: [java-spring, android, fragments, navigation, view-binding, back-stack]
level: 3
source_sha256: bd97da5e6a0668990e24cc5eb374e074663a604a4be2d8eef5a822bf37a61e6c
translation: machine
translated_at: '2026-10-24'
---
# Fragments Android et Navigation Component {#android-fragments-and-navigation-component}

Cycle de vie des Fragments, communication entre Fragments via un ViewModel partagé, Jetpack Navigation Component, Safe Args, View Binding, et le pattern d'architecture à Activity unique.

## Points clés {#key-facts}

- Fragment = portion d'UI réutilisable au sein d'une Activity, dispose de son propre cycle de vie
- Cycle de vie du Fragment : `onAttach` -> `onCreate` -> `onCreateView` -> `onViewCreated` -> ... -> `onDestroyView` -> `onDestroy` -> `onDetach`
- `onDestroyView` détruit la vue mais le Fragment survit : la vue peut être recréée plus tard
- Le Navigation Component gère les transactions de Fragments, la back stack et le passage d'arguments
- Le plugin Safe Args génère des classes typées pour passer des arguments entre destinations
- View Binding remplace `findViewById` par des classes de binding générées
- Pattern moderne : Activity unique + plusieurs Fragments

## Patterns {#patterns}

### Fragment avec View Binding {#fragment-with-view-binding}
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

### ViewModel partagé pour la communication entre Fragments {#shared-viewmodel-for-fragment-communication}
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

### Graphe de navigation {#navigation-graph}
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

### Navigation avec Safe Args {#safe-args-navigation}
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

### Navigation inférieure avec NavController {#bottom-navigation-with-navcontroller}
```kotlin
val navController = findNavController(R.id.navHostFragment)
binding.bottomNav.setupWithNavController(navController)
```

### Configuration du View Binding {#view-binding-setup}
```gradle
android { buildFeatures { viewBinding true } }
```

## Pièges {#gotchas}

- `_binding = null` dans `onDestroyView()` est essentiel : sans cela, le Fragment conserve une référence vers des vues détruites
- Utiliser `viewLifecycleOwner` (et non `this`) lors de l'observation de LiveData dans un Fragment : cela évite les mises à jour de vues détachées
- `requireContext()` lève une exception si le Fragment n'est pas attaché : utiliser `context` (nullable) dans les callbacks
- `addToBackStack(null)` dans les transactions de Fragments manuelles permet la navigation arrière
- Recréation du Fragment lors d'un changement de configuration : utiliser le ViewModel pour l'état persistant, et non les arguments

## Voir aussi {#see-also}

- [[android-activity-lifecycle]] - Activity qui héberge les Fragments
- [[android-architecture-mvvm]] - Intégration du ViewModel
- [[android-jetpack-compose]] - Navigation Compose comme alternative
