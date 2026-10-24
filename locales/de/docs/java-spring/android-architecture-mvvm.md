---
title: "Android-Architektur - MVP, MVVM, ViewModel, LiveData"
category: concepts
tags: [java-spring, android, mvvm, mvp, viewmodel, livedata, architecture]
level: 3
source_sha256: d78305fa6c2277d0c1ee56863a464e666e0ef575c77e57447000fcd88b726b7d
translation: machine
translated_at: '2026-10-24'
---
# Android-Architektur - MVP, MVVM, ViewModel, LiveData {#android-architecture-mvp-mvvm-viewmodel-livedata}

Architekturmuster für Android: MVP (Model-View-Presenter) vs. MVVM (Model-View-ViewModel), Jetpack ViewModel, LiveData, Repository-Pattern und ViewModelFactory.

## Wichtige Fakten {#key-facts}

- Anti-Pattern "God Activity": gesamte Logik in der Activity - nicht testbar, schwer lesbar, schwer wartbar
- MVP: Der Presenter hält eine Referenz auf die View und muss sie bei `onDestroy` auf null setzen, um Leaks zu vermeiden
- MVVM (von Google empfohlen): Das ViewModel hat KEINE Referenz auf die View und übersteht Konfigurationsänderungen
- Der Lebenszyklus von `ViewModel` ist an Activity/Fragment gebunden - er übersteht Rotationen
- `LiveData` ist ein lebenszyklusbewusstes, beobachtbares Objekt - Observer erhalten Updates nur, wenn sie aktiv sind (STARTED/RESUMED)
- `MutableLiveData` ist im ViewModel schreibbar; `LiveData` wird schreibgeschützt an die View weitergegeben
- `setValue()` = nur Main-Thread; `postValue()` = beliebiger Thread

## Muster {#patterns}

### MVP-Muster {#mvp-pattern}
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

### MVVM-Muster (empfohlen) {#mvvm-pattern-recommended}
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

### ViewModelFactory (Konstruktorparameter) {#viewmodelfactory-constructor-parameters}
```kotlin
class UserViewModelFactory(private val repo: UserRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UserViewModel(repo) as T
    }
}
val factory = UserViewModelFactory(repository)
val vm = ViewModelProvider(this, factory).get(UserViewModel::class.java)
```

### Repository-Pattern (Single Source of Truth) {#repository-pattern-single-source-of-truth}
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

### Vergleich MVP vs. MVVM {#mvp-vs-mvvm-comparison}
| Aspekt | MVP | MVVM |
|--------|-----|------|
| Kopplung View-Logik | Presenter referenziert View | Keine Referenz auf View |
| Lifecycle-Behandlung | Manuell (bei onDestroy auf null setzen) | Automatisch (übersteht Konfigurationsänderungen) |
| Testing | View-Interface mocken | ViewModel direkt testen |
| Datenfluss | Presenter ruft View-Methoden auf | View beobachtet LiveData |
| Boilerplate | Mehr (Contracts) | Weniger |
| Von Google empfohlen | Nein | Ja |

## Stolperfallen {#gotchas}

- Das ViewModel darf KEINE Referenzen auf Activity/Context halten - das verursacht Memory Leaks (falls ein Context benötigt wird, `AndroidViewModel` verwenden)
- `LiveData.observe()` benötigt einen `LifecycleOwner` - im Fragment `viewLifecycleOwner` verwenden, nicht `this`
- `MutableLiveData.setValue()` auf einem Hintergrund-Thread führt zum Absturz - aus dem Hintergrund `postValue()` verwenden
- Der MVP-Presenter muss die View-Referenz in `onDestroy()` auf null setzen, sonst leakt die gesamte Activity

## Siehe auch {#see-also}

- [[kotlin-coroutines]] - Asynchrone Operationen im ViewModel
- [[android-fragments-navigation]] - Fragment-Integration mit geteiltem ViewModel
- [[android-jetpack-compose]] - Zustandsverwaltung in Compose
