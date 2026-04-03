---
title: Android MVVM Architecture
category: concepts
tags: [ios-mobile, android, mvvm, viewmodel, livedata, repository, coroutines]
---

# Android MVVM Architecture

MVVM (Model-View-ViewModel) is the recommended architecture for Android apps. ViewModel survives configuration changes (rotation), LiveData notifies active observers, and coroutines handle async operations. This entry covers the ViewModel pattern, LiveData, coroutines, and the Repository layer.

## Key Facts

- ViewModel survives configuration changes (device rotation) - Activity/Fragment does not
- LiveData notifies only active (lifecycle-aware) observers automatically
- Pattern: `private MutableLiveData` + `public LiveData` encapsulates write access
- `viewModelScope.launch` ties coroutines to ViewModel lifecycle
- Dispatchers: `Main` for UI, `IO` for disk/network, `Default` for CPU work
- `suspend` functions can only be called from coroutines or other suspend functions
- Repository pattern separates ViewModel from data source details

## Patterns

### ViewModel with LiveData

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

### ViewModelFactory (Constructor Parameters)

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

### Getting ViewModel in Fragment

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

### Observing LiveData

```kotlin
viewModel.elapsedTime.observe(viewLifecycleOwner, Observer { time ->
    timerTextView.text = time
})

viewModel.allRecords.observe(viewLifecycleOwner, Observer { records ->
    adapter.submitList(records)
})
```

### Kotlin Coroutines

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

### Dispatchers

| Dispatcher | Use for |
|------------|---------|
| `Dispatchers.Main` | UI updates, LiveData.value |
| `Dispatchers.IO` | Database, network, file I/O |
| `Dispatchers.Default` | CPU-intensive work |

### suspend Functions

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

### Repository Pattern

```
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

### Either Pattern (Functional Error Handling)

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

### Android Service (Background Work)

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

Register in AndroidManifest.xml: `<service android:name=".record.RecordService" />`

```kotlin
// Start/stop service
context.startService(Intent(context, RecordService::class.java))
context.stopService(Intent(context, RecordService::class.java))
```

## Gotchas

- `MutableLiveData.value = x` must be called on the main thread; use `postValue()` from background threads
- `viewModelScope` is automatically cancelled when ViewModel is cleared - no manual cleanup needed
- `AndroidViewModel` provides `Application` reference; plain `ViewModel` does not - use factory pattern
- `observe()` requires `viewLifecycleOwner` (not `this`) in Fragments to avoid memory leaks
- `onCleared()` is the last callback before ViewModel is destroyed - cancel ongoing work here
- `START_NOT_STICKY` - system does not restart service if killed; `START_STICKY` - system restarts it

## See Also

- [[kotlin-android-fundamentals]] - Kotlin basics, project structure, UI components
- [[android-room-database]] - Room persistence with LiveData integration
- [[android-retrofit-networking]] - Retrofit with coroutines
- [[android-dagger-dependency-injection]] - injecting dependencies into ViewModels
