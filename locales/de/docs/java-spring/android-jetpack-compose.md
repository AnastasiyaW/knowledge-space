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

Android-Toolkit für deklarative Benutzeroberflächen: Composable-Funktionen, Zustandsverwaltung, Layout-Composables, Modifier-Ketten, Listen mit LazyColumn, Navigation und Material-3-Theming.

## Key Facts {#key-facts}

- Deklarativ: Man beschreibt, WAS die UI darstellt, das Framework übernimmt die Aktualisierungen. Kein XML, kein `findViewById`
- Die `@Composable`-Annotation markiert UI-Funktionen; die UI wird bei Zustandsänderungen neu komponiert
- `remember { mutableStateOf(value) }` übersteht Recompositions, aber NICHT Konfigurationsänderungen
- `rememberSaveable { }` übersteht Konfigurationsänderungen (serialisiert in ein Bundle)
- State Hoisting: Zustand NACH OBEN zum Aufrufer verschieben, für Wiederverwendbarkeit und Testbarkeit
- Die Reihenfolge der Modifier ist wichtig: `.padding().background()` wendet das Padding AUSSERHALB des Hintergrunds an
- `LazyColumn` = Entsprechung zu RecyclerView mit effizientem Recycling

## Patterns {#patterns}

### Basic Composable {#basic-composable}
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

### Layout Composables {#layout-composables}
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

### State Management {#state-management}
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

### State Hoisting {#state-hoisting}
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

### ViewModel Integration {#viewmodel-integration}
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

### LazyColumn (Efficient List) {#lazycolumn-efficient-list}
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

### Common Components {#common-components}
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

### Theming {#theming}
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

## Gotchas {#gotchas}

- `remember` übersteht Recomposition, aber NICHT Konfigurationsänderungen (Rotation) - für wichtigen Zustand `rememberSaveable` verwenden
- Die Reihenfolge der Modifier ist wichtig: `.padding(8.dp).background(Red)` und `.background(Red).padding(8.dp)` sehen unterschiedlich aus
- Composables müssen idempotent sein und dürfen keine Seiteneffekte haben - für Seiteneffekte `LaunchedEffect` verwenden
- Elemente von `LazyColumn` sollten einen stabilen `key` haben, damit das Diffing effizient ist
- Den ViewModel nicht direkt im Composable-Body aufrufen - Seiteneffekte in `LaunchedEffect` oder Event-Handlern ausführen

## See Also {#see-also}

- [[android-architecture-mvvm]] - ViewModel- und Zustandsverwaltungsmuster
- [[kotlin-language-features]] - Kotlin-Features, die in Compose intensiv genutzt werden
- [[android-recyclerview]] - View-System-Entsprechung (RecyclerView)
