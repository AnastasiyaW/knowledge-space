---
title: "Architecture Android - MVP, MVVM, ViewModel, LiveData"
category: concepts
tags: [java-spring, android, mvvm, mvp, viewmodel, livedata, architecture]
level: 3
source_sha256: d78305fa6c2277d0c1ee56863a464e666e0ef575c77e57447000fcd88b726b7d
translation: machine
translated_at: '2026-10-24'
---
# Architecture Android - MVP, MVVM, ViewModel, LiveData {#android-architecture-mvp-mvvm-viewmodel-livedata}

Patrons architecturaux pour Android : MVP (Model-View-Presenter) contre MVVM (Model-View-ViewModel), Jetpack ViewModel, LiveData, patron Repository et ViewModelFactory.

## Points clés {#key-facts}

- Anti-patron « God Activity » : toute la logique dans l'Activity, ce qui la rend non testable, illisible et difficile à maintenir
- MVP : le Presenter détient une référence à la View et doit la passer à null lors de la destruction pour éviter les fuites mémoire
- MVVM (recommandé par Google) : le ViewModel n'a AUCUNE référence à la View et survit aux changements de configuration
- Le cycle de vie de `ViewModel` est lié à l'Activity ou au Fragment : il survit à la rotation
- `LiveData` est un observable sensible au cycle de vie : les observateurs ne reçoivent les mises à jour que lorsqu'ils sont actifs (STARTED/RESUMED)
- `MutableLiveData` est modifiable à l'intérieur du ViewModel ; `LiveData` est exposé en lecture seule à la View
- `setValue()` = thread principal uniquement ; `postValue()` = tout thread

## Patrons {#patterns}

### Patron MVP {#mvp-pattern}
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

### Patron MVVM (recommandé) {#mvvm-pattern-recommended}
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

### ViewModelFactory (paramètres du constructeur) {#viewmodelfactory-constructor-parameters}
```kotlin
class UserViewModelFactory(private val repo: UserRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UserViewModel(repo) as T
    }
}
val factory = UserViewModelFactory(repository)
val vm = ViewModelProvider(this, factory).get(UserViewModel::class.java)
```

### Patron Repository (source unique de vérité) {#repository-pattern-single-source-of-truth}
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

### Comparaison MVP et MVVM {#mvp-vs-mvvm-comparison}
| Aspect | MVP | MVVM |
|--------|-----|------|
| Couplage View-Logique | Le Presenter référence la View | Aucune référence à la View |
| Gestion du cycle de vie | Manuelle (null à la destruction) | Automatique (survit aux changements de configuration) |
| Tests | Mocker l'interface View | Tester le ViewModel directement |
| Flux de données | Le Presenter appelle les méthodes de la View | La View observe le LiveData |
| Code répétitif | Plus (contrats) | Moins |
| Recommandé par Google | Non | Oui |

## Pièges {#gotchas}

- Le ViewModel ne doit PAS conserver de références à l'Activity ou au Context, sous peine de fuites mémoire (utiliser `AndroidViewModel` si un contexte est nécessaire)
- `LiveData.observe()` requiert un `LifecycleOwner` : dans un Fragment, utiliser `viewLifecycleOwner`, et non `this`
- Appeler `MutableLiveData.setValue()` depuis un thread d'arrière-plan provoque un plantage : utiliser `postValue()` depuis un thread d'arrière-plan
- Le Presenter MVP doit mettre à null la référence à la View dans `onDestroy()`, faute de quoi il retient l'Activity entière en mémoire

## Voir aussi {#see-also}

- [[kotlin-coroutines]] - Opérations asynchrones dans le ViewModel
- [[android-fragments-navigation]] - Intégration des Fragments avec un ViewModel partagé
- [[android-jetpack-compose]] - Gestion de l'état dans Compose
