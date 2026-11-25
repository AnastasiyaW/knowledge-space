---
title: "AVKit Audio and Haptic Feedback"
category: concepts
tags: [ios-mobile, swiftui, avkit, audio, haptics, sound-effects, music]
level: 3
source_sha256: 146c709664919f1d28579196cd945b4a7ab25af7d6ac2bf758976e2fd2902f52
translation: machine
translated_at: '2026-10-24'
---
# AVKit : audio et retour haptique {#avkit-audio-and-haptic-feedback}

AVKit assure la lecture audio pour la musique d'arrière-plan et les effets sonores. Les générateurs de retour d'UIKit fournissent le retour haptique sur les appareils physiques. Cette entrée couvre le modèle à deux lecteurs audio et l'intégration haptique dans SwiftUI.

## Points clés {#key-facts}

- `AVAudioPlayer` lit des fichiers audio depuis le bundle de l'application
- Utilisez deux lecteurs distincts (musique + effets) : avec un seul lecteur, les effets sonores interrompent la musique de façon permanente
- `numberOfLoops = -1` fait boucler l'audio indéfiniment
- Le retour haptique utilise `UINotificationFeedbackGenerator` d'UIKit
- Les retours haptiques ne fonctionnent que sur les appareils physiques, pas sur le simulateur
- Les fichiers audio doivent être ajoutés au bundle de l'application (glisser-déposer dans le projet Xcode)

## Modèles {#patterns}

### Modèle à deux lecteurs audio {#two-player-audio-pattern}

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

Point clé : `numberOfLoops = -1` fait boucler l'audio indéfiniment. `volume = 0.1` garde la musique d'arrière-plan discrète.

### Effets sonores {#sound-effects}

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

### Retour haptique {#haptic-feedback}

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

Types haptiques :
- `.error` : trois petites vibrations rapides (mauvaise réponse)
- `.success` : deux vibrations (bonne réponse)
- `.warning` : une seule vibration forte

### Niveaux de volume audio {#audio-volume-levels}

| Contexte | Volume | Raison |
|---------|--------|--------|
| Musique d'arrière-plan | 0.1 | Discrète, non distrayante |
| Effets sonores | 1.0 (par défaut) | Retour clair |
| Sons d'interface | 0.3-0.5 | Perceptible mais pas trop fort |

## Pièges {#gotchas}

- Utiliser un seul `AVAudioPlayer` pour la musique et les effets sonores fait que la musique s'arrête définitivement dès qu'un effet est joué
- `try!` à l'initialisation d'`AVAudioPlayer` est acceptable pour les fichiers embarqués ; l'audio réseau doit utiliser `try`/`catch`
- `Bundle.main.path(forResource:ofType:)` renvoie nil si le fichier n'est pas dans le bundle : vérifiez les noms de fichiers
- Les retours haptiques ne font rien dans le simulateur : testez sur un appareil réel
- `AVAudioPlayer` doit être stocké comme propriété (`@State`), sinon il est désalloué et cesse de jouer
- La lecture audio peut entrer en conflit avec d'autres applications : envisagez la configuration de `AVAudioSession` pour les applications en production

## Voir aussi {#see-also}

- [[swiftui-animations]] - coordonner le son avec les déclencheurs d'animation
- [[swiftui-state-and-data-flow]] - @State pour les références aux lecteurs
