---
title: DiffGI
category: projects

tags: [diffgi, diffgi-development, project]
aliases: ["DiffGI"]
---

# DiffGI

**Development line:** `project:diffgi` · thread `diffgi-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-06 · confidence: medium

## What it is

DiffGI — исследовательский метод image-to-3D для одежды и каркасной мебели с тонкими, открытыми поверхностями. — заменяет бинарную occupancy-карту непрерывным 2D TSDF; — восстанавливает mesh через дифференцируемый Marching Squares и использует DiffGI-VAE с latent diffusion; — авторы сообщают 1,21 с и 3,22 ГБ VRAM на RTX 4070 12 ГБ либо 8,52 с на CPU MacBook M4. Вердикт: сегодня это статья и проектная страница для исследования или собственной реализации, а не выпущенный inference-инструмент.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-15: DiffGI вышел как arXiv v1 — метод с непрерывным 2D TSDF, Differentiable Marching Squares, DiffGI-VAE и transformer-based latent diffusion. 2026-08-06: проектная страница относилась к уже опубликованной v1; отдельного paper revision, model release или runnable-code release на эту дату не подтверждено.

## How to use this

1. DiffGI сегодня используйте как технический ориентир для собственной реализации, если нужны тонкие незамкнутые поверхности, а не готовая модель для скачивания и запуска.
  — <https://arxiv.org/abs/2607.13365>
2. Перед планированием локального inference проверьте официальный исходник демо: URL моделей оставлены заглушками, а pipeline не подключён, поэтому команды установки или воспроизводимый запуск отсутствуют.
  — <https://github.com/EJShim/diffgi/blob/main/docs/demo/index.html>

## Best practices

- DiffGI: сохраняйте 1,21 с и 3,22 ГБ как авторский benchmark для RTX 4070 12 ГБ, а не как обещание производительности или аппаратное требование для другого workflow.
  — <https://ejshim.github.io/diffgi/>
- DiffGI: не планируйте интеграцию как готового open-source пакета — официальный репозиторий описан как статическая project page, а опубликованный демо-код не выполняет inference.
  — <https://github.com/EJShim/diffgi>
- DiffGI: перед применением в production отдельно проверяйте topology, UV charts и пригодность mesh для downstream simulation; результаты статьи не заменяют собственную валидацию ассета.
  — <https://arxiv.org/abs/2607.13365>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No official checkpoint, implementation package, model card, license, installation guide or reproducible workflow was available in the reviewed official sources.
- No independently dated primary artifact for 2026-08-06 documents a distinct paper revision, code release or model release.
- The reported quality, latency and memory figures are author-published results; no independent reproduction or production simulation validation was found.
- A focused Chinese-language search found no first-party Chinese release note, documentation or tutorial for DiffGI.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2607.13365 | DiffGI: Differentiable Geometry Images for High-Fidelity Thin-Shell 3D Generation — arXiv 2607.13365 | 2026-09-07 |
| https://ejshim.github.io/diffgi/ | DiffGI: Differentiable Geometry Images for High-Fidelity Thin-Shell 3D Generation | 2026-09-07 |
| https://github.com/EJShim/diffgi | EJShim/diffgi — DiffGI project-page repository | 2026-09-07 |
| https://github.com/EJShim/diffgi/blob/main/docs/demo/index.html | DiffGI WebGPU demo source | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:diffgi`, thread `diffgi-development`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
