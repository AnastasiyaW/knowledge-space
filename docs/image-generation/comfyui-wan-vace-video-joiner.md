# ComfyUI Wan VACE Video Joiner

The Wan VACE Video Joiner is a node suite designed for assembling disparate video segments into a continuous sequence using generative AI transitions. It leverages the Visual AutoEncoder (VACE) architectures from Wan 2.1 and Wan 2.2 (Fun VACE) to synthesize intermediate frames, ensuring motion continuity across clip boundaries.

## Technical Architecture
The system operates by analyzing the terminal frames of a leading clip and the initial frames of the subsequent clip. Instead of simple cross-fading, it employs a generative diffusion pass to fill the temporal gap.

- **VACE Integration:** Supports Wan 2.1 VACE for standard high-fidelity reconstructions and Wan 2.2 Fun VACE for optimized or stylized video workflows.
- **Boundary Synthesis:** Identifies and replaces noisy or artifact-heavy frames at clip edges with newly generated content that aligns with the global motion vector.
- **Source Agnosticism:** While optimized for Wan and LTX-2 outputs, the joiner accepts any standard video tensor input provided they share a consistent resolution and frame rate.

## Seamless Looping Logic
The joiner includes a dedicated mode for cyclic video generation. It treats the final frames of the last shot as the prefix for the first shot's transition, creating a seamless "infinite loop" by synthesizing a bridge that closes the temporal circuit.

### Parameter Configuration
```text
VideoJoinerNode:
  transition_frames: 8          # Number of synthesized frames between clips
  denoise_strength: 0.65       # Intensity of the generative pass on boundary frames
  vace_model: "wan_2.1_vace"   # Selection of the reconstruction backend
  loop_mode: true              # Connects the tail of the last clip to the head of the first
```

## Implementation Workflow
The typical pipeline involves loading multiple video latent or pixel tensors, passing them through the Joiner node, and performing a final VAE decode if the transitions were handled in latent space.

### Example Node Logic
```python
def join_clips(clip_list, transition_len=4):
    # Conceptual representation of the joining process
    assembled_tensor = []
    for i in range(len(clip_list) - 1):
        transition = generate_vace_bridge(
            clip_list[i].tail(), 
            clip_list[i+1].head(), 
            frames=transition_len
        )
        assembled_tensor.extend([clip_list[i], transition])
    return assembled_tensor
```

## Gotchas
- **Issue:** VRAM spikes during transition generation → **Fix:** Reduce the `transition_frames` parameter or use a tiled VAE decoding approach if the resolution exceeds 720p.
- **Issue:** Motion jitter at boundaries → **Fix:** Ensure the source clips have a consistent frame rate (FPS) before joining; use a higher `denoise_strength` to allow the AI to better blend disparate motion vectors.
- **Issue:** Style drift in transitions → **Fix:** Use the same VACE version (e.g., Wan 2.1) for both the original video generation and the joiner node to prevent color or texture shifts.

## See Also
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
- [[RealRestorer]]
- [[image-restoration-survey]]
- [[flux-klein-9b-inference]]

