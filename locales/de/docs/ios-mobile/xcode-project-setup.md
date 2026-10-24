---
title: "Xcode-Projekt-Einrichtung und Tooling"
category: tooling
tags: [ios-mobile, xcode, project-setup, previews, simulator, version-control]
level: 3
source_sha256: ceac8de319e62c481810f92d705d740fb325366adc214fd24f67384436f5dd47
translation: machine
translated_at: '2026-10-24'
---
# Xcode-Projekt-Einrichtung und Tooling {#xcode-project-setup-and-tooling}

Xcode ist die erforderliche IDE für die iOS-Entwicklung. Dieser Artikel behandelt die Projekterstellung, die Navigation in der Oberfläche, Live-Previews, die Nutzung des Simulators, Versionskontrolle und Konventionen zur Dateiorganisation.

## Key Facts {#key-facts}

- Xcode von developer.apple.com herunterladen (kostenlose Apple-ID erforderlich)
- Xcode 15+ für die Entwicklung für iOS 17, Xcode 16+ für iOS 18
- Der Simulator wird separat heruntergeladen (~7 GB); vor dem Ausführen von Apps abwarten, bis der Download abgeschlossen ist
- Die SwiftUI-Canvas bietet eine Echtzeit-Vorschau ohne Ausführung im Simulator
- Konvention ist eine View pro Datei; Modelldateien importieren `Foundation`, Views importieren `SwiftUI`
- Swift Playgrounds (File > New > Playground) bieten eine REPL-ähnliche Sandbox
- Erster Start: Plattformen auswählen (iOS ist erforderlich, Watch abwählen spart Zeit)

## Patterns {#patterns}

### Neues Projekt erstellen {#creating-a-new-project}

1. File > New > Project > iOS > App
2. Product Name = App-Name
3. Interface: **SwiftUI** (nicht Storyboard/UIKit)
4. Language: **Swift**
5. Storage: None (Basis), SwiftData (iOS 17+) oder Core Data (Legacy-Persistenz)

Generierte Dateien:
- `AppName.swift` - Einstiegspunkt mit `@main`, `WindowGroup { ContentView() }`
- `ContentView.swift` - erste View mit dem Standardtext `"Hello, world!"`

### Xcode-Oberfläche {#xcode-interface}

| Bereich | Ort | Zweck |
|---------|-----|-------|
| Navigator | Linke Seitenleiste | Dateibaum, Umschalten über das Ordnersymbol |
| Editor | Mitte | Code-Bearbeitung |
| Canvas/Preview | Rechts neben dem Editor | Live-SwiftUI-Vorschau |
| Konsole | Unten | Debug-Ausgabe von `print()` |
| Run-Schaltfläche | Werkzeugleiste oben links | Erstellen und im Simulator starten |

Farbschemata: Xcode > Settings > Themes (Dusk, Classic Light/Dark, Midnight).

### @main-App-Einstiegspunkt {#main-app-entry-point}

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

### Preview-Makro {#preview-macro}

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

### Preview mit Datenabhängigkeiten {#preview-with-data-dependencies}

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

### Dateiorganisation {#file-organization}

```python
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

- Model-/Enum-Dateien: nur `import Foundation` (nicht SwiftUI)
- View-Dateien: `import SwiftUI`
- Neue SwiftUI-View: File > New File from Template > SwiftUI View
- Namenskonvention: CamelCase mit dem Suffix `View` (z. B. `CustomButtonView`)

### Frameworks importieren {#import-frameworks}

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

### Views sicher umbenennen {#renaming-views-safely}

Xcode-Refactoring verwenden: Doppelklick auf den View-Namen > Rechtsklick > Refactor > Rename. Aktualisiert alle Referenzen, einschließlich Datei, Preview und App-Einstiegspunkt.

### Versionskontrolle in Xcode {#version-control-in-xcode}

1. Source Control > New Git Repositories
2. `Option+Cmd+C` öffnet den Commit-Dialog
3. Alle stagen > Nachricht schreiben > Commit
4. Nach jedem funktionierenden Feature committen, um sichere Rollback-Punkte zu haben

### Tipps zur Live-Vorschau {#live-preview-tips}

- Der Canvas zeigt Aktualisierungen in Echtzeit, ohne den Simulator zu starten
- Auf die Play-Schaltfläche im Canvas klicken, um die Live-Interaktion zu aktivieren
- Wenn die Vorschau stoppt: Show Editor Only, danach zurück zu Canvas wechseln
- Letzte Option bei hängenden Previews: Xcode beenden und neu öffnen

## Gotchas {#gotchas}

- Der erste Xcode-Start erfordert die Auswahl der Plattformen – iOS ist erforderlich, Watch abwählen spart Download-Zeit
- `inMemory: true` in Previews bedeutet, dass Daten nicht persistiert werden – für echtes Persistenz-Testing den Simulator verwenden
- Die Canvas-Vorschau unterstützt nicht alle Funktionen (z. B. benötigt `AsyncImage` die Live-Vorschau oder den Simulator)
- Ein nicht benötigter Framework-Import kann in manchen Konfigurationen zu Build-Fehlern führen
- Die `.storekit`-Konfigurationsdatei muss für IAP-Tests in den Scheme-Einstellungen ausgewählt werden
- Storage-Option beim Setup: None wählen, wenn noch keine Persistenz benötigt wird – SwiftData/Core Data können später hinzugefügt werden

## Siehe auch {#see-also}

- [[swiftui-views-and-modifiers]] - Aufbau der Benutzeroberfläche
- [[swiftdata-persistence]] - SwiftData-Projekt-Setup
- [[core-data-persistence]] - Core-Data-Projekt-Setup
