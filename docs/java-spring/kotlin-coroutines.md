---
title: Kotlin Coroutines, Flow, and Async Patterns
category: concepts
tags: [java-spring, kotlin, coroutines, flow, async, dispatchers, state-flow]
---

# Kotlin Coroutines, Flow, and Async Patterns

Kotlin coroutines for async programming: suspend functions, dispatchers, scopes, structured concurrency, error handling, Flow for reactive streams, StateFlow, and Android integration.

## Key Facts

- Coroutines are lightweight (few hundred bytes vs ~1MB per thread) - millions possible
- `suspend` functions can be paused/resumed without blocking the thread
- `viewModelScope` auto-cancels when ViewModel is cleared; `lifecycleScope` follows Activity/Fragment lifecycle
- `Dispatchers.IO` for network/DB, `Dispatchers.Main` for UI, `Dispatchers.Default` for CPU work
- Structured concurrency: child coroutines inherit parent scope; parent cancellation cancels all children
- `SupervisorJob`: one child failure does NOT cancel siblings
- `Flow` = cold async stream; `StateFlow` = hot stream with current value (LiveData replacement)

## Patterns

### Suspend Functions and Builders
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

### Dispatchers
| Dispatcher | Use | Pool |
|-----------|-----|------|
| `Dispatchers.Main` | UI updates | Main thread |
| `Dispatchers.IO` | Network, DB, file I/O | 64+ threads |
| `Dispatchers.Default` | CPU-intensive (sorting, parsing) | CPU core count |

```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val data = repository.fetchFromNetwork()
    withContext(Dispatchers.Main) { textView.text = data }
}
```

### Scopes
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

### Structured Concurrency (Parallel)
```kotlin
viewModelScope.launch {
    val users = async { api.getUsers() }
    val orders = async { api.getOrders() }
    // Both run in parallel, await both
    _data.value = CombinedData(users.await(), orders.await())
}
```

### Error Handling
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

### Flow (Cold Reactive Stream)
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

### StateFlow (Hot Stream, LiveData Replacement)
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

### Flow Operators
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

## Gotchas

- `runBlocking` blocks the current thread - NEVER use on Android main thread (only for tests/main)
- `GlobalScope.launch` has no lifecycle awareness - coroutines leak if not cancelled manually
- `SupervisorJob` only works if it's the parent of child coroutines - not if passed to `launch`
- `StateFlow` requires initial value; `SharedFlow` does not
- `collect` is a terminal suspending operation - code after `collect` won't run until flow completes

## See Also

- [[java-concurrency]] - Java threading for comparison
- [[android-architecture-mvvm]] - Coroutines in ViewModel
- [[android-networking-retrofit]] - Retrofit suspend functions
