---
title: "Android Jetpack Compose"
category: concepts
tags: [java-spring, android, compose, declarative-ui, state, material3]
level: 3
source_sha256: c0d91ac0ecba89f337222835e9430eec82b421b933f69d4d345456f88ccc70e3
translation: machine
translated_at: '2026-10-24'
---
# Android Jetpack Compose {#android-jetpack-compose}

Le toolkit d'interface déclaratif moderne d'Android : fonctions composables, gestion d'état, composables de mise en page, chaînes de `Modifier`, listes avec LazyColumn, navigation et thème Material 3.

## Points clés {#key-facts}

- Déclaratif : on décrit à quoi ressemble l'interface (WHAT), le framework gère les mises à jour. Pas de XML, pas de `findViewById`
- L'annotation `@Composable` marque les fonctions d'interface ; l'interface se recompose lorsque l'état change
- `remember { mutableStateOf(value) }` survit aux recompositions mais PAS aux changements de configuration
- `rememberSaveable { }` survit aux changements de configuration (sérialisé dans un Bundle)
- Remontée d'état (state hoisting) : on remonte l'état VERS l'appelant pour la réutilisabilité et la testabilité
- L'ordre des `Modifier` compte : `.padding().background()` applique le padding À L'EXTÉRIEUR du background
- `LazyColumn` = équivalent de RecyclerView avec recyclage efficace

## Modèles {#patterns}

### Composable de base {#basic-composable}
```kotlin
@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MyAppTheme { Greeting("Android") } }
    }
}
```

### Composables de mise en page {#layout-composables}
```kotlin
// Column (vertical), Row (horizontal), Box (overlapping)
Column(
    modifier = Modifier.fillMaxSize().padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    Text("First")
    Text("Second")
}

Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
) { Text("Left"); Text("Right") }
```

### Gestion d'état {#state-management}
```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) { Text("Increment") }
    }
}
```

### Remontée d'état (State Hoisting) {#state-hoisting}
```kotlin
// Stateless composable (preferred)
@Composable
fun Counter(count: Int, onIncrement: () -> Unit) {
    Column {
        Text("Count: $count")
        Button(onClick = onIncrement) { Text("+") }
    }
}

// Stateful parent
@Composable
fun CounterScreen() {
    var count by remember { mutableStateOf(0) }
    Counter(count = count, onIncrement = { count++ })
}
```

### Intégration avec le ViewModel {#viewmodel-integration}
```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    when (uiState) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Success -> UserList(uiState.data)
        is UiState.Error -> ErrorMessage(uiState.message)
    }
}
```

### LazyColumn (liste efficace) {#lazycolumn-efficient-list}
```kotlin
LazyColumn(
    contentPadding = PaddingValues(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(users, key = { it.id }) { user -> UserCard(user) }
}

// Grid
LazyVerticalGrid(columns = GridCells.Fixed(2)) {
    items(products) { ProductCard(it) }
}
```

### Composants courants {#common-components}
```kotlin
// Input
var text by remember { mutableStateOf("") }
OutlinedTextField(value = text, onValueChange = { text = it },
    label = { Text("Email") })

// Card
Card(modifier = Modifier.fillMaxWidth().padding(8.dp),
     elevation = CardDefaults.cardElevation(4.dp)) {
    Column(Modifier.padding(16.dp)) {
        Text(user.name, style = MaterialTheme.typography.titleMedium)
    }
}

// Image with Coil
AsyncImage(model = user.avatarUrl, contentDescription = "Avatar",
    modifier = Modifier.size(48.dp).clip(CircleShape))
```

### Navigation {#navigation}
```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController, startDestination = "users") {
        composable("users") {
            UserListScreen(onUserClick = { id ->
                navController.navigate("user/$id")
            })
        }
        composable("user/{userId}",
            arguments = listOf(navArgument("userId") { type = NavType.IntType })) {
            UserDetailScreen(it.arguments?.getInt("userId") ?: 0)
        }
    }
}
```

### Thème {#theming}
```kotlin
@Composable
fun MyAppTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme(),
        typography = Typography,
        content = content
    )
}
```

## Pièges {#gotchas}

- `remember` survit à la recomposition mais PAS aux changements de configuration (rotation) : utilisez `rememberSaveable` pour l'état important
- L'ordre des `Modifier` compte : `.padding(8.dp).background(Red)` et `.background(Red).padding(8.dp)` ne produisent pas le même rendu
- Les composables doivent être idempotents et sans effets de bord : utilisez `LaunchedEffect` pour les effets de bord
- Les éléments de `LazyColumn` doivent avoir une `key` stable pour un diffing efficace
- N'appelez pas le ViewModel directement dans le corps d'un composable : placez les effets de bord dans `LaunchedEffect` ou dans les gestionnaires d'événements

## Voir aussi {#see-also}

- [[android-architecture-mvvm]] - Modèles ViewModel et gestion d'état
- [[kotlin-language-features]] - Fonctionnalités Kotlin utilisées largement dans Compose
- [[android-recyclerview]] - Équivalent du système de vues (RecyclerView)
