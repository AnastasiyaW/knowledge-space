---
title: Unitree
category: organizations

tags: [organization, unitree, unitree-development]
aliases: ["Unitree"]
---

# Unitree

**Development line:** `organization:unitree` · thread `unitree-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

Unitree builds hardware and software for hands-on work with the G1 humanoid, quadruped robots, and robotic arms.

- Physical robots: humanoid and quadruped platforms for field testing.
- SDK2 and DDS: programmatic communication and robot control.
- ROS and MuJoCo: simulation environments for controllers.
- Teleoperation and policy kits: tools for data collection and policy training.

G1 EDU offers 23–43 degrees of freedom, about 2 hours of runtime, and secondary development; base G1 has 23 degrees of freedom.
This is a platform for engineering integration and testing on real hardware, not a ready-made general-purpose autonomous worker.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-04-12 — A published Unitree video could not be reliably attributed to a specific model, version, or release. The available viewing returned no metadata, so we cannot expand this fact.
- 2026-06-01 — Unitree announced H2 Plus as the reference humanoid robot for NVIDIA Isaac GR00T academic research. This is a separate, later event, not a clarification of the April video.
- 2026-09-05 — The current G1 page lists a starting price from $13,500. The historical 2024 news post listed a price from $16,000.

## How to use this

As of 2026-04-12, make no practice change from this line until the linked video is researched and its event facts are verified.

1. Choose the specific model and package. G1 development requires the EDU variant because base G1 does not support secondary development.
  — <https://www.unitree.com/g1/>
2. Connect the robot to the network following official instructions. Install the Python SDK2 interface and Cyclone DDS dependencies, then start with status and control examples.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
3. Test the controller in the Unitree MuJoCo simulator before deploying to hardware. Use unitree_hg messages for G1, not unitree_go.
  — <https://github.com/unitreerobotics/unitree_mujoco>
4. Use the published Unitree imitation learning stack to train and deploy policies. It covers data collection, algorithm development, training, and verification on G1.
  — <https://www.unitree.com/mobile/opensource/>

## Best practices

- Start with official SDK2 examples and verify the network interface name before sending commands to the robot.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
- Run control loops in MuJoCo first. Select unitree_hg messages explicitly for G1.
  — <https://github.com/unitreerobotics/unitree_mujoco>
- Do not mix low-level and high-level control modes without checking state. Open SDK reports confirm RPC errors and conflicts after running low-level examples.
  — <https://github.com/unitreerobotics/unitree_sdk2_python/issues/39>

## Superseded by this

- 2024-07-05 — The historical Unitree figure of G1 from $16,000 is obsolete as a price benchmark. The current G1 page lists pricing from $13,500.

## Still unknown

- The 2026-04-12 video returned no verifiable title, author, publish date, or description from YouTube. The specific model and meaning of the event remain unknown.
- Unitree maintains multiple product lines. Without metadata, we cannot assign the April video to G1, H2, H1, R1, or a quadruped robot.
- The current price from $13,500 applies to the G1 page. It does not confirm the price for a specific configuration, region, shipping, or taxes.

## Sources

| source | title | read |
|---|---|---|
| https://www.youtube.com/watch?v=zoMDadPQLKA | YouTube video zoMDadPQLKA | 2026-09-05 |
| https://www.unitree.com/g1/ | Unitree G1 | 2026-09-05 |
| https://www.unitree.com/news/ | Unitree News Center | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_sdk2_python | unitree_sdk2_python | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_mujoco | unitree_mujoco | 2026-09-05 |
| https://www.unitree.com/mobile/opensource/ | Official Open Source | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_sdk2_python/issues/39 | Can't run g1 high_level example after running low_level examples | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `organization:unitree`, thread `unitree-development`, 0 dated events - → -.
- **Practical note:** As of 2026-04-12, make no practice change from this line until the linked video is researched and its event facts are verified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
