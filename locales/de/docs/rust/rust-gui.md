---
title: "Rust-GUI-Frameworks"
category: tools
tags: [gui, desktop, egui, iced, tauri, frontend]
level: 3
source_sha256: b9f3f5b185ee5c8fb3188c5068bebe5e314b69490e6b5573cd688d21d73e5c7d
translation: machine
translated_at: '2026-10-24'
---
# Rust-GUI-Frameworks {#rust-gui-frameworks}

Überblick über die GUI-Entwicklung in Rust: native Frameworks, Bindings zu etablierten Toolkits und webbasierte Ansätze. Das Ökosystem ist noch jung, reift aber schnell.

## Key Facts {#key-facts}

- Es gibt kein einzelnes dominierendes GUI-Framework in Rust (anders als Qt für C++ oder Swing für Java)
- Zwei Rendering-Paradigmen: Retained Mode (die Bibliothek verwaltet die Szene) und Immediate Mode (die Anwendung zeichnet jeden Frame neu)
- Immediate Mode ist einfacher zu implementieren, Retained Mode ist bei komplexen UIs effizienter
- Die ausgereifteste Option für den Produktiveinsatz: Tauri (webbasiert) oder GTK-Bindings
- Ergonomischste reine Rust-Lösungen: egui (Immediate Mode) oder iced (Elm-Architektur)
- areweguiyet.com verfolgt den Status des Ökosystems

## Framework-Vergleich {#framework-comparison}

| Framework | Modus | Plattformübergreifend | Reife | Am besten geeignet für |
|-----------|-------|----------------------|-------|------------------------|
| egui | Immediate | Ja | Aktiv, stabil | Tools, Debug-UIs, Prototypen |
| iced | Retained (Elm) | Ja | Aktiv | Desktop-Apps |
| Tauri | Web (HTML/CSS/JS) | Ja | Produktionsreif | Teams mit Web-Technologien |
| gtk-rs | Retained | Linux-first | Ausgereifte Bindings | GTK-Ökosystem |
| Slint | Deklarativ | Ja + Embedded | Kommerziell | Embedded, Enterprise |
| Dioxus | React-ähnlich | Ja + Web + Mobil | Aktiv | React-Entwickler |

## Immediate Mode (egui) {#immediate-mode-egui}

```rust
// egui - redraws every frame, no persistent widget tree
use eframe::egui;

struct MyApp {
    name: String,
    counter: i32,
}

impl eframe::App for MyApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("My App");
            ui.text_edit_singleline(&mut self.name);
            if ui.button("Click me").clicked() {
                self.counter += 1;
            }
            ui.label(format!("Count: {}", self.counter));
        });
    }
}

fn main() -> eframe::Result<()> {
    eframe::run_native(
        "My App",
        eframe::NativeOptions::default(),
        Box::new(|_cc| Ok(Box::new(MyApp {
            name: String::new(),
            counter: 0,
        }))),
    )
}
```

## Retained Mode (iced) {#retained-mode-iced}

```rust
// iced - Elm architecture: Model, Message, View, Update
use iced::widget::{button, column, text};
use iced::Element;

#[derive(Default)]
struct Counter {
    value: i32,
}

#[derive(Debug, Clone)]
enum Message {
    Increment,
    Decrement,
}

impl Counter {
    fn update(&mut self, message: Message) {
        match message {
            Message::Increment => self.value += 1,
            Message::Decrement => self.value -= 1,
        }
    }

    fn view(&self) -> Element<Message> {
        column![
            button("+").on_press(Message::Increment),
            text(self.value),
            button("-").on_press(Message::Decrement)].into()
    }
}
```

## Webbasiert (Tauri) {#web-based-tauri}

```rust
// Backend in Rust, frontend in HTML/CSS/JS
// tauri::command exposes Rust functions to JS
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running");
}
```

```javascript
// Frontend calls Rust via invoke
const result = await invoke("greet", { name: "World" });
```

## Rendering-Backends {#rendering-backends}

- **wgpu**: plattformübergreifende GPU-Abstraktion (Vulkan/Metal/DX12/WebGPU)
- **OpenGL**: veraltet, aber weit verbreitet
- **Software-Rendering**: CPU-basiert, keine GPU nötig (geeignet für Remote- oder Embedded-Einsatz)
- **Skia**: 2D-Grafikbibliothek (über die `skia-safe`-Bindings)

## Entscheidungshilfe {#decision-guide}

| Szenario | Empfehlung |
|----------|-----------|
| Schnelles Tool / Debug-UI | egui |
| Desktop-App, Rust-nativ | iced oder Slint |
| Team kennt Web-Technologien | Tauri |
| Linux-Desktop-App | gtk-rs |
| Embedded-Gerät | Slint |
| React-Entwickler | Dioxus |
| Game-UI-Overlay | egui |

## Gotchas {#gotchas}

- **Problem:** egui zeichnet die gesamte UI in jedem Frame neu -> hohe CPU-Auslastung im Leerlauf -> **Lösung:** `ctx.request_repaint_after()` verwenden, um Neuzeichnungen zu drosseln. egui 0.28+ erkennt Leerlauf besser.
- **Problem:** Das Ownership-Modell von Rust macht Widget-Bäume im Retained Mode komplex (Eltern-Kind-Referenzen) -> **Lösung:** Indizierte Arenas oder ECS-ähnliche Muster verwenden. Alternativ den Immediate Mode wählen, um das Problem zu umgehen.
- **Problem:** Ein natives Look-and-Feel ist mit reinen Rust-Frameworks schwer umzusetzen -> **Lösung:** Für ein natives Erscheinungsbild GTK-/Qt-Bindings oder Tauri mit der System-Webview verwenden. Reine Rust-Frameworks zeichnen ihre eigenen Widgets.

## Siehe auch {#see-also}

- [[async-await]] - Async-Muster für GUI-Event-Loops
- [[closures]] - Callbacks in GUI-Frameworks
- [[traits]] - trait-basierte Widget-Abstraktionen
