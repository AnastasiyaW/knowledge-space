---
title: AVKit Audio and Haptic Feedback
category: concepts
tags: [ios-mobile, swiftui, avkit, audio, haptics, sound-effects, music]
---

# AVKit Audio and Haptic Feedback

AVKit provides audio playback for background music and sound effects. UIKit's feedback generators provide haptic feedback on physical devices. This entry covers the two-player audio pattern and haptic integration in SwiftUI.

## Key Facts

- `AVAudioPlayer` plays audio files from the app bundle
- Use two separate players (music + SFX) - one player causes SFX to interrupt music permanently
- `numberOfLoops = -1` loops audio indefinitely
- Haptic feedback uses `UINotificationFeedbackGenerator` from UIKit
- Haptics only work on physical devices, not the simulator
- Audio files must be added to the app bundle (drag into Xcode project)

## Patterns

### Two-Player Audio Pattern

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

Key: `numberOfLoops = -1` loops indefinitely. `volume = 0.1` keeps background music subtle.

### Sound Effects

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

### Haptic Feedback

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

Haptic types:
- `.error` - three quick taps (wrong answer)
- `.success` - two taps (correct answer)
- `.warning` - single strong tap

### Audio Volume Levels

| Context | Volume | Reason |
|---------|--------|--------|
| Background music | 0.1 | Subtle, non-distracting |
| Sound effects | 1.0 (default) | Clear feedback |
| UI sounds | 0.3-0.5 | Noticeable but not loud |

## Gotchas

- Using a single `AVAudioPlayer` for both music and SFX causes music to stop permanently when an SFX plays
- `try!` on `AVAudioPlayer` init is acceptable for bundled files; network audio should use `try`/`catch`
- `Bundle.main.path(forResource:ofType:)` returns nil if the file is not in the bundle - verify file names
- Haptics do nothing in the simulator - test on a real device
- `AVAudioPlayer` must be stored as a property (`@State`) or it gets deallocated and stops playing
- Audio playback may conflict with other apps - consider `AVAudioSession` configuration for production apps

## See Also

- [[swiftui-animations]] - coordinating sound with animation triggers
- [[swiftui-state-and-data-flow]] - @State for player references
