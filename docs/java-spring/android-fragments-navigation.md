---
title: Android Fragments and Navigation Component
category: concepts
tags: [java-spring, android, fragments, navigation, view-binding, back-stack]
---

# Android Fragments and Navigation Component

Fragment lifecycle, Fragment communication via shared ViewModel, Jetpack Navigation Component, Safe Args, View Binding, and the single-Activity architecture pattern.

## Key Facts

- Fragment = reusable UI portion within an Activity, has its own lifecycle
- Fragment lifecycle: `onAttach` -> `onCreate` -> `onCreateView` -> `onViewCreated` -> ... -> `onDestroyView` -> `onDestroy` -> `onDetach`
- `onDestroyView` destroys the view but Fragment survives - can recreate view later
- Navigation Component manages fragment transactions, back stack, and argument passing
- Safe Args plugin generates type-safe classes for passing arguments between destinations
- View Binding replaces `findViewById` with generated binding classes
- Modern pattern: Single Activity + Multiple Fragments

## Patterns

### Fragment with View Binding
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

### Shared ViewModel for Fragment Communication
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

### Navigation Graph
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

### Safe Args Navigation
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

### Bottom Navigation with NavController
```kotlin
val navController = findNavController(R.id.navHostFragment)
binding.bottomNav.setupWithNavController(navController)
```

### View Binding Setup
```gradle
android { buildFeatures { viewBinding true } }
```

## Gotchas

- `_binding = null` in `onDestroyView()` is critical - without it, Fragment holds reference to destroyed views
- Use `viewLifecycleOwner` (not `this`) when observing LiveData in Fragments - prevents updates to detached views
- `requireContext()` throws if Fragment is not attached - use `context` (nullable) in callbacks
- `addToBackStack(null)` in manual Fragment transactions enables back navigation
- Fragment recreation on config change: use ViewModel for persistent state, not arguments

## See Also

- [[android-activity-lifecycle]] - Activity that hosts Fragments
- [[android-architecture-mvvm]] - ViewModel integration
- [[android-jetpack-compose]] - Compose Navigation as alternative
