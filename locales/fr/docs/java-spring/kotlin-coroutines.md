---
title: "Coroutines Kotlin, Flow et patterns asynchrones"
category: concepts
tags: [java-spring, kotlin, coroutines, flow, async, dispatchers, state-flow]
level: 3
source_sha256: 252f61574762648da0b7e4e3af9a99fe3a5a999032991ad610afdfe26978b0c9
translation: machine
translated_at: '2026-10-24'
---
# Coroutines Kotlin, Flow et patterns asynchrones {#kotlin-coroutines-flow-and-async-patterns}

Coroutines Kotlin pour la programmation asynchrone : fonctions suspend, dispatchers, scopes, concurrence structurée, gestion des erreurs, Flow pour les flux réactifs, StateFlow et intégration Android.

## Points clés {#key-facts}

- Les coroutines sont légères (quelques centaines d'octets contre ~1 Mo par thread) - des millions sont possibles
- Les fonctions `suspend` peuvent être suspendues et reprises sans bloquer le thread
- `viewModelScope` s'annule automatiquement lorsque le ViewModel est détruit ; `lifecycleScope` suit le cycle de vie de l'Activity ou du Fragment
- `Dispatchers.IO` pour le réseau et la BD, `Dispatchers.Main` pour l'UI, `Dispatchers.Default` pour le travail CPU
- Concurrence structurée : les coroutines enfants héritent du scope parent ; l'annulation du parent annule tous les enfants
- `SupervisorJob` : l'échec d'un enfant n'annule PAS ses frères
- `Flow` = flux asynchrone froid ; `StateFlow` = flux chaud avec valeur courante (remplacement de LiveData)

## Patterns {#patterns}

### Fonctions suspend et builders {#suspend-functions-and-builders}
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
| Dispatcher | Usage | Pool |
|-----------|-----|------|
| `Dispatchers.Main` | Mises à jour de l'UI | Thread principal |
| `Dispatchers.IO` | Réseau, BD, E/S fichiers | 64+ threads |
| `Dispatchers.Default` | CPU intensif (tri, parsing) | Nombre de cœurs CPU |

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

### Concurrence structurée (parallèle) {#structured-concurrency-parallel}
```kotlin
viewModelScope.launch {
    val users = async { api.getUsers() }
    val orders = async { api.getOrders() }
    // Both run in parallel, await both
    _data.value = CombinedData(users.await(), orders.await())
}
```

### Gestion des erreurs {#error-handling}
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

### Flow (flux réactif froid) {#flow-cold-reactive-stream}
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

### StateFlow (flux chaud, remplacement de LiveData) {#stateflow-hot-stream-livedata-replacement}
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

### Opérateurs de Flow {#flow-operators}
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

## Pièges {#gotchas}

- `runBlocking` bloque le thread courant - NE JAMAIS l'utiliser sur le thread principal Android (uniquement pour les tests et le main)
- `GlobalScope.launch` n'a aucune conscience du cycle de vie - les coroutines fuient si elles ne sont pas annulées manuellement
- `SupervisorJob` ne fonctionne que s'il est le parent des coroutines enfants - pas s'il est passé à `launch`
- `StateFlow` exige une valeur initiale ; `SharedFlow` non
- `collect` est une opération suspendante terminale - le code situé après `collect` ne s'exécute pas tant que le flux n'est pas terminé

## Voir aussi {#see-also}

- [[java-concurrency]] - Threading Java pour comparaison
- [[android-architecture-mvvm]] - Coroutines dans le ViewModel
- [[android-networking-retrofit]] - Fonctions suspend de Retrofit
