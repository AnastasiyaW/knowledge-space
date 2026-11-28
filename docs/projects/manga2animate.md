---
title: "Manga2Animate: manga2animate-release — Manga2Animate Release"
category: "projects"
date: 2026-10-21
tags: ["manga2animate", "manga2animate-release", "project"]
aliases: ["Manga2Animate: manga2animate-release"]
---

# Manga2Animate: manga2animate-release — Manga2Animate Release

**Development line:** project:manga2animate · thread manga2animate-release  
**Last event:** 2026-10-21 · 1 dated since 2026-10-21 · **Researched:** 2026-11-28 · confidence: high

## What it is

Manga2Animate is a multi-agent framework from National Yang Ming Chiao Tung University that turns a few manga pages and a character reference into an animation faithful to the source. It follows real animation production: it writes an animation script, draws a visual storyboard, and only then generates the video. A creator agent produces each step, and a paired reviewer agent checks it against the source manga panels.

## Development line

- **2026-10-21 — Manga2Animate agentic manga-to-animation pipeline released as open source.** Manga2Animate, an agentic pipeline that converts manga pages into animation via script, storyboard, and video stages with reviewer agents, was announced with open code on GitHub and published evaluation data, including a 37-person user study and pairwise storyboard comparison across 13 criteria.
  - The project page names the authors \(Sheng-Wei Zhang, Hsi-An Chen, Yan-Ting Liou, Chih-Hsuan Chen, Shih-Chen Tseng, Yu-Lun Liu\) at National Yang Ming Chiao Tung University. It describes two intermediate representations, an animation script and a visual storyboard, each made by a creator agent and reviewed against the source panels by a paired reviewer agent. It reports that 37 participants saw eight storyboard cases and eight video cases next to the input manga, with method names hidden and order randomized, and picked the best result per criterion. It also links an arXiv paper, code, a Hugging Face page and evaluation data. (undated) — <https://annchenn.github.io/Manga2Animate/>
  - The GitHub repository contains the pipeline in src/, agent prompts in prompts/, an opensource\_backends/ folder for open-model setup, and a mangaeval/ folder with storyboard metrics \(vistorybench\), video metrics \(vbench\) and aesthetic scores. The creators and reviewers call Gemini through Vertex AI, or through a plain API key if no GCP project is set. The pipeline uses 6 panels per case \(NUM\_CLIPS=6\), and the script and storyboard are refined over two rounds of feedback. The page showed 99 stars and 10 forks when observed. (undated) — <https://github.com/annchenn/Manga2Animate>

## What changed

The project page, code repository and evaluation data are now public. The authors argue that feeding manga pages straight into a video model misreads the panel layout and gets the story wrong, while working from text alone loses the characters and art style. Their approach grounds every stage in the source panels and refines the script and storyboard over two rounds of feedback.

## How to use this

1. Create the environment with conda \(python 3.12\) and run pip install -r requirements.txt.
  — <https://github.com/annchenn/Manga2Animate>
2. Set up Gemini access through Vertex AI \(gcloud auth application-default login\) or a plain GEMINI\_API\_KEY. Copy .env.example to .env and fill in credentials. Only the video models you use need a key: ARK\_API\_KEY for seedance, MINIMAX\_API\_KEY for minimax-api, DASHSCOPE\_API\_KEY for wan, plus IMGBB\_API\_KEY for image hosting with seedance or wan.
  — <https://github.com/annchenn/Manga2Animate>
3. Prepare each case as a folder target/\<case\>/ containing manga\_page.jpg \(or manga\_page1.jpg, manga\_page2.jpg... in reading order\) and a character reference sheet ref.png. Alternatively, put one image per character in a characters/ folder.
  — <https://github.com/annchenn/Manga2Animate>
4. Run the three stages in order. Stage 1 crops pages into panels in reading order \(python src/croppanels.py -t \<case\>\) and extracts the transcript. Stage 2 runs script and storyboard refinement \(src/run\_all.py\). Stage 3 generates the video \(src/create\_video.py\).
  — <https://github.com/annchenn/Manga2Animate>

## Best practices

- Work through the script and storyboard before generating video, and have a reviewer check each stage against the source panels. The project page shows that a candidate script can describe one panel precisely and misread the next, so the Script Reviewer picks the best parts clip by clip across three candidates.
  — <https://annchenn.github.io/Manga2Animate/>
- Provide a character reference image, since it is used to write identity-defining character descriptions that keep characters and style consistent. Use the per-character images option if one sheet does not cover all characters.
  — <https://github.com/annchenn/Manga2Animate>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact list of the 13 pairwise storyboard comparison criteria, and which are hard pass/fail, was not visible in the observed page text.
- The numeric results of the user study and ablations were cut off in the observed page text.
- The exact release date of the code and data is not stated on the pages; neither page carries a date.

## Sources

| source | title | read |
|---|---|---|
| https://annchenn.github.io/Manga2Animate/ | Manga2Animate: Reading Manga Before Animating It \(project page\) | 2026-10-21 |
| https://github.com/annchenn/Manga2Animate | GitHub - annchenn/Manga2Animate | 2026-10-21 |

## Agent brief {#agent-brief}

- **Subject:** project:manga2animate, thread manga2animate-release, 1 dated events 2026-10-21 → 2026-10-21.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
