---
title: "Architecture MVVM sur Android"
category: concepts
tags: [ios-mobile, android, mvvm, viewmodel, livedata, repository, coroutines]
level: 3
source_sha256: 570f6fdb60e291506f3589dce8fbcc1c369cf83a74d1f78897301a258b243c64
translation: machine
translated_at: '2026-10-24'
---
# Architecture MVVM sur Android {#android-mvvm-architecture}

MVVM (Model-View-ViewModel) est l'architecture recommandée pour les applications Android. Le ViewModel survit aux changements de configuration (rotation), LiveData notifie les observateurs actifs, et les coroutines gèrent les opérations asynchrones. Cette entrée couvre le modèle ViewModel, LiveData, les coroutines et la couche Repository.

## Points clés {#key-facts}

- Le ViewModel survit aux changements de configuration (rotation de l'appareil), contrairement à Activity/Fragment
- LiveData notifie automatiquement uniquement les observateurs actifs (sensibles au cycle de vie)
- Modèle : `private MutableLiveData` + `public LiveData` encapsule l'accès en écriture
- `viewModelScope.launch` lie les coroutines au cycle de vie du ViewModel
- Dispatchers : `Main` pour l'UI, `IO` pour le disque et le réseau, `Default` pour les calculs CPU
- Les fonctions `suspend` ne peuvent être appelées que depuis des coroutines ou d'autres fonctions `suspend`
- Le modèle Repository sépare le ViewModel des détails de la source de données

## Modèles {#patterns}

### ViewModel avec LiveData {#viewmodel-with-livedata}

```kotlin
class RecordViewModel(private val app: Application) : AndroidViewModel(app) {

    private val _elapsedTime = MutableLiveData<String>()
    val elapsedTime: LiveData<String>
        get() = _elapsedTime

    private val database = RecordDatabase.getInstance(app).recordDatabaseDao
    val allRecords = database.getAllRecords()   // LiveData from Room

    fun startTimer() {
        viewModelScope.launch {
            saveTime(SystemClock.elapsedRealtime())
        }
    }

    private suspend fun saveTime(triggerTime: Long) =
        withContext(Dispatchers.IO) {
            prefs.edit().putLong(TRIGGER_TIME, triggerTime).apply()
        }

    override fun onCleared() {
        super.onCleared()
        // clean up resources
    }
}
```

### ViewModelFactory (paramètres du constructeur) {#viewmodelfactory-constructor-parameters}

```kotlin
class RecordViewModelFactory(
    private val application: Application
) : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(RecordViewModel::class.java)) {
            return RecordViewModel(application) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
```

### Obtenir le ViewModel dans un Fragment {#getting-viewmodel-in-fragment}

```kotlin
// Legacy approach
val factory = RecordViewModelFactory(requireActivity().application)
viewModel = ViewModelProviders.of(this, factory)
    .get(RecordViewModel::class.java)

// Modern Kotlin extensions
val viewModel: RecordViewModel by viewModels {
    RecordViewModelFactory(requireActivity().application)
}
```

### Observer LiveData {#observing-livedata}

```kotlin
viewModel.elapsedTime.observe(viewLifecycleOwner, Observer { time ->
    timerTextView.text = time
})

viewModel.allRecords.observe(viewLifecycleOwner, Observer { records ->
    adapter.submitList(records)
})
```

### Coroutines Kotlin {#kotlin-coroutines}

```kotlin
// In ViewModel (auto-cancelled when ViewModel cleared)
viewModelScope.launch {
    val result = withContext(Dispatchers.IO) {
        database.insert(recordingItem)
    }
    // back on Main thread here
}

// Manual scope (Service or non-ViewModel)
private val job = Job()
private val uiScope = CoroutineScope(Dispatchers.Main + job)

// Cancel in onDestroy
job.cancel()
```

### Dispatchers {#dispatchers}

| Dispatcher | Utilisé pour |
|------------|--------------|
| `Dispatchers.Main` | Mises à jour de l'UI, LiveData.value |
| `Dispatchers.IO` | Base de données, réseau, E/S fichiers |
| `Dispatchers.Default` | Travaux intensifs en CPU |

### Fonctions suspend {#suspend-functions}

```kotlin
private suspend fun saveTime(triggerTime: Long) =
    withContext(Dispatchers.IO) {
        prefs.edit().putLong(TRIGGER_TIME, triggerTime).apply()
    }

private suspend fun loadTime(): Long =
    withContext(Dispatchers.IO) {
        prefs.getLong(TRIGGER_TIME, 0)
    }
```

### Modèle Repository {#repository-pattern}

```sql
View (Activity/Fragment)
  | observe LiveData / call functions
ViewModel
  | call functions / expose LiveData
Repository
  | fetch from network or database
Remote (Retrofit) + Local (Room)
```

```kotlin
class AccountRepository(
    private val remote: AccountRemote,
    private val local: AccountLocal
) {
    fun login(email: String, password: String): LiveData<Either<Failure, None>> {
        return remote.login(email, password)
    }
}

class AccountViewModel(
    private val repository: AccountRepository
) : ViewModel() {
    private val _loginData = MutableLiveData<None>()
    val loginData: LiveData<None> = _loginData

    fun login(email: String, password: String) {
        viewModelScope.launch {
            repository.login(email, password).collect { result ->
                result.fold(::handleFailure, ::handleLogin)
            }
        }
    }
}
```

### Modèle Either (gestion fonctionnelle des erreurs) {#either-pattern-functional-error-handling}

```kotlin
sealed class Either<out L, out R> {
    data class Left<out L>(val value: L) : Either<L, Nothing>()
    data class Right<out R>(val value: R) : Either<Nothing, R>()

    fun fold(fnL: (L) -> Unit, fnR: (R) -> Unit) = when (this) {
        is Left -> fnL(value)
        is Right -> fnR(value)
    }
}

// Usage
result.fold(
    { failure -> showError(failure) },
    { none -> navigateToHome() }
)
```

### Service Android (travail en arrière-plan) {#android-service-background-work}

```kotlin
class RecordService : Service() {
    private val job = Job()
    private val uiScope = CoroutineScope(Dispatchers.Main + job)

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        startRecording()
        return START_NOT_STICKY
    }

    override fun onDestroy() {
        recorder?.stop()
        job.cancel()
    }
}
```

Enregistrer dans AndroidManifest.xml : `<service android:name=".record.RecordService" />`

```kotlin
// Start/stop service
context.startService(Intent(context, RecordService::class.java))
context.stopService(Intent(context, RecordService::class.java))
```

## Pièges courants {#gotchas}

- `MutableLiveData.value = x` doit être appelé sur le thread principal ; utiliser `postValue()` depuis les threads d'arrière-plan
- `viewModelScope` est automatiquement annulé lorsque le ViewModel est effacé : aucun nettoyage manuel n'est nécessaire
- `AndroidViewModel` fournit une référence à `Application`, contrairement à un `ViewModel` simple : utiliser le modèle factory
- `observe()` nécessite `viewLifecycleOwner` (et non `this`) dans les Fragments pour éviter les fuites mémoire
- `onCleared()` est le dernier callback avant la destruction du ViewModel : annuler ici les travaux en cours
- `START_NOT_STICKY` : le système ne redémarre pas le service s'il est arrêté ; `START_STICKY` : le système le redémarre

## Voir aussi {#see-also}

- [[kotlin-android-fundamentals]] - Bases de Kotlin, structure de projet, composants UI
- [[android-room-database]] - Persistance avec Room et intégration de LiveData
- [[android-retrofit-networking]] - Retrofit avec les coroutines
- [[android-dagger-dependency-injection]] - injection de dépendances dans les ViewModels
