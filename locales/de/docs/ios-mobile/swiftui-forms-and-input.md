---
title: "SwiftUI Formulare und Eingabesteuerelemente"
category: concepts
tags: [ios-mobile, swiftui, form, textfield, datepicker, slider, texteditor]
level: 3
source_sha256: 2799f930cdca5a33c52525428b1ea3d1dda8f9fb470040c89c080bcb77b27d68
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI Formulare und Eingabesteuerelemente {#swiftui-forms-and-input-controls}

Formulare gruppieren Eingabesteuerelemente für Dateneingabebildschirme. Dieser Eintrag behandelt `TextField`, `TextEditor`, `DatePicker`, `Slider` sowie gängige Muster für Create-/Edit-Abläufe mit Sheets.

## Wichtige Fakten {#key-facts}

- `Form` ist ein spezialisierter Listen-Container, der Eingabesteuerelemente mit System-Styling gruppiert
- `TextField` ist einzeilige Texteingabe; `TextEditor` ist mehrzeilig (ohne integrierten Platzhalter)
- Alle Eingabesteuerelemente benötigen eine `$`-Bindung an eine `@State`-Eigenschaft
- `DatePicker` bietet `.date`, `.hourAndMinute` oder beide Anzeigekomponenten
- `Slider(value:in:step:)` stellt einen Bereichsschieber mit optionalen Schrittweiten bereit
- `.keyboardType(.decimalPad)` zeigt eine numerische Tastatur für Zahleneingaben an

## Muster {#patterns}

### Vollständiges Create-Formular {#complete-create-form}

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

### TextField-Stile und Konfiguration {#textfield-styles-and-configuration}

```swift
TextField("Amount", text: $leftAmount)
    .textFieldStyle(.roundedBorder)           // visible border
    .multilineTextAlignment(.trailing)        // right-align text
    .keyboardType(.decimalPad)                // numeric keyboard
    .padding()
    .border(Color.gray)                       // custom border
```

### Anzeigekomponenten des DatePicker {#datepicker-display-components}

```swift
// Date only (no time)
DatePicker("Date", selection: $date, displayedComponents: .date)

// Time only
DatePicker("Time", selection: $date, displayedComponents: .hourAndMinute)

// Both date and time (default)
DatePicker("Date & Time", selection: $date)
```

### Muster für die Bearbeitungsansicht {#edit-view-pattern}

Bei `@Model`-Klassen (Referenztypen) werden Änderungen automatisch zurückgegeben:

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

### Referenz der Eingabesteuerelemente {#input-controls-reference}

| Steuerelement | Zweck | Binding-Typ |
|---------------|-------|-------------|
| `TextField("label", text:)` | Einzeiliger Text | `Binding<String>` |
| `TextEditor(text:)` | Mehrzeiliger Text | `Binding<String>` |
| `DatePicker("label", selection:)` | Datum/Uhrzeit | `Binding<Date>` |
| `Slider(value:in:step:)` | Bereichsauswahl | `Binding<Double>` |
| `Toggle("label", isOn:)` | Boolescher Schalter | `Binding<Bool>` |
| `Picker("label", selection:)` | Auswahl aus Optionen | `Binding<T>` |

### TipKit (iOS 17+) {#tipkit-ios-17}

Kontextbezogene Onboarding-Tipps anzeigen:

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

Tipps werden nach dem Anzeigen automatisch ausgeblendet.

## Fallstricke {#gotchas}

- `TextEditor` hat keinen integrierten Platzhaltertext – als Workaround `@State var text = "Today was..."` als Anfangswert setzen
- `Form`-Abschnitte gruppieren Steuerelemente automatisch optisch; für eine explizite Gruppierung `Section` verwenden
- `.keyboardType(.decimalPad)` hat keine „Fertig“-Taste – mit `@FocusState` + `.onTapGesture` die Tastatur ausblenden
- Der Wert von `Slider` ist `Double`; für die Anzeige als `Int` ist eine Konvertierung mit `Int(rating)` nötig
- Die `$`-Bindung ist für alle Eingabesteuerelemente erforderlich – ohne sie entstehen Typfehler wegen `Binding<T>`
- Das Muster für die Bearbeitungsansicht funktioniert mit `@Model`-Klassen, weil sie Referenztypen sind – Änderungen werden automatisch gespeichert

## Siehe auch {#see-also}

- [[swiftui-state-and-data-flow]] – @State und @Binding steuern Formulareingaben
- [[swiftui-navigation]] – Sheet-Präsentation für Create-/Edit-Abläufe
- [[swiftdata-persistence]] – modelContext.insert() zum Speichern von Formulardaten
- [[core-data-persistence]] – viewContext.save() für Core-Data-Formulare
