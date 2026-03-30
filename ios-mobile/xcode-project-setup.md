---
title: Xcode Project Setup and Configuration
category: ios-mobile/tooling
tags: [xcode, project-setup, simulator, app-icon, assets, xcode-16]
---

# Xcode Project Setup and Configuration

## Key Facts

- Xcode 16 is required for iOS 18, SwiftUI 6, and Swift 6 development
- Minimum macOS version for Xcode 16: macOS Sonoma 14.5
- New project setup: File > New > iOS > App > SwiftUI interface > Swift language
- **Product Name** is not necessarily the App Store display name - it's the internal project name
- **Organization Identifier**: reverse domain notation (`com.yourcompany`) - must be unique per developer
- **Bundle Identifier**: auto-generated from org identifier + product name
- Swift 6 must be manually enabled: Build Settings > Swift Language Version > Swift 6 (defaults to Swift 5)
- Apple ID sign-in is required for App Store publishing and physical device testing, but not for development
- Predictive code completion requires macOS 15+, Apple silicon, and 16GB+ RAM
- Asset catalog (`.xcassets`) stores images, app icons, and color sets
- Simulator selection is in the top toolbar - choose from available device types
- `import SwiftUI` is auto-added to new SwiftUI files; other frameworks must be imported manually

## Patterns

```
Xcode Navigator (left panel):
  Project Navigator - files and folders
  Source Control Navigator - git history
  Bookmark Navigator - saved code locations
  Build Navigator - build results

Xcode Inspector (right panel):
  File Inspector - file metadata and path
  Quick Help Inspector - documentation for selected code
  Attributes Inspector - visual properties, updates code automatically
```

```
Project structure for a typical SwiftUI app:
  MyApp/
    MyAppApp.swift          // @main entry point
    ContentView.swift       // Main view
    Assets.xcassets/        // Images, icons, colors
      AppIcon.appiconset/   // App icon
    Models/                 // Data models
    Views/                  // UI views
```

```swift
// Entry point - @main marks the app's starting point
@main
struct LOTRConverterApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

## Gotchas

- New projects default to Swift 5, NOT Swift 6 - must change manually in Build Settings
- App icon: iOS 18 supports single-size icon only (1024x1024) - Apple auto-generates other sizes
- Source Control/Git checkbox during project creation: uncheck if you don't need it immediately
- Preview sometimes pauses or crashes - click the refresh/play button in the preview canvas
- Xcode minimap (Editor > Minimap): helpful for large files but takes screen space
- `Re-indent on paste` in Settings > Indentation - recommended to enable for cleaner code
- Storage option during setup: None, SwiftData, Core Data - choose None if you don't need persistence yet
- Xcode auto-complete: always use it (Tab key) to avoid capitalization and spelling mistakes
- Without a Mac: services like macincloud.com or macstadium.com provide remote Mac access

## See Also

- [Xcode Overview](https://developer.apple.com/xcode/)
- [Creating an Xcode Project](https://developer.apple.com/documentation/xcode/creating-an-xcode-project-for-an-app)
- [[swiftui-views]]
- [[app-store-submission]]
