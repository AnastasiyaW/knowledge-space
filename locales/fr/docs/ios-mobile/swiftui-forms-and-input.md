---
title: "Formulaires SwiftUI et contrôles de saisie"
category: concepts
tags: [ios-mobile, swiftui, form, textfield, datepicker, slider, texteditor]
level: 3
source_sha256: 2799f930cdca5a33c52525428b1ea3d1dda8f9fb470040c89c080bcb77b27d68
translation: machine
translated_at: '2026-10-24'
---
# Formulaires SwiftUI et contrôles de saisie {#swiftui-forms-and-input-controls}

Les formulaires regroupent les contrôles de saisie pour les écrans de saisie de données. Cette entrée couvre `TextField`, `TextEditor`, `DatePicker`, `Slider`, ainsi que les patrons courants pour les flux de création et de modification à l'aide de feuilles (sheets).

## Faits clés {#key-facts}

- `Form` est un conteneur de liste spécialisé qui regroupe les contrôles de saisie avec le style système
- `TextField` est une saisie de texte sur une seule ligne ; `TextEditor` est multiligne (sans placeholder intégré)
- Tous les contrôles de saisie nécessitent une liaison `$` vers une propriété `@State`
- `DatePicker` propose `.date`, `.hourAndMinute`, ou les deux composantes d'affichage
- `Slider(value:in:step:)` fournit un curseur de plage avec des incréments optionnels
- `.keyboardType(.decimalPad)` affiche un clavier numérique pour les saisies de nombres

## Patrons {#patterns}

### Formulaire de création complet {#complete-create-form}

```swift
struct CreateJournalEntryView: View {
    @Environment(\.modelContext) var modelContext
    @Environment(\.dismiss) var dismiss

    @State var title = ""
    @State var text = "Today was..."
    @State var rating = 3.0
    @State var date = Date()

    var body: some View {
        NavigationStack {
            Form {
                TextField("Title", text: $title)

                TextEditor(text: $text)

                DatePicker("Date", selection: $date, displayedComponents: .date)

                HStack {
                    Text(String(repeating: "star", count: Int(rating)))
                    Slider(value: $rating, in: 1...5, step: 1)
                }
            }
            .navigationTitle("New Journal Entry")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        let entry = JournalEntry(
                            title: title, text: text,
                            rating: rating, date: date
                        )
                        modelContext.insert(entry)
                        dismiss()
                    }
                    .bold()
                }
            }
        }
    }
}
```

### Styles et configuration de TextField {#textfield-styles-and-configuration}

```swift
TextField("Amount", text: $leftAmount)
    .textFieldStyle(.roundedBorder)           // visible border
    .multilineTextAlignment(.trailing)        // right-align text
    .keyboardType(.decimalPad)                // numeric keyboard
    .padding()
    .border(Color.gray)                       // custom border
```

### Composantes d'affichage de DatePicker {#datepicker-display-components}

```swift
// Date only (no time)
DatePicker("Date", selection: $date, displayedComponents: .date)

// Time only
DatePicker("Time", selection: $date, displayedComponents: .hourAndMinute)

// Both date and time (default)
DatePicker("Date & Time", selection: $date)
```

### Patron de vue d'édition {#edit-view-pattern}

Pour les classes `@Model` (types référence), les modifications se propagent automatiquement en retour :

```swift
struct EditJournalEntryView: View {
    @Environment(\.modelContext) var modelContext
    @Environment(\.dismiss) var dismiss

    @State var editingEntry: JournalEntry  // @Model = reference type, edits persist
    @State var editMode = false

    var body: some View {
        NavigationStack {
            if editMode {
                Form {
                    TextField("Title", text: $editingEntry.title)
                    TextEditor(text: $editingEntry.text)
                    DatePicker("Date", selection: $editingEntry.date,
                               displayedComponents: .date)
                    Slider(value: $editingEntry.rating, in: 1...5, step: 1)
                }
                .toolbar {
                    ToolbarItem(placement: .navigationBarLeading) {
                        Button("Delete") {
                            modelContext.delete(editingEntry)
                            dismiss()
                        }
                        .foregroundStyle(.red)
                    }
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button("Done") { editMode = false }
                            .bold()
                    }
                }
            } else {
                JournalEntryDetailView(entry: editingEntry)
                    .toolbar {
                        Button("Edit") { editMode = true }
                    }
            }
        }
    }
}
```

### Référence des contrôles de saisie {#input-controls-reference}

| Contrôle | Rôle | Type de liaison |
|---------|---------|-------------|
| `TextField("label", text:)` | Texte sur une seule ligne | `Binding<String>` |
| `TextEditor(text:)` | Texte multiligne | `Binding<String>` |
| `DatePicker("label", selection:)` | Date/heure | `Binding<Date>` |
| `Slider(value:in:step:)` | Sélection dans une plage | `Binding<Double>` |
| `Toggle("label", isOn:)` | Interrupteur booléen | `Binding<Bool>` |
| `Picker("label", selection:)` | Sélection parmi des choix | `Binding<T>` |

### TipKit (iOS 17+) {#tipkit-ios-17}

Afficher des conseils d'accueil contextuels :

```swift
import TipKit

struct ConversionTip: Tip {
    var title: Text { Text("Select a Currency") }
    var message: Text? { Text("Tap a currency to select what you want to convert.") }
    var image: Image? { Image(systemName: "hand.tap") }
}

// In view
TipView(ConversionTip())

// Configure at app entry point
init() {
    try? Tips.configure([
        .displayFrequency(.immediate),   // .daily or .weekly for production
        .datastoreLocation(.applicationDefault)
    ])
}
```

Les conseils se ferment automatiquement une fois affichés.

## Pièges courants {#gotchas}

- `TextEditor` n'a pas de texte d'espace réservé intégré - utilisez `@State var text = "Today was..."` comme valeur initiale en guise de contournement
- Les sections `Form` regroupent automatiquement les contrôles visuellement ; utilisez `Section` pour un regroupement explicite
- `.keyboardType(.decimalPad)` n'a pas de bouton « OK » - utilisez `@FocusState` + `.onTapGesture` pour fermer le clavier
- La valeur de `Slider` est un `Double` ; pour l'afficher sous forme d'`Int`, il faut la convertir avec `Int(rating)`
- La liaison `$` est obligatoire pour tous les contrôles de saisie - l'oublier provoque des erreurs de non-correspondance de type `Binding<T>`
- Le patron de vue d'édition fonctionne avec les classes `@Model` car ce sont des types référence - les modifications sont persistées automatiquement

## Voir aussi {#see-also}

- [[swiftui-state-and-data-flow]] - @State et @Binding alimentent les saisies des formulaires
- [[swiftui-navigation]] - présentation de feuilles pour les flux de création/modification
- [[swiftdata-persistence]] - modelContext.insert() pour enregistrer les données du formulaire
- [[core-data-persistence]] - viewContext.save() pour les formulaires Core Data
