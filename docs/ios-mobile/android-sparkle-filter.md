---
title: Android Realtime Sparkle / Glitter Filter
category: techniques
tags: [android, camerax, liteRT, opengl, shader, voronoi, realtime, segmentation]
aliases: ["Sparkle Filter", "Glitter Effect Android", "Android CameraX Shader"]
---

# Android Realtime Sparkle / Glitter Filter

Implementing realtime sparkle/glitter effects on clothing in live camera preview on Android. Target: 30fps on mid-range devices (2022+). Stack: CameraX + LiteRT (TFLite successor) + OpenGL ES 3.1.

## Architecture Overview

```
CameraX (preview frame)
    ↓
LiteRT segmentation model (clothing mask)
    ↓
OpenGL ES 3.1 compute shader (Voronoi sparkle)
    ↓
SurfaceView / TextureView (display)
```

## CameraX Setup

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

## LiteRT (TFLite Successor) Segmentation

LiteRT = Google's rebranding of TFLite (as of 2024). Use `com.google.android.gms:play-services-tflite-gpu` for GPU delegate.

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

### Model Options for Clothing Segmentation

| Model | Size | Speed | Notes |
|-------|------|-------|-------|
| MediaPipe Selfie Segmentation | ~1 MB | Fast | Person mask (not clothing-specific) |
| MobileNetV3 + DeepLabV3 | ~3 MB | Medium | Semantic segmentation, needs clothing classes |
| Custom EfficientSeg | 2-5 MB | Fast | Train on fashion dataset for clothing-only |
| YOLOv8n-seg | ~6 MB | Fast | Multi-class, good for clothing areas |

For sparkle effects, person mask (not clothing-specific) often works well enough - the effect looks natural on any worn item.

## OpenGL ES 3.1 Voronoi Sparkle Shader

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

## Performance Optimization

### Achieving 30fps on Mid-Range Devices

| Optimization | Impact | Notes |
|-------------|--------|-------|
| GPU delegate for segmentation | 3-5x | LiteRT GPU delegate |
| Segmentation at 256px (not 512px) | 2x faster | Mask is blurred anyway |
| Mask update every 2 frames | 15ms saved | Clothing doesn't move fast |
| OpenGL ES 3.1 (not ES 2.0) | Compute shaders | Required for modern pipeline |
| Render to FBO, not direct | Avoids stalls | Off-screen rendering |

### Frame Pipeline

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

### VRAM Budget

| Component | Memory |
|-----------|--------|
| Camera texture (1080p RGBA) | ~8 MB |
| Segmentation model (TFLite) | 2-6 MB |
| Mask texture (256×256) | 0.25 MB |
| Shader intermediate buffers | 2-4 MB |
| **Total** | ~15 MB |

Fits well within mid-range device GPU budget (300-500 MB available for apps).

## Intensity and Animation Control

```kotlin
// Expose to UI
interface SparkleControl {
    var intensity: Float     // 0.0 = off, 1.0 = maximum sparkle
    var speed: Float         // 0.5 = slow, 2.0 = fast animation
    var color: FloatArray    // RGB sparkle color tint
    var cellSize: Float      // 10.0 = coarse, 40.0 = fine sparkle
}
```

## Gotchas

- **LiteRT vs TFLite naming**: as of 2024, Google rebranded TensorFlow Lite to LiteRT. The gradle artifact is `com.google.ai.edge.litert:litert`, but existing `.tflite` model files still work unchanged.
- **CameraX frame format**: use `OUTPUT_IMAGE_FORMAT_RGBA_8888` for easy GPU texture upload. The default YUV_420_888 requires a conversion step before uploading to OpenGL texture.
- **OpenGL context on camera thread**: don't call GLES methods from the CameraX analyzer thread — they must run on the GL thread. Use a shared texture (`GLES11Ext.GL_TEXTURE_EXTERNAL_OES`) for zero-copy frame transfer.
- **Voronoi at very small cell sizes** (>60.0 scale) produces visible aliasing at playback resolution. Keep cell scale 15-40 for smooth appearance; compensate with multi-scale blending for richness.
- **Battery drain**: continuous GPU compute shader + neural inference will drain ~15-20% battery per hour on mid-range devices. Warn users, provide auto-pause when camera preview is not visible.

## See Also

- [[android-mvvm-architecture]] - Android app architecture for camera features
- [[android-room-database]] - storing user settings and filter presets
- [[low-vram-inference-strategies]] - lightweight model selection for mobile inference
