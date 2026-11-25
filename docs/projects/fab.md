---
title: "Fab: fab-human-motion-reconstruction — Fab Human Motion Reconstruction"
category: "projects"
date: 2026-11-20
tags: ["fab", "fab-human-motion-reconstruction", "project"]
aliases: ["Fab: fab-human-motion-reconstruction"]
---

# Fab: fab-human-motion-reconstruction — Fab Human Motion Reconstruction

FAB is a ViT-L student distilled from SAM 3D Body for real-time 3D human mesh recovery from monocular video.

**Development line:** project:fab · thread fab-human-motion-reconstruction  
**Last event:** 2026-11-20 · 2 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

FAB is a vision transformer student model distilled from SAM 3D Body. It recovers 3D human meshes from monocular video in real time, and it is aimed at visual teleoperation and interactive motion capture.

It outputs:

- camera-space 3D skeletons
- dense surface point clouds
- contact states for heels, toes, hands and knees

The motion retargets directly to humanoid robots such as the Unitree G1. The pipeline runs at thirty-nine frames per second on an RTX 4070 Ti SUPER GPU, person detection included. The ViT-L student replaces SAM 3D Body inference that took several seconds.

## Development line

- **2026-11-20 — FAB: fast human body reconstruction model released.** FAB is a human body reconstruction model distilled from SAM 3D Body into a ViT-L student. It reports 39.2 FPS on an RTX 4070 Ti SUPER with person detection included. It also reports better camera-space accuracy than SAM 3D Body on most benchmarks, and contact prediction for heels, toes, hands and knees. Its Unitree G1 motion retargeting is reported as better than several listed methods. Code and weights are linked on GitHub and Hugging Face.
- **2026-11-20 — FAB human body reconstruction model released.** FAB is a fast human body reconstruction model for video. It outputs dense 2D and 3D points and a skeleton. The ViT-L student is distilled from SAM 3D Body and runs at a reported 39.2 FPS on an RTX 4070 Ti SUPER. Code and weights are on GitHub and Hugging Face.
- **2026-11-20 — other reporting on this date.**
  - The project release describes the ViT-L student distilled from SAM 3D Body. It reports 39.2 FPS on an RTX 4070 Ti SUPER with detection latency included, better camera-space precision on standard benchmarks, and contact predictions for heels, toes, hands and knees for Unitree G1 retargeting. (2026-11-20) — <https://www.jinkuncao.com/FAB/>
  - The release includes open code and model checkpoints. They cover dense 2D and 3D surface points and 3D skeletal tracking directly from monocular video. (2026-11-20) — <https://www.jinkuncao.com/FAB/>

## What changed

Human mesh recovery was built on heavy promptable models. It is now moving to low-latency student models for real-time robot teleoperation and motion capture. Distilling SAM 3D Body into a ViT-L student kept camera-space accuracy and gave frame rates fit for real-time control. Contact prediction now covers heels, toes, hands and knees, so retargeting to a robot shows fewer physical artifacts.

## How to use this

1. Clone the FAB project repository and set up the Python environment with PyTorch and its dependencies.
  — <https://www.jinkuncao.com/FAB/>
2. Download the pre-trained ViT-L student weights from the model repository.
  — <https://www.jinkuncao.com/FAB/>
3. Run the video inference script. It extracts 3D joint skeletons, dense surface point clouds and joint contact states from monocular video.
  — <https://www.jinkuncao.com/FAB/>
4. Map the predicted joint poses and contact signals to humanoid control targets, such as the Unitree G1 robot.
  — <https://www.jinkuncao.com/FAB/>

## Best practices

- Run on a fast GPU such as an RTX 4070 Ti SUPER, so reconstruction stays above thirty-nine frames per second with detection included.
  — <https://www.jinkuncao.com/FAB/>
- Use the predicted contact states at heels, toes, hands and knees as physical constraints. That reduces foot sliding and floor penetration during robot retargeting.
  — <https://www.jinkuncao.com/FAB/>

## Superseded by this

- The belief that accurate camera-space human mesh recovery and dense point estimation need offline models with multi-second inference, such as unoptimized SAM 3D Body.
  — <https://www.jinkuncao.com/FAB/>

## Still unknown

- Repository commit hashes and the exact Hugging Face repository identifiers could not be resolved from search results, because the links redirect. Community deployment benchmarks from forums are not indexed.

## Sources

| source | title | read |
|---|---|---|
| https://www.jinkuncao.com/FAB/ | FAB: Fast and Accurate Body Estimation | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:fab, thread fab-human-motion-reconstruction, 2 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
