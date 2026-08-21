---
title: Perspective Calibration for Object Compositing
description: A local decision framework for estimating camera geometry, validating it with scene evidence, and deriving a stable placement transform before compositing an object.
---

# Perspective Calibration for Object Compositing

Perspective calibration is the geometry stage **before** object compositing. Its output is a defensible camera-and-support-plane hypothesis: intrinsics `K`, camera orientation, horizon, and a plane mapping. It does not make a cut-out match the scene; it prevents a later compositor from trying to hide an impossible scale, tilt, or contact point.

Use calibration when the inserted object must rest on a planar surface, share converging edges, or remain plausible after a small reposition. For a flat graphic placed parallel to the image plane, use a 2D transform instead. For an object that must be viewed from a materially different angle, acquire/render a matching view; a single-image calibration does not recover hidden geometry.

## Decide What Must Be Estimated

Start from the edit, not the model:

- **Placement only on a known plane:** estimate `K`, orientation, and one support-plane homography. This is the normal product-on-floor, sign-on-wall, or furniture-on-ground case.
- **Visible architecture or road markings:** extract lines and require agreement between their vanishing directions and the camera estimate.
- **Weak, curved, or texture-only context:** use a learned single-image estimate as a proposal, but require manual horizon/anchors or a second image before committing a high-stakes placement.
- **Need local surface orientation or occlusion:** add monocular depth/normals after camera calibration. Treat their scale as uncertain unless the source provides metric constraints that fit the scene.
- **Strong barrel/fisheye distortion:** rectify first or select a camera model that represents it. A pinhole estimate on a visibly distorted image is not a calibration failure that a compositor can repair.

The minimum deliverable is not a focal-length number. Persist the image dimensions, camera model, `K`, rotation convention, horizon, support-plane definition, anchors, and a validation overlay. Those artifacts make the object transform reproducible and expose when a later crop or resize invalidates it.

## Tool Selection and Legal Boundary

The table is deliberately short: select an estimator for the unknown, then a separate evidence source for validation. “Activity” is the GitHub repository `pushed_at` value checked on **2026-08-21**; it signals maintenance recency, not accuracy. Code and checkpoint terms are separate assets and must be recorded separately in a release manifest.

