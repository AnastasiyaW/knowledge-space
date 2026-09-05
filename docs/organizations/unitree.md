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

Unitree builds humanoid and quadruped robots for robotics development and hardware integration.

- Physical hardware: G1 humanoid, quadruped robots, and robotic arms.
- Simulation and control: SDK2/DDS, ROS, and MuJoCo simulation.
- Training: telepresence kits and policy training environments.

G1 EDU provides 23–43 degrees of freedom, about 2 hours of runtime, and secondary development; the base G1 has 23 degrees of freedom. We use it as a platform for engineering integration and testing on real hardware, not as a finished universal autonomous worker.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-04-12 — A published Unitree video could not be reliably attributed to a specific model, version, or release: available viewing returned no metadata, so we cannot expand this fact.
- 2026-06-01 — Unitree announced H2 Plus as the reference humanoid robot for NVIDIA Isaac GR00T in academic research; this is a separate, later event, not an elaboration of the April video.
- 2026-09-05 — The current G1 page lists a starting price from $13,500, while a historical 2024 company news post listed a price from $16,000.

## How to use this

As of 2026-04-12, make no practice change from this line until the linked video is researched and its event facts are verified.

1. Select a specific model and configuration; for G1 development, use the EDU variant, because the standard G1 lists no secondary development.
  — <https://www.unitree.com/g1/>
2. Connect the robot to the network using the official instructions, install the SDK2 Python interface and Cyclone DDS dependencies, then start with status and control examples.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
3. Port the controller to the Unitree MuJoCo simulator before running on the robot; for G1, use unitree_hg messages rather than unitree_go.
  — <https://github.com/unitreerobotics/unitree_mujoco>
4. Use the published Unitree imitation learning stack to train and deploy policies: it covers data collection, algorithm development, training, and testing on G1.
  — <https://www.unitree.com/mobile/opensource/>

## Best practices

- Start with the official SDK2 examples, and check the network interface name before sending commands to the robot.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
- Test control in MuJoCo first; for G1, explicitly select the unitree_hg message type.
  — <https://github.com/unitreerobotics/unitree_mujoco>
- Do not mix low-level and high-level control modes without checking state: open reports on the official SDK show RPC errors and conflicts after low-level examples.
  — <https://github.com/unitreerobotics/unitree_sdk2_python/issues/39>

## Superseded by this

- 2024-07-05 — The historical Unitree notice of "G1 from $16,000" is obsolete as a price benchmark: the current G1 page lists pricing from $13,500.

## Still unknown

- The 2026-04-12 video returned no verifiable title, author, publication date, or description when querying YouTube; the specific model and event meaning remain unknown.
- Unitree has several independent product lines; without metadata, we cannot assign the April video to G1, H2, H1, R1, or a quadruped robot.
- The current starting price from $13,500 applies to the G1 page and does not confirm pricing for a specific configuration, region, delivery, or taxes.

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
