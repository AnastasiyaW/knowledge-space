---
title: SwiftUI Forms and Input Controls
category: concepts
tags: [ios-mobile, swiftui, form, textfield, datepicker, slider, texteditor]
---

# SwiftUI Forms and Input Controls

Forms group input controls for data entry screens. This entry covers TextField, TextEditor, DatePicker, Slider, and common patterns for create/edit flows using sheets.

## Key Facts

- `Form` is a specialized list container that groups input controls with system styling
- `TextField` is single-line text input; `TextEditor` is multi-line (no built-in placeholder)
- All input controls require `$` binding to a `@State` property
- `DatePicker` offers `.date`, `.hourAndMinute`, or both display components
- `Slider(value:in:step:)` provides a range slider with optional step increments
- `.keyboardType(.decimalPad)` shows numeric keyboard for number inputs

## Patterns

### Complete Create Form

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

### TextField Styles and Configuration

```swift
TextField("Amount", text: $leftAmount)
    .textFieldStyle(.roundedBorder)           // visible border
    .multilineTextAlignment(.trailing)        // right-align text
    .keyboardType(.decimalPad)                // numeric keyboard
    .padding()
    .border(Color.gray)                       // custom border
```

### DatePicker Display Components

```swift
// Date only (no time)
DatePicker("Date", selection: $date, displayedComponents: .date)

// Time only
DatePicker("Time", selection: $date, displayedComponents: .hourAndMinute)

// Both date and time (default)
DatePicker("Date & Time", selection: $date)
```

### Edit View Pattern

For `@Model` classes (reference types), edits propagate back automatically:

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

### Input Controls Reference

| Control | Purpose | Binding Type |
|---------|---------|-------------|
| `TextField("label", text:)` | Single-line text | `Binding<String>` |
| `TextEditor(text:)` | Multi-line text | `Binding<String>` |
| `DatePicker("label", selection:)` | Date/time | `Binding<Date>` |
| `Slider(value:in:step:)` | Range selection | `Binding<Double>` |
| `Toggle("label", isOn:)` | Boolean switch | `Binding<Bool>` |
| `Picker("label", selection:)` | Choice selection | `Binding<T>` |

### TipKit (iOS 17+)

Show contextual onboarding tips:

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

Tips auto-dismiss after being seen.

## Gotchas

- `TextEditor` has no built-in placeholder text - set `@State var text = "Today was..."` as initial value workaround
- `Form` sections automatically group controls visually; use `Section` for explicit grouping
- `.keyboardType(.decimalPad)` has no "Done" button - use `@FocusState` + `.onTapGesture` to dismiss
- `Slider` value is `Double`; converting to `Int` for display requires `Int(rating)`
- The `$` binding is required for all input controls - forgetting it gives `Binding<T>` type mismatch errors
- Edit view pattern works with `@Model` classes because they are reference types - changes persist automatically

## See Also

- [[swiftui-state-and-data-flow]] - @State and @Binding drive form inputs
- [[swiftui-navigation]] - sheet presentation for create/edit flows
- [[swiftdata-persistence]] - modelContext.insert() to save form data
- [[core-data-persistence]] - viewContext.save() for Core Data forms
