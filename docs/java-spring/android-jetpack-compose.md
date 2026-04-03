---
title: Android Jetpack Compose
category: concepts
tags: [java-spring, android, compose, declarative-ui, state, material3]
---

# Android Jetpack Compose

Android's modern declarative UI toolkit: composable functions, state management, layout composables, Modifier chains, lists with LazyColumn, navigation, and Material 3 theming.

## Key Facts

- Declarative: describe WHAT UI looks like, framework handles updates. No XML, no `findViewById`
- `@Composable` annotation marks UI functions; UI recomposes when state changes
- `remember { mutableStateOf(value) }` survives recompositions but NOT config changes
- `rememberSaveable { }` survives config changes (serializes to Bundle)
- State hoisting: move state UP to caller for reusability and testability
- Modifier order matters: `.padding().background()` applies padding OUTSIDE background
- `LazyColumn` = RecyclerView equivalent with efficient recycling

## Patterns

### Basic Composable
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

### Layout Composables
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

### State Management
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

### State Hoisting
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

### ViewModel Integration
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

### LazyColumn (Efficient List)
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

### Common Components
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

### Navigation
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

### Theming
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

## Gotchas

- `remember` survives recomposition but NOT config changes (rotation) - use `rememberSaveable` for important state
- Modifier order matters: `.padding(8.dp).background(Red)` vs `.background(Red).padding(8.dp)` look different
- Composables must be idempotent and free of side effects - use `LaunchedEffect` for side effects
- `LazyColumn` items should have stable `key` for efficient diffing
- Don't call ViewModel directly in composable body - side effects in `LaunchedEffect` or event handlers

## See Also

- [[android-architecture-mvvm]] - ViewModel and state management patterns
- [[kotlin-language-features]] - Kotlin features used extensively in Compose
- [[android-recyclerview]] - View-system equivalent (RecyclerView)
