---
title: "Android-Echtzeitfilter für Glitzer- und Funkeleffekte"
category: techniques
tags: [android, camerax, liteRT, opengl, shader, voronoi, realtime, segmentation]
aliases: ["Sparkle Filter", "Glitter Effect Android", "Android CameraX Shader"]
level: 3
source_sha256: 98bdb7d17a47944f0675f71c82dd38e0fd31914476472de33c36bceaa80c7832
translation: machine
translated_at: '2026-10-24'
---
# Android-Echtzeitfilter für Glitzer- und Funkeleffekte {#android-realtime-sparkle-glitter-filter}

Implementierung von Echtzeit-Glitzer- und Funkeleffekten auf Kleidung in der Live-Kameravorschau auf Android. Ziel: 30 fps auf Mittelklasse-Geräten (ab 2022). Stack: CameraX + LiteRT (Nachfolger von TFLite) + OpenGL ES 3.1.

## Architekturüberblick {#architecture-overview}

```text
CameraX (preview frame)
    ↓
LiteRT segmentation model (clothing mask)
    ↓
OpenGL ES 3.1 compute shader (Voronoi sparkle)
    ↓
SurfaceView / TextureView (display)
```

## CameraX-Einrichtung {#camerax-setup}

```kotlin
val cameraProviderFuture = ProcessCameraProvider.getInstance(context)

cameraProviderFuture.addListener({
    val cameraProvider = cameraProviderFuture.get()

    val preview = Preview.Builder()
        .setTargetAspectRatio(AspectRatio.RATIO_16_9)
        .build()
        .also { it.setSurfaceProvider(viewBinding.previewView.surfaceProvider) }

    val imageAnalysis = ImageAnalysis.Builder()
        .setTargetAspectRatio(AspectRatio.RATIO_16_9)
        .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
        .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_RGBA_8888)
        .build()

    imageAnalysis.setAnalyzer(cameraExecutor) { imageProxy ->
        processFrame(imageProxy)
        imageProxy.close()
    }

    cameraProvider.bindToLifecycle(
        lifecycleOwner, CameraSelector.DEFAULT_BACK_CAMERA,
        preview, imageAnalysis
    )
}, ContextCompat.getMainExecutor(context))
```

## LiteRT-Segmentierung (Nachfolger von TFLite) {#litert-tflite-successor-segmentation}

LiteRT ist Googles Neubenennung von TFLite (Stand 2024). Für den GPU-Delegate wird `com.google.android.gms:play-services-tflite-gpu` verwendet.

```kotlin
// build.gradle
dependencies {
    implementation("com.google.ai.edge.litert:litert:1.0.1")
    implementation("com.google.ai.edge.litert:litert-gpu:1.0.1")
}
```

```kotlin
class ClothingSegmentor(context: Context) {
    private val interpreter: Interpreter

    init {
        val gpuDelegate = GpuDelegate()
        val options = Interpreter.Options().addDelegate(gpuDelegate)
        val modelBuffer = loadModelFile(context, "clothing_segmentation.tflite")
        interpreter = Interpreter(modelBuffer, options)
    }

    fun segment(bitmap: Bitmap): FloatArray {
        // Resize to model input (typically 256x256 or 512x512)
        val input = Bitmap.createScaledBitmap(bitmap, INPUT_SIZE, INPUT_SIZE, true)
        val inputArray = bitmapToFloatArray(input)
        val outputArray = Array(1) { Array(INPUT_SIZE) { FloatArray(INPUT_SIZE) } }
        interpreter.run(arrayOf(inputArray), outputArray)
        return outputArray[0].flatten().toFloatArray()
    }
}
```

### Modelloptionen für die Kleidungssegmentierung {#model-options-for-clothing-segmentation}

| Modell | Größe | Geschwindigkeit | Hinweise |
|-------|------|-------|-------|
| MediaPipe Selfie Segmentation | ~1 MB | Schnell | Personenmaske (nicht kleidungsspezifisch) |
| MobileNetV3 + DeepLabV3 | ~3 MB | Mittel | Semantische Segmentierung, benötigt Kleidungsklassen |
| Eigenes EfficientSeg | 2-5 MB | Schnell | Auf Modedatensatz für reine Kleidungssegmentierung trainiert |
| YOLOv8n-seg | ~6 MB | Schnell | Mehrklassig, gut für Kleidungsbereiche |

Für Funkeleffekte funktioniert oft eine Personenmaske (nicht kleidungsspezifisch) ausreichend gut – der Effekt wirkt auf jedem getragenen Kleidungsstück natürlich.

## OpenGL ES 3.1 Voronoi-Funkel-Shader {#opengl-es-31-voronoi-sparkle-shader}

