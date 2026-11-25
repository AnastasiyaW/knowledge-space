---
title: "Configuration du projet Xcode et outillage"
category: tooling
tags: [ios-mobile, xcode, project-setup, previews, simulator, version-control]
level: 3
source_sha256: ceac8de319e62c481810f92d705d740fb325366adc214fd24f67384436f5dd47
translation: machine
translated_at: '2026-10-24'
---
# Configuration du projet Xcode et outillage {#xcode-project-setup-and-tooling}

Xcode est l'IDE requis pour le développement iOS. Ce document couvre la création de projet, la navigation dans l'interface, les aperçus en direct, l'utilisation du simulateur, la gestion de versions et les conventions d'organisation des fichiers.

## Points clés {#key-facts}

- Télécharger Xcode depuis developer.apple.com (identifiant Apple gratuit requis)
- Xcode 15+ pour le développement iOS 17, Xcode 16+ pour iOS 18
- Les simulateurs se téléchargent séparément (environ 7 Go) ; attendre la fin du téléchargement avant d'exécuter des apps
- Le Canvas SwiftUI fournit un aperçu en temps réel sans lancer le simulateur
- Une vue par fichier est la convention ; les fichiers de modèle importent `Foundation`, les vues importent `SwiftUI`
- Swift Playgrounds (File > New > Playground) fournit un bac à sable de type REPL
- Premier lancement : sélectionner les plateformes (iOS est obligatoire, décocher Watch pour gagner du temps)

## Modèles {#patterns}

### Créer un nouveau projet {#creating-a-new-project}

1. File > New > Project > iOS > App
2. Product name = nom de l'app
3. Interface : **SwiftUI** (et non Storyboard/UIKit)
4. Langage : **Swift**
5. Stockage : None (basique), SwiftData (iOS 17+), ou Core Data (persistance héritée)

Fichiers générés :
- `AppName.swift` - point d'entrée avec `@main`, `WindowGroup { ContentView() }`
- `ContentView.swift` - première vue avec le texte par défaut `"Hello, world!"`

### Interface de Xcode {#xcode-interface}

| Zone | Emplacement | Rôle |
|------|-------------|------|
| Navigator | Barre latérale gauche | Arborescence des fichiers, à afficher/masquer avec l'icône de dossier |
| Editor | Centre | Édition du code |
| Canvas/Preview | À droite de l'éditeur | Aperçu SwiftUI en direct |
| Console | Bas | Sortie de débogage de `print()` |
| Run button | Barre d'outils en haut à gauche | Compiler et lancer dans le simulateur |

Thèmes : Xcode > Settings > Themes (Dusk, Classic Light/Dark, Midnight).

### Point d'entrée de l'app avec @main {#main-app-entry-point}

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

### Macro Preview {#preview-macro}

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

### Preview avec dépendances de données {#preview-with-data-dependencies}

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

### Organisation des fichiers {#file-organization}

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

- Fichiers de modèle/enum : `import Foundation` uniquement (pas SwiftUI)
- Fichiers de vue : `import SwiftUI`
- Nouvelle vue SwiftUI : File > New File from Template > SwiftUI View
- Convention de nommage : CamelCase se terminant par `View` (par ex. `CustomButtonView`)

### Import des frameworks {#import-frameworks}

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

### Renommer les vues en toute sécurité {#renaming-views-safely}

Utiliser le refactoring de Xcode : double-cliquer sur le nom de la vue > clic droit > Refactor > Rename. Cela met à jour toutes les références, y compris le fichier, la preview et le point d'entrée de l'app.

### Gestion de versions dans Xcode {#version-control-in-xcode}

1. Source Control > New Git Repositories
2. `Option+Cmd+C` ouvre la boîte de dialogue de commit
3. Stage all > rédiger le message > Commit
4. Committer après chaque fonctionnalité fonctionnelle pour disposer de points de retour sûrs

### Conseils pour l'aperçu en direct {#live-preview-tips}

- Le Canvas affiche les mises à jour en temps réel sans lancer le simulateur
- Cliquer sur le bouton lecture dans le Canvas pour activer l'interaction en direct
- Si l'aperçu s'arrête : Show Editor Only, puis revenir sur Canvas
- Solution radicale pour un aperçu bloqué : quitter et relancer Xcode

## Pièges {#gotchas}

- Le premier lancement de Xcode exige la sélection des plateformes : iOS est obligatoire, décocher Watch pour gagner du temps de téléchargement
- `inMemory: true` dans les previews signifie que les données ne sont pas persistées : utiliser le simulateur pour tester la persistance réelle
- Le Canvas ne prend pas en charge toutes les fonctionnalités (par ex. `AsyncImage` nécessite l'aperçu en direct ou le simulateur)
- Ajouter un import de framework inutile peut provoquer des erreurs de compilation dans certaines configurations
- Le fichier de configuration `.storekit` doit être sélectionné dans les réglages du scheme pour tester les achats intégrés (IAP)
- Option de stockage lors de la configuration : choisir None si la persistance n'est pas encore nécessaire ; SwiftData/Core Data peut être ajouté plus tard

## Voir aussi {#see-also}

- [[swiftui-views-and-modifiers]] - construction de l'interface
- [[swiftdata-persistence]] - configuration d'un projet SwiftData
- [[core-data-persistence]] - configuration d'un projet Core Data
