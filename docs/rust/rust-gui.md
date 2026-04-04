---
title: Rust GUI Frameworks
category: tools
tags: [gui, desktop, egui, iced, tauri, frontend]
---

# Rust GUI Frameworks

Landscape of GUI development in Rust: native frameworks, bindings to established toolkits, and web-based approaches. Ecosystem is young but maturing rapidly.

## Key Facts

- No single dominant GUI framework in Rust (unlike Qt for C++ or Swing for Java)
- Two rendering paradigms: retained mode (library manages scene) and immediate mode (app redraws every frame)
- Immediate mode simpler to implement, retained mode more efficient for complex UIs
- Most mature option for production: Tauri (web-based) or GTK bindings
- Most ergonomic pure-Rust: egui (immediate mode) or iced (Elm architecture)
- areweguiyet.com tracks ecosystem status

## Framework Comparison

| Framework | Mode | Cross-platform | Maturity | Best for |
|-----------|------|---------------|----------|----------|
| egui | Immediate | Yes | Active, stable | Tools, debug UIs, prototypes |
| iced | Retained (Elm) | Yes | Active | Desktop apps |
| Tauri | Web (HTML/CSS/JS) | Yes | Production-ready | Web-tech teams |
| gtk-rs | Retained | Linux-first | Mature bindings | GTK ecosystem |
| Slint | Declarative | Yes + embedded | Commercial | Embedded, enterprise |
| Dioxus | React-like | Yes + web + mobile | Active | React developers |

## Immediate Mode (egui)

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

## Retained Mode (iced)

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
            button("-").on_press(Message::Decrement),
        ].into()
    }
}
```

## Web-Based (Tauri)

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

## Rendering Backends

- **wgpu**: cross-platform GPU abstraction (Vulkan/Metal/DX12/WebGPU)
- **OpenGL**: legacy but widely supported
- **Software rendering**: CPU-based, no GPU needed (good for remote/embedded)
- **Skia**: 2D graphics library (via `skia-safe` bindings)

## Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Quick tool / debug UI | egui |
| Desktop app, Rust-native | iced or Slint |
| Team knows web tech | Tauri |
| Linux desktop app | gtk-rs |
| Embedded device | Slint |
| React developer | Dioxus |
| Game UI overlay | egui |

## Gotchas

- **Issue:** egui redraws entire UI every frame -> high CPU usage when idle -> **Fix:** Use `ctx.request_repaint_after()` to throttle repaints. egui 0.28+ has better idle detection.
- **Issue:** Rust's ownership model makes retained mode widget trees complex (parent-child references) -> **Fix:** Use indexed arenas or ECS-like patterns. Or choose immediate mode to sidestep the problem.
- **Issue:** Native look-and-feel is hard with pure-Rust frameworks -> **Fix:** For native appearance, use GTK/Qt bindings or Tauri with system webview. Pure-Rust frameworks draw their own widgets.

## See Also

- [[async-await]] - async patterns for GUI event loops
- [[closures]] - callbacks in GUI frameworks
- [[traits]] - trait-based widget abstractions
