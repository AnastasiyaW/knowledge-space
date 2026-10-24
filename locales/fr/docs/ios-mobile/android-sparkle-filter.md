---
title: "Filtre Sparkle / Glitter en temps réel sur Android"
category: techniques
tags: [android, camerax, liteRT, opengl, shader, voronoi, realtime, segmentation]
aliases: ["Sparkle Filter", "Glitter Effect Android", "Android CameraX Shader"]
level: 3
source_sha256: 98bdb7d17a47944f0675f71c82dd38e0fd31914476472de33c36bceaa80c7832
translation: machine
translated_at: '2026-10-24'
---
# Filtre Sparkle / Glitter en temps réel sur Android {#android-realtime-sparkle-glitter-filter}

Implémentation d'effets sparkle/glitter en temps réel sur les vêtements, dans l'aperçu de la caméra en direct sous Android. Objectif : 30 ips sur les appareils de milieu de gamme (2022 et après). Stack : CameraX + LiteRT (successeur de TFLite) + OpenGL ES 3.1.

## Vue d'ensemble de l'architecture {#architecture-overview}

```text
CameraX (preview frame)
    ↓
LiteRT segmentation model (clothing mask)
    ↓
OpenGL ES 3.1 compute shader (Voronoi sparkle)
    ↓
SurfaceView / TextureView (display)
```

## Configuration de CameraX {#camerax-setup}

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

## Segmentation avec LiteRT (successeur de TFLite) {#litert-tflite-successor-segmentation}

LiteRT est le nouveau nom de TFLite donné par Google (depuis 2024). Utilisez `com.google.android.gms:play-services-tflite-gpu` pour le délégué GPU.

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

### Options de modèles pour la segmentation des vêtements {#model-options-for-clothing-segmentation}

| Modèle | Taille | Vitesse | Remarques |
|-------|------|-------|-------|
| MediaPipe Selfie Segmentation | ~1 Mo | Rapide | Masque de personne (non spécifique aux vêtements) |
| MobileNetV3 + DeepLabV3 | ~3 Mo | Moyenne | Segmentation sémantique, nécessite des classes de vêtements |
| EfficientSeg personnalisé | 2-5 Mo | Rapide | Entraîné sur un jeu de données mode pour ne cibler que les vêtements |
| YOLOv8n-seg | ~6 Mo | Rapide | Multi-classes, adapté aux zones de vêtements |

Pour les effets sparkle, un masque de personne (non spécifique aux vêtements) fonctionne souvent assez bien : l'effet paraît naturel sur n'importe quel vêtement porté.

## Shader Voronoi sparkle en OpenGL ES 3.1 {#opengl-es-31-voronoi-sparkle-shader}

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

## Optimisation des performances {#performance-optimization}

### Atteindre 30 ips sur les appareils de milieu de gamme {#achieving-30fps-on-mid-range-devices}

| Optimisation | Impact | Remarques |
|-------------|--------|-------|
| Délégué GPU pour la segmentation | 3-5x | Délégué GPU de LiteRT |
| Segmentation à 256 px (et non 512 px) | 2x plus rapide | Le masque est de toute façon flouté |
| Mise à jour du masque toutes les 2 images | 15 ms économisées | Les vêtements ne bougent pas vite |
| OpenGL ES 3.1 (et non ES 2.0) | Compute shaders | Requis pour le pipeline moderne |
| Rendu dans un FBO, et non directement | Évite les blocages | Rendu hors écran |

### Pipeline d'images {#frame-pipeline}

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

### Budget VRAM {#vram-budget}

| Composant | Mémoire |
|-----------|--------|
| Texture caméra (RGBA 1080p) | ~8 Mo |
| Modèle de segmentation (TFLite) | 2-6 Mo |
| Texture de masque (256×256) | 0,25 Mo |
| Tampons intermédiaires du shader | 2-4 Mo |
| **Total** | ~15 Mo |

Cela tient largement dans le budget GPU des appareils de milieu de gamme (300-500 Mo disponibles pour les applications).

## Contrôle de l'intensité et de l'animation {#intensity-and-animation-control}

```kotlin
// Expose to UI
interface SparkleControl {
    var intensity: Float     // 0.0 = off, 1.0 = maximum sparkle
    var speed: Float         // 0.5 = slow, 2.0 = fast animation
    var color: FloatArray    // RGB sparkle color tint
    var cellSize: Float      // 10.0 = coarse, 40.0 = fine sparkle
}
```

## Pièges à éviter {#gotchas}

- **Nommage LiteRT et TFLite** : depuis 2024, Google a renommé TensorFlow Lite en LiteRT. L'artefact gradle est `com.google.ai.edge.litert:litert`, mais les fichiers de modèle `.tflite` existants fonctionnent toujours sans modification.
- **Format d'image CameraX** : utilisez `OUTPUT_IMAGE_FORMAT_RGBA_8888` pour faciliter le transfert de texture vers le GPU. Le format YUV_420_888 par défaut nécessite une étape de conversion avant l'envoi vers une texture OpenGL.
- **Contexte OpenGL sur le thread caméra** : n'appelez pas les méthodes GLES depuis le thread d'analyse de CameraX, elles doivent s'exécuter sur le thread GL. Utilisez une texture partagée (`GLES11Ext.GL_TEXTURE_EXTERNAL_OES`) pour un transfert d'images sans copie.
- **Voronoi à très petites tailles de cellule** (échelle > 60.0) produit un aliasing visible à la résolution de lecture. Conservez une échelle de cellule entre 15 et 40 pour un rendu lisse, et compensez en gagnant en richesse avec un mélange multi-échelle.
- **Consommation de batterie** : un shader de calcul GPU continu combiné à l'inférence neuronale épuise environ 15-20 % de batterie par heure sur les appareils de milieu de gamme. Prévenez les utilisateurs et proposez une mise en pause automatique lorsque l'aperçu de la caméra n'est pas visible.

## Voir aussi {#see-also}

- [[android-mvvm-architecture]] - Architecture d'application Android pour les fonctionnalités caméra
- [[android-room-database]] - stockage des paramètres utilisateur et des préréglages de filtres
- [[low-vram-inference-strategies]] - sélection de modèles légers pour l'inférence mobile
