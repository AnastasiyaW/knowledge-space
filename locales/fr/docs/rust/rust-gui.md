---
title: "Frameworks GUI en Rust"
category: tools
tags: [gui, desktop, egui, iced, tauri, frontend]
level: 3
source_sha256: b9f3f5b185ee5c8fb3188c5068bebe5e314b69490e6b5573cd688d21d73e5c7d
translation: machine
translated_at: '2026-10-24'
---
# Frameworks GUI en Rust {#rust-gui-frameworks}

Panorama du développement d'interfaces graphiques en Rust : frameworks natifs, bindings vers des toolkits établis et approches basées sur le web. L'écosystème est jeune mais évolue rapidement.

## Points clés {#key-facts}

- Aucun framework GUI dominant en Rust (contrairement à Qt pour C++ ou Swing pour Java)
- Deux paradigmes de rendu : mode retenu (la bibliothèque gère la scène) et mode immédiat (l'application redessine à chaque frame)
- Le mode immédiat est plus simple à implémenter, le mode retenu plus efficace pour les interfaces complexes
- Option la plus mature pour la production : Tauri (basé sur le web) ou les bindings GTK
- Options pur Rust les plus ergonomiques : egui (mode immédiat) ou iced (architecture Elm)
- areweguiyet.com suit l'état de l'écosystème

## Comparatif des frameworks {#framework-comparison}

| Framework | Mode | Multiplateforme | Maturité | Idéal pour |
|-----------|------|---------------|----------|----------|
| egui | Immédiat | Oui | Actif, stable | Outils, interfaces de débogage, prototypes |
| iced | Retenu (Elm) | Oui | Actif | Applications de bureau |
| Tauri | Web (HTML/CSS/JS) | Oui | Prêt pour la production | Équipes web |
| gtk-rs | Retenu | Priorité à Linux | Bindings matures | Écosystème GTK |
| Slint | Déclaratif | Oui + embarqué | Commercial | Embarqué, entreprise |
| Dioxus | Style React | Oui + web + mobile | Actif | Développeurs React |

## Mode immédiat (egui) {#immediate-mode-egui}

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

## Mode retenu (iced) {#retained-mode-iced}

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

## Basé sur le web (Tauri) {#web-based-tauri}

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

## Backends de rendu {#rendering-backends}

- **wgpu** : abstraction GPU multiplateforme (Vulkan/Metal/DX12/WebGPU)
- **OpenGL** : ancien mais largement supporté
- **Rendu logiciel** : calcul sur CPU, aucun GPU requis (adapté au distant et à l'embarqué)
- **Skia** : bibliothèque graphique 2D (via les bindings `skia-safe`)

## Guide de décision {#decision-guide}

| Scénario | Recommandation |
|----------|---------------|
| Outil rapide / interface de débogage | egui |
| Application de bureau, Rust natif | iced ou Slint |
| Équipe maîtrisant les technologies web | Tauri |
| Application de bureau Linux | gtk-rs |
| Périphérique embarqué | Slint |
| Développeur React | Dioxus |
| Overlay d'interface de jeu | egui |

## Pièges courants {#gotchas}

- **Problème :** egui redessine l'intégralité de l'interface à chaque frame -> forte utilisation du CPU à l'inactivité -> **Correctif :** utiliser `ctx.request_repaint_after()` pour limiter les repaints. egui 0.28+ détecte mieux l'inactivité.
- **Problème :** le modèle de propriété de Rust rend les arbres de widgets du mode retenu complexes (références parent-enfant) -> **Correctif :** utiliser des arènes indexées ou des patterns de type ECS. Ou choisir le mode immédiat pour contourner le problème.
- **Problème :** l'apparence native est difficile à obtenir avec les frameworks purs Rust -> **Correctif :** pour une apparence native, utiliser les bindings GTK/Qt ou Tauri avec la webview système. Les frameworks purs Rust dessinent leurs propres widgets.

## Voir aussi {#see-also}

- [[async-await]] - patterns async pour les boucles d'événements GUI
- [[closures]] - callbacks dans les frameworks GUI
- [[traits]] - abstractions de widgets basées sur les traits