```glsl
// Fragment shader - Voronoi-based sparkle
#version 310 es
precision mediump float;

uniform sampler2D uCameraTexture;   // input camera frame
uniform sampler2D uMaskTexture;     // clothing segmentation mask
uniform float uTime;                // animation time (seconds)
uniform float uIntensity;           // sparkle density 0.0-1.0
uniform vec2 uResolution;

out vec4 fragColor;

// Random hash function
vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453);
}

// Animated Voronoi cells
float voronoi(vec2 uv, float time) {
    vec2 i = floor(uv);
    vec2 f = fract(uv);

    float minDist = 1.0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec2 neighbor = vec2(float(x), float(y));
            vec2 point = hash2(i + neighbor);
            // Animate point position
            point = 0.5 + 0.5 * sin(time * 2.0 + 6.2831 * point);
            vec2 diff = neighbor + point - f;
            float dist = length(diff);
            minDist = min(minDist, dist);
        }
    }
    return minDist;
}

void main() {
    vec2 uv = gl_FragCoord.xy / uResolution;
    vec4 cameraColor = texture(uCameraTexture, uv);
    float mask = texture(uMaskTexture, uv).r;

    if (mask < 0.5) {
        // Not clothing - pass through
        fragColor = cameraColor;
        return;
    }

    // Voronoi sparkle at varying scales for depth
    float v1 = voronoi(uv * 20.0, uTime * 1.2);
    float v2 = voronoi(uv * 40.0, uTime * 2.0);

    // Threshold to create sharp sparkle points
    float sparkle = step(0.05, v1) * step(0.03, v2);
    sparkle = 1.0 - sparkle;  // invert: 1 = sparkle location

    // Brightness flicker per sparkle location
    float flicker = sin(uTime * 8.0 + hash2(floor(uv * 20.0)).x * 6.28) * 0.5 + 0.5;
    sparkle *= flicker;

    // Blend sparkle onto camera frame
    vec3 sparkleColor = vec3(1.0, 0.98, 0.9);  // warm white
    vec3 result = mix(cameraColor.rgb, sparkleColor, sparkle * uIntensity * mask);

    fragColor = vec4(result, 1.0);
}
```

## Performance-Optimierung {#performance-optimization}

### 30 fps auf Mittelklasse-Geräten erreichen {#achieving-30fps-on-mid-range-devices}

| Optimierung | Wirkung | Hinweise |
|-------------|--------|-------|
| GPU-Delegate für Segmentierung | 3-5x | LiteRT GPU-Delegate |
| Segmentierung bei 256px (statt 512px) | 2x schneller | Die Maske wird ohnehin weichgezeichnet |
| Maskenaktualisierung alle 2 Frames | 15 ms gespart | Kleidung bewegt sich nicht schnell |
| OpenGL ES 3.1 (nicht ES 2.0) | Compute-Shader | Für moderne Pipeline erforderlich |
| Rendering in FBO statt direkt | Vermeidet Stalls | Off-Screen-Rendering |

### Frame-Pipeline {#frame-pipeline}

```kotlin
class SparkleRenderer : GLSurfaceView.Renderer {
    private var frameCount = 0

    override fun onDrawFrame(gl: GL10) {
        frameCount++
        val cameraFrame = latestCameraFrame ?: return

        // Update segmentation every 2 frames
        if (frameCount % 2 == 0) {
            clothingMask = segmentor.segment(cameraFrame)
            maskTexture.update(clothingMask)
        }

        // Always update shader params
        shader.setUniform("uTime", SystemClock.elapsedRealtime() / 1000f)
        shader.setUniform("uIntensity", userIntensitySetting)

        // Draw
        GLES31.glDrawArrays(GLES31.GL_TRIANGLE_STRIP, 0, 4)
    }
}
```

### VRAM-Budget {#vram-budget}

| Komponente | Speicher |
|-----------|--------|
| Kamera-Textur (1080p RGBA) | ~8 MB |
| Segmentierungsmodell (TFLite) | 2-6 MB |
| Maskentextur (256×256) | 0,25 MB |
| Zwischenpuffer des Shaders | 2-4 MB |
| **Gesamt** | ~15 MB |

Passt gut in das GPU-Budget von Mittelklasse-Geräten (300-500 MB für Apps verfügbar).

## Steuerung von Intensität und Animation {#intensity-and-animation-control}

```kotlin
// Expose to UI
interface SparkleControl {
    var intensity: Float     // 0.0 = off, 1.0 = maximum sparkle
    var speed: Float         // 0.5 = slow, 2.0 = fast animation
    var color: FloatArray    // RGB sparkle color tint
    var cellSize: Float      // 10.0 = coarse, 40.0 = fine sparkle
}
```

## Stolperfallen {#gotchas}

- **LiteRT vs. TFLite-Benennung**: Stand 2024 hat Google TensorFlow Lite in LiteRT umbenannt. Das Gradle-Artefakt lautet `com.google.ai.edge.litert:litert`, bestehende `.tflite`-Modelldateien funktionieren aber unverändert weiter.
- **CameraX-Frameformat**: Verwende `OUTPUT_IMAGE_FORMAT_RGBA_8888` für einen einfachen GPU-Texturupload. Das Standardformat YUV_420_888 erfordert vor dem Hochladen in eine OpenGL-Textur einen Konvertierungsschritt.
- **OpenGL-Kontext im Kamera-Thread**: Rufe keine GLES-Methoden aus dem CameraX-Analyzer-Thread auf – sie müssen im GL-Thread laufen. Verwende eine gemeinsame Textur (`GLES11Ext.GL_TEXTURE_EXTERNAL_OES`) für die kopierfreie Übertragung der Frames.
- **Voronoi bei sehr kleinen Zellgrößen** (Skalierung >60,0) erzeugt bei der Wiedergabeauflösung sichtbares Aliasing. Halte die Zellskalierung bei 15-40 für ein glattes Erscheinungsbild; zur Erhöhung der Vielfalt kompensiere mit Multiskalen-Überblendung.
- **Akkuverbrauch**: Kontinuierlicher GPU-Compute-Shader zusammen mit neuronaler Inferenz verbraucht auf Mittelklasse-Geräten etwa 15-20 % Akku pro Stunde. Warne Nutzer und biete eine automatische Pause, wenn die Kameravorschau nicht sichtbar ist.

## Siehe auch {#see-also}

- [[android-mvvm-architecture]] - Android-App-Architektur für Kamerafunktionen
- [[android-room-database]] - Speichern von Nutzereinstellungen und Filtervorlagen
- [[low-vram-inference-strategies]] - Auswahl leichtgewichtiger Modelle für die mobile Inferenz