| Role | Use when | Local interface or output | Code license | Weight/checkpoint terms | Activity checked 2026-08-21 |
|---|---|---|---|---|---|
| [GeoCalib](https://github.com/cvg/GeoCalib) | Default single-image intrinsics + gravity proposal | `GeoCalib().calibrate(image)` returns camera, gravity, covariance/confidence fields; pinhole and radial-family models | Apache-2.0 | The official repository downloads `pinhole`/`distorted` artifacts from its GitHub release. No separate checkpoint license was stated in the repository README or LICENSE at check time; review the exact release artifact before redistribution. | 2026-08-16 |
| [DeepLSD](https://github.com/cvg/DeepLSD) | Accurate scene lines and independent VP evidence | line segments; repository export supports `--pred_vps` | MIT | Official checkpoints are hosted at `cvg-data.inf.ethz.ch`; no separate weight license is stated in the README. | 2025-01-09 |
| [CTRL-C](https://github.com/jwlee-vcl/CTRL-C) | Independent line-conditioned calibration proposal | vanishing points, focal length, horizon line from image + line segments | Apache-2.0 | Official checkpoints are linked from Google Drive; the repository license covers code, while distinct checkpoint terms are not stated there. | 2024-06-25 |
| [MoGe](https://github.com/microsoft/MoGe) | Need depth, normals, intrinsics, and FoV to build support/occlusion evidence | point map, depth, normals, normalized intrinsics | MIT; bundled DINOv2 subtree is Apache-2.0 | The official `Ruicheng/moge-2-vitl-normal` model card declares `mit` as of the check date. Re-check the precise model card and every dependency for the selected revision. | 2026-08-19 |

For a commercially distributable pipeline, prefer a tool only after the **exact code revision and exact downloaded checkpoint** are each attached to their applicable terms. “Open repository” and “downloadable checkpoint” are not license classifications.

## Calibration Pipeline

1. **Normalize the source.** Preserve the original pixels and EXIF separately. Record any crop, resize, rotation, or lens correction. Run inference on the same raster used for placement; otherwise transform `K` and all anchors by the identical image transform.
2. **Choose the camera model.** Begin with pinhole for rectilinear imagery. Escalate to a radial model only when straight scene edges visibly bow; do not use an extra distortion parameter merely to absorb bad anchors.
3. **Generate a camera proposal.** Estimate intrinsics and gravity with GeoCalib, saving camera parameters plus covariance/confidence outputs. GeoCalib assumes the principal point is centered and does not optimise it, so treat strongly cropped or off-axis images as a review case.
4. **Extract independent geometry.** Run DeepLSD, cluster long coherent lines by direction, and compare resulting vanishing directions with the predicted horizon/rotation. On structured scenes, run CTRL-C as an independent proposal rather than averaging outputs blindly.
5. **Accept, revise, or stop.** Accept only if visible parallel edge families, horizon, and known verticals agree within the image tolerance chosen for the edit. If the evidence conflicts, inspect lens distortion, crop history, non-planar “reference” edges, and line selection before changing models.
6. **Build the support plane.** Define a plane-local coordinate system from three or more visible anchors, then derive a plane-to-image homography. A render uses the camera projection; a 2D warp uses the same plane homography. Keep physical object dimensions in the plane coordinate system rather than tuning an image-space scale by eye.
7. **Place and validate.** Project a box, footprint, or wireframe before rendering pixels. Check contact point, height, vertical direction, occlusion order, and a cast-shadow direction against the source. Only then pass the placed asset to alpha compositing, matting, relighting, or generative harmonisation.

For a plane `Z = 0` in world coordinates, a projective placement is:

```text
p ~ K [r1 r2 t] [X Y 1]^T
H_plane = K [r1 r2 t]
```

`~` means equality up to scale. The equation is valid only for points on the declared plane. It must not be used to “rotate” a volumetric object into a new view.

## Practical Configuration Contract

This is application-level configuration, not a command line accepted by the upstream projects. It makes every decision and later review explicit.

```yaml
source:
  image: scene.png
  raster_size_px: [4032, 3024]
  image_transform: identity          # crop/resize/rectification chain; never implicit
camera:
  estimator: geocalib
  camera_model: pinhole              # use simple_radial only after visible-distortion review
  principal_point: image_center_assumed
  save: camera.json                  # K, orientation, gravity, covariance, source hash
evidence:
  lines:
    detector: deeplsd
    minimum_length_px: 160
    use_for: [horizon_check, vanishing_direction_check]
  independent_estimate:
    estimator: ctrl-c
    required_for: high_value_structured_scene
acceptance:
  horizon_residual_px_max: 12        # edit-specific; compare at final raster size
  vertical_edge_angle_error_deg_max: 2
  require_two_consistent_edge_families: true
placement:
  support_plane: floor
  anchors_px: [[491, 2210], [2108, 2160], [2999, 1894]]
  object_size_m: [0.42, 0.18, 0.12]
  export: [placement.json, validation-overlay.png]
```

The thresholds are review gates, not universal accuracy claims. Tighten them for a prominent architectural edge; loosen them only with a written reason for low-salience imagery. Store an overlay with horizon, fitted vanishing directions, anchors, object footprint, and reference verticals so an operator can reject an implausible result without interpreting raw matrices.

## Validation Logic

Use independent observations instead of one scalar “confidence”:

- **Horizon test:** projected horizon follows at least two long, parallel-in-world edge families when those are visible.
- **Vertical test:** world-up projects in the same direction as trustworthy verticals; exclude leaning objects and handheld-camera roll unless their pose is intentional.
- **Footprint test:** all contact points lie on the declared plane and scale changes monotonically with depth.
- **Occlusion test:** a foreground scene boundary masks the object before colour, shadow, or texture synthesis begins.
- **Relighting test:** the contact shadow originates at the footprint and follows a source-consistent direction. Lighting agreement is separate from camera calibration.

When a projective estimate is slightly wrong, re-fit against explicit landmarks with the camera model held fixed. When the residual has a systematic curve, revisit distortion or source preprocessing; do not compensate by moving only the object.

## Gotchas

- **Crop invalidates intrinsics:** `K` belongs to a particular pixel coordinate system. A crop changes the principal point; a resize scales focal lengths and principal point. **Fix:** retain the image-transform chain and update all calibration artifacts together.
- **False parallel lines:** shelf edges, rooflines, and pavement seams can be non-parallel in 3D or curve under lens distortion. **Fix:** use multiple long edge families and reject clusters that disagree with known scene structure.
- **Principal point assumption:** GeoCalib’s documented centered-principal-point assumption can bias an off-axis crop. **Fix:** use the uncropped frame when available, manually constrain geometry, or flag the output as a proposal rather than a final camera.
- **Depth is not a ruler by default:** a monocular depth map can provide useful ordering and normals without fixing absolute object scale. **Fix:** anchor scale to a known scene dimension or a calibrated plane.
- **A good matte cannot fix parallax:** clean alpha edges, inpainting, or harmonisation cannot make a side view appear from a front-view asset. **Fix:** acquire a compatible view or use a 3D asset and render with the fitted camera.
- **Terms can diverge:** repository code terms do not automatically license checkpoints, training data, or a bundled backbone. **Fix:** record every downloaded artifact, revision, and license/model-card URL in the release manifest.

## Limitations

Single-image calibration is under-constrained. Repeated patterns, limited field of view, low resolution, rolling shutter, severe blur, reflections, and scenes without reliable straight lines can yield several plausible cameras. Learned estimates can be useful proposals but do not establish ground truth. Neither a homography nor depth/normals recovers hidden surfaces, object-specific material response, or a physically correct light source.

This pipeline also deliberately separates geometry from finishing. Use [[intrinsic-decomposition]] for illumination/albedo reasoning, [[color-checker-and-white-balance]] for colour measurement, [[videomama-diffusion-based-video-matting]] for alpha refinement, and [[spatialedit-16b-geometric-control-for-diffusion-based-image-editing]] when an image-editing model is considered after the geometric placement is fixed.

## Primary Sources

- [GeoCalib repository and inference API](https://github.com/cvg/GeoCalib), [Apache-2.0 license](https://github.com/cvg/GeoCalib/blob/main/LICENSE), and [v1.0 checkpoint release](https://github.com/cvg/GeoCalib/releases/tag/v1.0).
- [DeepLSD repository](https://github.com/cvg/DeepLSD) and [MIT license](https://github.com/cvg/DeepLSD/blob/main/LICENSE).
- [CTRL-C repository](https://github.com/jwlee-vcl/CTRL-C) and [Apache-2.0 license](https://github.com/jwlee-vcl/CTRL-C/blob/main/LICENSE).
- [MoGe repository](https://github.com/microsoft/MoGe), [code license](https://github.com/microsoft/MoGe/blob/main/LICENSE), and [MoGe-2 ViT-L normal model card](https://huggingface.co/Ruicheng/moge-2-vitl-normal).
