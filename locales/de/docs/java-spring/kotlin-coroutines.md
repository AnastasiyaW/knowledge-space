---
title: "Kotlin-Coroutinen, Flow und asynchrone Muster"
category: concepts
tags: [java-spring, kotlin, coroutines, flow, async, dispatchers, state-flow]
level: 3
source_sha256: 252f61574762648da0b7e4e3af9a99fe3a5a999032991ad610afdfe26978b0c9
translation: machine
translated_at: '2026-10-24'
---
# Kotlin-Coroutinen, Flow und asynchrone Muster {#kotlin-coroutines-flow-and-async-patterns}

Kotlin-Coroutinen für asynchrone Programmierung: Suspend-Funktionen, Dispatcher, Scopes, Structured Concurrency, Fehlerbehandlung, Flow für reaktive Streams, StateFlow und Android-Integration.

## Key Facts {#key-facts}

- Coroutinen sind leichtgewichtig (wenige hundert Bytes statt ~1 MB pro Thread) - Millionen sind möglich
- `suspend`-Funktionen können pausiert und fortgesetzt werden, ohne den Thread zu blockieren
- `viewModelScope` wird automatisch abgebrochen, wenn das ViewModel freigegeben wird; `lifecycleScope` folgt dem Lebenszyklus von Activity/Fragment
- `Dispatchers.IO` für Netzwerk/DB, `Dispatchers.Main` für UI, `Dispatchers.Default` für CPU-Arbeit
- Structured Concurrency: Child-Coroutinen übernehmen den Scope des Parents; das Abbrechen des Parents bricht alle Children ab
- `SupervisorJob`: das Fehlschlagen eines Children bricht die Geschwister NICHT ab
- `Flow` = kalter asynchroner Stream; `StateFlow` = Hot Stream mit aktuellem Wert (LiveData-Ersatz)

## Patterns {#patterns}

### Suspend-Funktionen und Builder {#suspend-functions-and-builders}
```kotlin
suspend fun fetchUser(id: Int): User {
    val response = api.getUser(id)  // suspends, doesn't block
    return response.body() ?: throw Exception("Not found")
}

// launch - fire and forget (returns Job)
viewModelScope.launch {
    val users = repository.getUsers()
    _users.value = users
}

// async - returns Deferred (await for result)
val deferred = viewModelScope.async { repository.getUsers() }
val users = deferred.await()
```

### Dispatchers {#dispatchers}
| Dispatcher | Verwendung | Pool |
|-----------|-----|------|
| `Dispatchers.Main` | UI-Aktualisierungen | Main-Thread |
| `Dispatchers.IO` | Netzwerk, DB, Datei-I/O | 64+ Threads |
| `Dispatchers.Default` | CPU-intensiv (Sortieren, Parsen) | Anzahl CPU-Kerne |

```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val data = repository.fetchFromNetwork()
    withContext(Dispatchers.Main) { textView.text = data }
}
```

### Scopes {#scopes}
```kotlin
// ViewModel scope - cancelled when VM cleared
viewModelScope.launch { ... }

// Lifecycle scope - tied to Activity/Fragment
lifecycleScope.launch { ... }
lifecycleScope.launchWhenStarted { ... }  // pauses when stopped

// Custom scope
val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
scope.launch { ... }
scope.cancel()  // must cancel manually
```

### Structured Concurrency (Parallelität) {#structured-concurrency-parallel}
```kotlin
viewModelScope.launch {
    val users = async { api.getUsers() }
    val orders = async { api.getOrders() }
    // Both run in parallel, await both
    _data.value = CombinedData(users.await(), orders.await())
}
```

### Fehlerbehandlung {#error-handling}
```kotlin
viewModelScope.launch {
    try {
        val result = repository.getData()
        _data.value = result
    } catch (e: HttpException) { _error.value = "Server: ${e.code()}" }
      catch (e: IOException) { _error.value = "Network error" }
}

// Global handler
val handler = CoroutineExceptionHandler { _, e -> _error.postValue(e.message) }
viewModelScope.launch(handler) { ... }
```

### Flow (Cold Reactive Stream) {#flow-cold-reactive-stream}
```kotlin
fun getUsers(): Flow<List<User>> = flow {
    while (true) {
        emit(api.getUsers())
        delay(30_000)  // refresh every 30s
    }
}

// Collecting
viewModelScope.launch {
    repository.getUsers()
        .catch { e -> _error.value = e.message }
        .collect { users -> _users.value = users }
}
```

### StateFlow (Hot Stream, LiveData-Ersatz) {#stateflow-hot-stream-livedata-replacement}
```kotlin
class MyViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try { _uiState.value = UiState.Success(repository.getData()) }
            catch (e: Exception) { _uiState.value = UiState.Error(e.message) }
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val data: List<User>) : UiState()
    data class Error(val message: String?) : UiState()
}
```

### Flow-Operatoren {#flow-operators}
```kotlin
flow
    .filter { it.isActive }
    .map { it.toUiModel() }
    .debounce(300)
    .distinctUntilChanged()
    .flatMapLatest { query -> searchApi(query) }
    .onStart { showLoading() }
    .onCompletion { hideLoading() }
    .catch { e -> showError(e) }
    .collect { result -> showResult(result) }
```

## Fallstricke {#gotchas}

- `runBlocking` blockiert den aktuellen Thread - NIEMALS im Android-Main-Thread verwenden (nur für Tests/main)
- `GlobalScope.launch` hat keine Lebenszyklus-Bindung - Coroutinen leaken, wenn sie nicht manuell abgebrochen werden
- `SupervisorJob` wirkt nur, wenn es der Parent der Child-Coroutinen ist - nicht, wenn es an `launch` übergeben wird
- `StateFlow` benötigt einen Initialwert; `SharedFlow` nicht
- `collect` ist eine terminale suspendierende Operation - Code nach `collect` wird erst ausgeführt, wenn der Flow abgeschlossen ist

## Siehe auch {#see-also}

- [[java-concurrency]] - Java-Threading zum Vergleich
- [[android-architecture-mvvm]] - Coroutinen im ViewModel
- [[android-networking-retrofit]] - Retrofit-Suspend-Funktionen
