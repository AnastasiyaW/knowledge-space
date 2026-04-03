---
title: Android Architecture - MVP, MVVM, ViewModel, LiveData
category: concepts
tags: [java-spring, android, mvvm, mvp, viewmodel, livedata, architecture]
---

# Android Architecture - MVP, MVVM, ViewModel, LiveData

Architectural patterns for Android: MVP (Model-View-Presenter) vs MVVM (Model-View-ViewModel), Jetpack ViewModel, LiveData, Repository pattern, and ViewModelFactory.

## Key Facts

- "God Activity" anti-pattern: all logic in Activity - untestable, unreadable, unmaintainable
- MVP: Presenter holds View reference, must null on destroy to prevent leaks
- MVVM (recommended by Google): ViewModel has NO reference to View, survives config changes
- `ViewModel` lifecycle is tied to Activity/Fragment - survives rotation
- `LiveData` is lifecycle-aware observable - observers only receive updates when active (STARTED/RESUMED)
- `MutableLiveData` writable inside ViewModel; `LiveData` read-only exposed to View
- `setValue()` = main thread only; `postValue()` = any thread

## Patterns

### MVP Pattern
```java
// Contract
public interface UserContract {
    interface View { void showUsers(List<User> users); void showError(String msg); }
    interface Presenter { void loadUsers(); void onDestroy(); }
}

// Presenter holds View reference
public class UserPresenter implements UserContract.Presenter {
    private UserContract.View view;
    @Override public void onDestroy() { view = null; }  // prevent leak
}

// Activity implements View
public class UserActivity extends AppCompatActivity implements UserContract.View {
    @Override public void showUsers(List<User> users) { adapter.setUsers(users); }
}
```

### MVVM Pattern (Recommended)
```kotlin
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users

    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading

    fun loadUsers() {
        viewModelScope.launch {
            _loading.value = true
            try { _users.value = repository.getUsers() }
            catch (e: Exception) { /* handle error */ }
            finally { _loading.value = false }
        }
    }
}

// Activity observes
class UserActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        val viewModel = ViewModelProvider(this).get(UserViewModel::class.java)
        viewModel.users.observe(this) { users -> adapter.setUsers(users) }
        viewModel.loading.observe(this) { isLoading ->
            progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        }
        viewModel.loadUsers()
    }
}
```

### ViewModelFactory (Constructor Parameters)
```kotlin
class UserViewModelFactory(private val repo: UserRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UserViewModel(repo) as T
    }
}
val factory = UserViewModelFactory(repository)
val vm = ViewModelProvider(this, factory).get(UserViewModel::class.java)
```

### Repository Pattern (Single Source of Truth)
```kotlin
class UserRepository(private val api: ApiService, private val dao: UserDao) {
    suspend fun getUsers(): List<User> = try {
        val remote = api.getUsers()
        dao.insertAll(remote)  // cache
        remote
    } catch (e: Exception) {
        dao.getAllUsers()       // fallback to cache
    }
}
```

### MVP vs MVVM Comparison
| Aspect | MVP | MVVM |
|--------|-----|------|
| View-Logic coupling | Presenter references View | No reference to View |
| Lifecycle handling | Manual (null on destroy) | Automatic (survives config changes) |
| Testing | Mock View interface | Test ViewModel directly |
| Data flow | Presenter calls View methods | View observes LiveData |
| Boilerplate | More (contracts) | Less |
| Google recommended | No | Yes |

## Gotchas

- ViewModel must NOT hold Activity/Context references - causes memory leaks (use `AndroidViewModel` if context needed)
- `LiveData.observe()` requires `LifecycleOwner` - in Fragment use `viewLifecycleOwner`, not `this`
- `MutableLiveData.setValue()` on background thread crashes - use `postValue()` from background
- MVP Presenter must null the View reference in `onDestroy()` or it leaks the entire Activity

## See Also

- [[kotlin-coroutines]] - Async operations in ViewModel
- [[android-fragments-navigation]] - Fragment integration with shared ViewModel
- [[android-jetpack-compose]] - State management in Compose
