# ML Plugin Inference UX Patterns

Patterns for making slow ML inference (10-30s per operation) feel fast inside desktop creative applications (Photoshop, Lightroom, etc.). Covers caching, progressive preview, background pre-compute, batch queuing, and predictive prefetch.

## Latency Thresholds (Miller / Doherty)

| Threshold | Value | User perception |
|-----------|-------|----------------|
| Immediate | <100 ms | Direct manipulation — no perceived delay |
| Interactive | <400 ms (Doherty) | Seamless continuation |
| Responsive | 1-3 s | "System is working" — spinner acceptable |
| Background | 3-10 s | Progress bar required; user may switch tasks |
| Blocking | >10 s | Anti-pattern — must never block UI |

**Rule:** ML inference that takes >400 ms must run in background. The UI thread must never block.

## Per-Image Computation Cache

Cache per-image preprocessing results keyed by image hash. Eliminates redundant compute on repeated applies to the same image.

```python
import hashlib, pickle, os
from pathlib import Path

class InferenceCache:
    def __init__(self, cache_dir: str, max_entries: int = 50):
        self.dir = Path(cache_dir)
        self.dir.mkdir(exist_ok=True)
        self.max_entries = max_entries

    def _key(self, img_array) -> str:
        """Hash first 64KB of image data — fast, collision-rare."""
        sample = img_array.flat[:65536].tobytes()
        return hashlib.blake2b(sample, digest_size=16).hexdigest()

    def get(self, img_array, stage: str):
        key = self._key(img_array)
        path = self.dir / f"{key}_{stage}.pkl"
        if path.exists():
            with open(path, 'rb') as f:
                return pickle.load(f)
        return None

    def put(self, img_array, stage: str, value):
        key = self._key(img_array)
        path = self.dir / f"{key}_{stage}.pkl"
        with open(path, 'wb') as f:
            pickle.dump(value, f)
        self._evict_if_needed()

    def _evict_if_needed(self):
        entries = sorted(self.dir.glob("*.pkl"), key=os.path.getmtime)
        while len(entries) > self.max_entries:
            entries.pop(0).unlink()
```

