---
title: "AVKit-Audio und haptisches Feedback"
category: concepts
tags: [ios-mobile, swiftui, avkit, audio, haptics, sound-effects, music]
level: 3
source_sha256: 146c709664919f1d28579196cd945b4a7ab25af7d6ac2bf758976e2fd2902f52
translation: machine
translated_at: '2026-10-24'
---
# AVKit-Audio und haptisches Feedback {#avkit-audio-and-haptic-feedback}

AVKit stellt Audiowiedergabe für Hintergrundmusik und Soundeffekte bereit. Die Feedback-Generatoren von UIKit liefern haptisches Feedback auf physischen Geräten. Dieser Eintrag behandelt das Zwei-Player-Audiomuster und die Integration von Haptik in SwiftUI.

## Wichtige Fakten {#key-facts}

- `AVAudioPlayer` spielt Audiodateien aus dem App-Bundle ab
- Zwei separate Player verwenden (Musik + SFX) – ein einzelner Player führt dazu, dass SFX die Musik dauerhaft unterbrechen
- `numberOfLoops = -1` lässt Audio unbegrenzt wiederholen
- Haptisches Feedback verwendet `UINotificationFeedbackGenerator` aus UIKit
- Haptik funktioniert nur auf physischen Geräten, nicht im Simulator
- Audiodateien müssen dem App-Bundle hinzugefügt werden (per Drag & Drop in das Xcode-Projekt)

## Muster {#patterns}

### Zwei-Player-Audiomuster {#two-player-audio-pattern}

```swift
import AVKit

struct GameplayView: View {
    @State private var musicPlayer: AVAudioPlayer!
    @State private var sfxPlayer: AVAudioPlayer!

    private func playMusic() {
        let songs = [
            "let the mystery unfold",
            "spellcraft",
            "hiding place in the forest",
            "deep in the dell"
        ]
        let i = Int.random(in: 0...3)

        if let sound = Bundle.main.path(forResource: songs[i], ofType: "mp3") {
            musicPlayer = try! AVAudioPlayer(
                contentsOf: URL(fileURLWithPath: sound)
            )
            musicPlayer.numberOfLoops = -1   // loop forever
            musicPlayer.volume = 0.1         // 10% - subtle background
            musicPlayer.play()
        }
    }

    private func playSFX(_ name: String) {
        if let sound = Bundle.main.path(forResource: name, ofType: "mp3") {
            sfxPlayer = try! AVAudioPlayer(
                contentsOf: URL(fileURLWithPath: sound)
            )
            sfxPlayer.play()
        }
    }

    var body: some View {
        // ...
        .onAppear { playMusic() }
    }
}
```

Wichtig: `numberOfLoops = -1` lässt die Wiedergabe unbegrenzt wiederholen. `volume = 0.1` hält die Hintergrundmusik dezent.

### Soundeffekte {#sound-effects}

```swift
private func playFlipSound() {
    playSFX("page flip")
}

private func playWrongSound() {
    playSFX("negative beeps")
}

private func playCorrectSound() {
    playSFX("magic wand")
}
```

### Haptisches Feedback {#haptic-feedback}

```swift
import UIKit

private func giveWrongFeedback() {
    let generator = UINotificationFeedbackGenerator()
    generator.notificationOccurred(.error)
}

// Call outside withAnimation - haptic is not animated
.onTapGesture {
    withAnimation { /* visual changes */ }
    giveWrongFeedback()   // haptic separate from animation
}
```

Haptiktypen:
- `.error` – drei kurze Impulse (falsche Antwort)
- `.success` – zwei Impulse (richtige Antwort)
- `.warning` – ein einzelner kräftiger Impuls

### Lautstärkepegel {#audio-volume-levels}

| Kontext | Lautstärke | Begründung |
|---------|------------|------------|
| Hintergrundmusik | 0.1 | Dezent, nicht ablenkend |
| Soundeffekte | 1.0 (Standard) | Klares Feedback |
| UI-Sounds | 0.3-0.5 | Wahrnehmbar, aber nicht laut |

## Fallstricke {#gotchas}

- Die Verwendung eines einzelnen `AVAudioPlayer` für Musik und SFX führt dazu, dass die Musik dauerhaft stoppt, sobald ein SFX abgespielt wird
- `try!` bei der Initialisierung von `AVAudioPlayer` ist für gebündelte Dateien akzeptabel; Netzwerk-Audio sollte `try`/`catch` verwenden
- `Bundle.main.path(forResource:ofType:)` gibt nil zurück, wenn die Datei nicht im Bundle liegt – Dateinamen prüfen
- Haptik hat im Simulator keine Wirkung – auf einem echten Gerät testen
- `AVAudioPlayer` muss als Property (`@State`) gespeichert werden, sonst wird er deallokiert und die Wiedergabe stoppt
- Audiowiedergabe kann mit anderen Apps in Konflikt geraten – für Produktions-Apps eine Konfiguration von `AVAudioSession` in Betracht ziehen

## Siehe auch {#see-also}

- [[swiftui-animations]] – Abstimmung von Sound und Animations-Auslösern
- [[swiftui-state-and-data-flow]] – @State für Player-Referenzen
