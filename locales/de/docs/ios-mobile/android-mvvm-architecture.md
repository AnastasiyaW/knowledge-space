---
title: "Android-MVVM-Architektur"
category: concepts
tags: [ios-mobile, android, mvvm, viewmodel, livedata, repository, coroutines]
level: 3
source_sha256: 570f6fdb60e291506f3589dce8fbcc1c369cf83a74d1f78897301a258b243c64
translation: machine
translated_at: '2026-10-24'
---
# Android-MVVM-Architektur {#android-mvvm-architecture}

MVVM (Model-View-ViewModel) ist die empfohlene Architektur für Android-Apps. Ein ViewModel überlebt Konfigurationsänderungen (Rotation), LiveData benachrichtigt aktive Observer, und Coroutines übernehmen asynchrone Operationen. Dieser Eintrag behandelt das ViewModel-Muster, LiveData, Coroutines und die Repository-Schicht.

## Wichtige Fakten {#key-facts}

- Ein ViewModel überlebt Konfigurationsänderungen (Gerätrotation), Activity/Fragment hingegen nicht
- LiveData benachrichtigt automatisch nur aktive (lifecycle-aware) Observer
- Muster: `private MutableLiveData` + `public LiveData` kapselt den Schreibzugriff
- `viewModelScope.launch` bindet Coroutines an den Lebenszyklus des ViewModels
- Dispatcher: `Main` für die UI, `IO` für Datenträger und Netzwerk, `Default` für CPU-Arbeit
- `suspend`-Funktionen können nur aus Coroutines oder anderen `suspend`-Funktionen aufgerufen werden
- Das Repository-Muster trennt das ViewModel von den Details der Datenquelle

## Muster {#patterns}

### ViewModel mit LiveData {#viewmodel-with-livedata}

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

### ViewModelFactory (Konstruktorparameter) {#viewmodelfactory-constructor-parameters}

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

### ViewModel in einem Fragment abrufen {#getting-viewmodel-in-fragment}

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

### LiveData beobachten {#observing-livedata}

```kotlin
viewModel.elapsedTime.observe(viewLifecycleOwner, Observer { time ->
    timerTextView.text = time
})

viewModel.allRecords.observe(viewLifecycleOwner, Observer { records ->
    adapter.submitList(records)
})
```

### Kotlin-Coroutines {#kotlin-coroutines}

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

### Dispatcher {#dispatchers}

| Dispatcher | Verwendung für |
|------------|----------------|
| `Dispatchers.Main` | UI-Aktualisierungen, LiveData.value |
| `Dispatchers.IO` | Datenbank, Netzwerk, Datei-I/O |
| `Dispatchers.Default` | CPU-intensive Arbeit |

### suspend-Funktionen {#suspend-functions}

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

### Repository-Muster {#repository-pattern}

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

### Either-Muster (funktionale Fehlerbehandlung) {#either-pattern-functional-error-handling}

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

### Android-Service (Hintergrundarbeit) {#android-service-background-work}

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

In der AndroidManifest.xml registrieren: `<service android:name=".record.RecordService" />`

```kotlin
// Start/stop service
context.startService(Intent(context, RecordService::class.java))
context.stopService(Intent(context, RecordService::class.java))
```

## Fallstricke {#gotchas}

- `MutableLiveData.value = x` muss im Main-Thread aufgerufen werden; aus Hintergrund-Threads `postValue()` verwenden
- `viewModelScope` wird automatisch abgebrochen, wenn das ViewModel geleert wird – keine manuelle Bereinigung nötig
- `AndroidViewModel` stellt eine `Application`-Referenz bereit, ein einfaches `ViewModel` nicht – dafür das Factory-Muster verwenden
- `observe()` erfordert in Fragments `viewLifecycleOwner` (nicht `this`), um Speicherlecks zu vermeiden
- `onCleared()` ist der letzte Callback, bevor das ViewModel zerstört wird – laufende Arbeit hier abbrechen
- `START_NOT_STICKY` – das System startet den Service nach einem Beenden nicht neu; `START_STICKY` – das System startet ihn neu

## Siehe auch {#see-also}

- [[kotlin-android-fundamentals]] - Kotlin-Grundlagen, Projektstruktur, UI-Komponenten
- [[android-room-database]] - Room-Persistenz mit LiveData-Integration
- [[android-retrofit-networking]] - Retrofit mit Coroutines
- [[android-dagger-dependency-injection]] - Abhängigkeiten in ViewModels injizieren
