---
title: Xcode Project Setup and Tooling
category: tooling
tags: [ios-mobile, xcode, project-setup, previews, simulator, version-control]
---

# Xcode Project Setup and Tooling

Xcode is the required IDE for iOS development. This covers project creation, interface navigation, live previews, simulator usage, version control, and file organization conventions.

## Key Facts

- Download Xcode from developer.apple.com (free Apple ID required)
- Xcode 15+ for iOS 17, Xcode 16+ for iOS 18 development
- Simulator downloads separately (~7 GB); wait for it before running apps
- SwiftUI Canvas provides real-time preview without running the simulator
- One view per file is the convention; model files import `Foundation`, views import `SwiftUI`
- Swift Playgrounds (File > New > Playground) provide a REPL-like sandbox
- First launch: select platforms (iOS is required, uncheck Watch to save time)

## Patterns

### Creating a New Project

1. File > New > Project > iOS > App
2. Product name = app name
3. Interface: **SwiftUI** (not Storyboard/UIKit)
4. Language: **Swift**
5. Storage: None (basic), SwiftData (iOS 17+), or Core Data (legacy persistence)

Generated files:
- `AppName.swift` - entry point with `@main`, `WindowGroup { ContentView() }`
- `ContentView.swift` - first view with default `"Hello, world!"` text

### Xcode Interface

| Area | Location | Purpose |
|------|----------|---------|
| Navigator | Left sidebar | File tree, toggle with folder icon |
| Editor | Center | Code editing |
| Canvas/Preview | Right of editor | Live SwiftUI preview |
| Console | Bottom | Debug output from `print()` |
| Run button | Top-left toolbar | Build and launch in simulator |

Themes: Xcode > Settings > Themes (Dusk, Classic Light/Dark, Midnight).

### @main App Entry Point

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Preview Macro

```swift
// Modern syntax (Xcode 15+)
#Preview {
    ContentView()
}

// Legacy syntax (still valid)
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

// Dark mode preview
#Preview {
    ContentView()
        .preferredColorScheme(.dark)
}
```

### Preview with Data Dependencies

```swift
// SwiftData preview
#Preview {
    JournalEntriesListView()
        .modelContainer(for: JournalEntry.self, inMemory: true)
}

// Core Data preview
#Preview {
    PokemonDetail(pokemon: PersistenceController.preview.fetchPokemon(id: 1))
}
```

### File Organization

```
MyApp/
  MyApp.swift              // @main entry point
  ContentView.swift        // root view
  Views/
    DetailView.swift       // additional views
    RowView.swift
  Models/
    DataModel.swift        // import Foundation only
    Enums.swift
  Assets.xcassets/         // images, colors, app icon
```

- Model/enum files: `import Foundation` only (not SwiftUI)
- View files: `import SwiftUI`
- New SwiftUI view: File > New File from Template > SwiftUI View
- Naming convention: CamelCase ending in `View` (e.g., `CustomButtonView`)

### Import Frameworks

```swift
import SwiftUI        // UI framework
import Foundation     // strings, dates, URLs
import MapKit         // maps
import SwiftData      // persistence (iOS 17+)
import Charts         // data visualization
import AVKit          // audio/video
import StoreKit       // in-app purchases
import TipKit         // onboarding tips (iOS 17+)
```

### Renaming Views Safely

Use Xcode refactor: double-click view name > Right-click > Refactor > Rename. Updates all references including file, preview, and app entry point.

### Version Control in Xcode

1. Source Control > New Git Repositories
2. `Option+Cmd+C` opens commit dialog
3. Stage all > write message > Commit
4. Commit after each working feature for safe rollback points

### Live Preview Tips

- Canvas shows real-time updates without running simulator
- Click play button in canvas to enable live interaction
- If preview stops: Show Editor Only, then switch back to Canvas
- Nuclear option for stuck previews: quit and reopen Xcode

## Gotchas

- First Xcode launch requires platform selection - iOS is required, uncheck Watch to save download time
- `inMemory: true` in previews means data is not persisted - use the simulator to test actual persistence
- Canvas preview does not support all features (e.g., `AsyncImage` requires live preview or simulator)
- Adding a framework import that is not needed can cause build errors in some configurations
- The `.storekit` configuration file must be selected in scheme settings for IAP testing
- Storage option during setup: choose None if you don't need persistence yet - SwiftData/Core Data can be added later

## See Also

- [[swiftui-views-and-modifiers]] - building the UI
- [[swiftdata-persistence]] - SwiftData project setup
- [[core-data-persistence]] - Core Data project setup
