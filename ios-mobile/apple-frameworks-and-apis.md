---
title: Apple Frameworks and APIs
category: ios-mobile/frameworks
tags: [frameworks, mapkit, swiftdata, coredata, import, apple-intelligence, sf-symbols]
---

# Apple Frameworks and APIs

## Key Facts

- Apple provides 300+ frameworks/technologies, each imported individually per file as needed
- `import SwiftUI` is auto-added to SwiftUI view files; other frameworks must be imported manually
- Importing a framework loads its code into the current file - not importing means types from that framework are unavailable
- **MapKit**: maps, annotations, user location - `import MapKit`
- **SwiftData**: modern data persistence framework (iOS 17+) - replacement for Core Data
- **Core Data**: legacy persistence framework - still supported but SwiftData is preferred for new projects
- **SF Symbols**: Apple's built-in icon library with 5000+ symbols - accessed via `Image(systemName: "icon.name")`
- **Apple Intelligence**: on-device AI features including predictive code completion in Xcode 16
- **Combine**: reactive framework for handling async events (being superseded by async/await)
- **Foundation**: basic types, collections, networking, dates - imported automatically with SwiftUI
- Each framework is loaded per-file, not project-wide, to keep build times fast

## Patterns

```swift
// Importing frameworks as needed
import SwiftUI    // UI components
import MapKit     // Maps and location
import SwiftData  // Data persistence

// SF Symbols usage
Image(systemName: "star.fill")           // Filled star
Image(systemName: "arrow.up.arrow.down") // Sort icon
Image(systemName: "slider.horizontal.3") // Filter icon

// MapKit basic usage
struct MapView: View {
    var body: some View {
        Map {
            Marker("Location", coordinate: CLLocationCoordinate2D(
                latitude: 37.7749,
                longitude: -122.4194
            ))
        }
    }
}

// SwiftData model
@Model
class TodoItem {
    var title: String
    var isComplete: Bool
    var createdAt: Date

    init(title: String) {
        self.title = title
        self.isComplete = false
        self.createdAt = .now
    }
}

// SwiftData container setup
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: TodoItem.self)
    }
}
```

## Gotchas

- Missing `import` causes "Cannot find type X in scope" errors - the type exists but the framework isn't loaded
- SwiftUI automatically imports Foundation, but MapKit, SwiftData, etc. need explicit imports
- SF Symbols names are case-sensitive and use dot notation - check the SF Symbols app for exact names
- SwiftData requires iOS 17+ deployment target - use Core Data if supporting older iOS versions
- Apple Intelligence features require specific hardware (Apple Silicon + 16GB RAM) - not available on all devices
- Framework availability varies by platform - some iOS frameworks are not available on macOS or watchOS
- Importing too many frameworks in one file doesn't cause runtime issues but can slow compilation

## See Also

- [Apple Developer Documentation](https://developer.apple.com/documentation/technologies)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
- [SwiftData](https://developer.apple.com/documentation/swiftdata)
- [[xcode-project-setup]]
- [[state-and-data-flow]]