**Cacheable stages per image:**
- Face detection landmarks (stable — image content doesn't change)
- Skin segmentation mask
- Frequency separation HF/LF layers
- VAE latent encoding (most expensive — cache first)

**Cache key:** Hash of raw pixel data, not filename. Filename-based keys miss in-place edits.

## Background Idle Pre-Compute

On image open, start computing expensive preprocessing stages during the idle period before the user clicks Apply. When Apply fires, pre-computed data is already available.

```python
import threading
from enum import Enum

class Stage(Enum):
    A = "face_landmarks"
    B = "skin_segmentation"
    C = "freq_sep"
    D = "vae_encode"

class BackgroundPrecompute:
    def __init__(self, cache: InferenceCache):
        self.cache = cache
        self._thread = None
        self._cancel = threading.Event()

    def start(self, img_array, on_stage_done=None):
        """Call when document is opened or becomes active."""
        self._cancel.clear()
        self._thread = threading.Thread(
            target=self._run, args=(img_array, on_stage_done), daemon=True
        )
        self._thread.start()

    def cancel(self):
        self._cancel.set()

    def _run(self, img, callback):
        stages = [
            (Stage.A, compute_face_landmarks),
            (Stage.B, compute_skin_seg),
            (Stage.C, compute_freq_sep),
            (Stage.D, compute_vae_latent),
        ]
        for stage, fn in stages:
            if self._cancel.is_set():
                return
            if self.cache.get(img, stage.value) is None:
                result = fn(img)
                self.cache.put(img, stage.value, result)
            if callback:
                callback(stage)
```

**Result:** First Apply on a freshly-opened image: ~23s cold start drops to ~8s if stages A-C completed in background (Stages A-C take ~6-8s combined; D is 12s and is the biggest win).

## Progressive Multi-Resolution Preview

Show a low-resolution result immediately, replace with full-resolution when ready. Never block Apply on full-resolution completion.

```python
RESOLUTION_PYRAMID = [
    (1/8, "draft",   target_ms=500),
    (1/4, "preview", target_ms=2000),
    (1/2, "refine",  target_ms=6000),
    (1/1, "final",   target_ms=None),
]

def apply_progressive(img, model, on_update):
    """
    on_update(layer_img, quality_label) called at each pyramid level.
    Caller replaces visible PS layer with each update.
    """
    import concurrent.futures
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def run_at_scale(scale):
        h, w = img.shape[:2]
        small = cv2.resize(img, (int(w*scale), int(h*scale)))
        result = model.infer(small)
        return cv2.resize(result, (w, h), interpolation=cv2.INTER_LANCZOS4)

    for scale, label, _ in RESOLUTION_PYRAMID:
        if executor._work_queue.qsize() > 0:
            break  # new Apply requested — abort current
        future = executor.submit(run_at_scale, scale)
        result = future.result()
        on_update(result, label)
```

**Tile-based streaming variant (for large images):**

```python
def apply_tiled_streaming(img, model, tile_size=512, on_tile=None):
    """
    Process tiles from center outward. Center tiles appear first —
    matches user attention (center of frame is subject).
    """
    h, w = img.shape[:2]
    tiles = []
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            cx, cy = x + tile_size//2, y + tile_size//2
            dist = ((cx - w//2)**2 + (cy - h//2)**2) ** 0.5
            tiles.append((dist, x, y))
    tiles.sort()  # process center-nearest first

    result = img.copy()
    for _, x, y in tiles:
        tile = img[y:y+tile_size, x:x+tile_size]
        out = model.infer(tile)
        result[y:y+tile_size, x:x+tile_size] = out
        if on_tile:
            on_tile(result)  # caller updates preview layer
    return result
```

## Intensity Slider (Lerp-Based Instant Preview)

After full ML inference completes, store both original and result. Slider becomes a lerp between them — instant, no re-inference.

```python
class LayerBlendController:
    def __init__(self, original, ml_result):
        self.orig = original.astype(np.float32)
        self.result = ml_result.astype(np.float32)
        self._dirty = False   # True if params changed requiring re-inference

    def at_intensity(self, t: float) -> np.ndarray:
        """t in [0..1]. Instant — no ML involved."""
        return np.clip(self.orig + t * (self.result - self.orig), 0, 255).astype(np.uint8)

    def refine_at(self, t: float, model, img, params):
        """Full ML re-inference at exact t. Use for "Accept" action only."""
        params['intensity'] = t
        self.result = model.infer(img, params)
        self._dirty = False
        return self.result
```

**UX pattern (borrowed from audio DAW "bounce"):**
1. Apply: show draft result at 1/4-res in ~2s
2. Background: full-res completes in ~23s, replaces draft
3. Slider drag: lerp between original and full-res result — 10ms/frame
4. "Refine" button: re-inference at exact slider position — ~23s, gives accurate (non-lerp) result

## Batch Queue

Background processing queue that never blocks Photoshop UI. User adds images and continues working.

```text
Queue state machine:
  Idle → (user adds image) → Queued → (worker picks up) → Processing → Done
  Processing → (user clicks current image) → Interrupted → Queued (reprioritized)

Priority rules:
  1. Current active document (always first)
  2. ★ Hero-marked images (full quality)
  3. Queue order (FIFO)
  4. Background items (deferred)
```

**Session-level cache for batch series (same shooting session):**
- Face detection model: stays warm in VRAM across batch
- Skin-tone prior: computed from first 5 images, shared with remaining 45
- LoRA weights: loaded once for entire batch
- Result: batch throughput ~60-70% of theoretical sequential × N

**Acceptance criteria (Phase 1):**
- 2nd Apply on same file: <8s (cache hit)
- 10-image batch: completes in 4 min vs 10 min sequential
- Perceived time on single Apply: 5-8s (user study, questionnaire)

## Predictive Prefetch (Markov Chain)

Build a Markov chain of user action sequences from PS event history. After `D&B Apply`, prefetch `Volume` inputs if transition probability > 40%.

```python
from collections import defaultdict

class ActionPredictor:
    def __init__(self, min_probability: float = 0.40):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.min_prob = min_probability

    def record(self, from_action: str, to_action: str):
        self.transitions[from_action][to_action] += 1

    def predict_next(self, current_action: str) -> str | None:
        counts = self.transitions[current_action]
        if not counts:
            return None
        total = sum(counts.values())
        best = max(counts, key=counts.get)
        prob = counts[best] / total
        return best if prob >= self.min_prob else None

    def should_prefetch(self, current_action: str) -> bool:
        return self.predict_next(current_action) is not None
```

**Default priors from retoucher community data:**
```python
DEFAULT_TRANSITIONS = {
    'db_apply':     {'volume_apply': 0.70, 'beauty_apply': 0.40},
    'volume_apply': {'beauty_apply': 0.62, 'color_apply': 0.40},
    'beauty_apply': {'color_apply': 0.20},
}
```

After 20-30 sessions, per-user model overrides defaults. Adaptive: retoucher who always does D&B → Color (not Volume) will have that transition reinforced.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Modal spinner blocking PS UI | Users cannot work while plugin thinks | Always background; layer appears when ready |
| Spinner without context | 23s with "Loading…" = rage | Progress bar + stage name + time estimate |
| Auto-apply to all layers | Violates non-destructive culture | One Apply = one explicit new layer |
| "Fast mode" checkbox | Stigmatizes quality; complicates docs | Auto-select quality by content (hero vs batch) |
| Streaming animation always on | Blurry intermediate irritates pros | Optional toggle; default off for production users |
| Cloud offload by default | Offline expectation; privacy concern | Local first; cloud = explicit opt-in |
| Stochastic inference (random seed) | Breaks undo/redo consistency | Fixed seed = hash(image_path + params) |
| Re-inference on every slider tick | 23s per tick = unusable | Lerp between cached results; re-infer only on Accept |

## Gotchas

- **Issue:** Background precompute starts, then user opens different image — precomputed cache from wrong image gets used. -> **Fix:** Include document ID or pixel hash in every cache key. Cancel and restart `BackgroundPrecompute` on `documentChanged` event.
- **Issue:** Batch queue uses FIFO, but user star-marks a hero shot mid-queue — it waits until its turn. -> **Fix:** Implement priority re-ordering: ★ hero images jump to position 1 in queue. Current processing item finishes (no mid-inference cancel — atomic layer commit required).
- **Issue:** Lerp-based intensity slider produces wrong result for non-linear ML operations (beauty/frequency adjustments are not linear). -> **Fix:** Label the lerp as "preview intensity"; provide "Refine at X%" button that triggers full re-inference at the chosen intensity value and replaces the lerp result.
- **Issue:** VAE latent cache is stale after in-application editing (layer added, curves adjustment) — content hash unchanged, latent wrong. -> **Fix:** Key the VAE latent cache on (pixel hash + composite layer stack hash). Invalidate on any layer modification to the source document.
- **Issue:** Per-session skin-tone prior built from first 5 images propagates a skin cast from a badly-lit photo to all subsequent batch images. -> **Fix:** Use prior only as weak regularizer (weight 0.1), not hard target. Each image still gets independent skin segmentation; prior only smooths boundary cases.

## See Also

- [[frequency-decomposition-editing]] - HF/LF cache entries for skin retouch pipeline
- [[diffusion-lora-training]] - batch inference considerations for LoRA-based operators
- [[tile-position-encoding]] - position-aware tiling for high-res progressive rendering
