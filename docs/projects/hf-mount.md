---
title: hf-mount
category: projects
date: 2026-03-25
tags: [hf-mount, hf-mount-development, hf_mount, project]
aliases: ["hf-mount"]
---

# hf-mount

**Development line:** `project:hf-mount` · thread `hf-mount-development`  
**Last event:** 2026-03-25 · 1 dated since 2026-03-25 · **Researched:** 2026-09-05 · confidence: medium

## What it is

hf-mount is a Rust CLI for developers and ML infrastructure.

- Hugging Face Buckets: mounts with write support over NFS or FUSE.
- Model and dataset repositories: mounts read-only with data loaded on first access.

Remote changes have eventual consistency, usually up to 10 seconds in FUSE and up to 30 seconds in NFS. Repositories stay read-only. It fits read-heavy ML workloads and tight disks, but not multi-writer setups, cross-machine locks, or latency-sensitive random I/O.

## Development line

- **2026-03-25 — Hugging Face's hf-mount repository was publicly referenced.** On 2026-03-25, this development line recorded a link to Hugging Face's hf-mount GitHub repository. From the dated link alone, it can establish only that the project was publicly referenced on that date; no release, feature, or usage claim is supported.

## What changed

2026-03-25 — hf-mount became available to mount Hub Storage Buckets, models, and datasets into a local path. Buckets support writing; repositories are read-only.

Update to the 2026-03-25 entry: the official announcement from 2026-03-24 clarifies scale: we can attach remote storage up to 100 times larger than the local disk. This is clarification of the original launch, not a new release on 25 March.

- 2026-06-10 — v0.7.0 added JSON log formatting and FUSE/NFS shutdown fixes that prevent hung pods.
- 2026-07-08 — v0.9.0 capped remote chunk-read time and cut CAS read timeout to 30 seconds; FUSE link() became server-side copy.
- 2026-08-14 — v0.9.2 fixed phantom directories on raw-prefix tree matches, URL-encoding of paths, and added object_store writer support.

## How to use this

As of 2026-03-25, practitioners can use the hf-mount GitHub repository as the starting point for evaluating the project, while verifying its capabilities and maturity from primary documentation.

1. Install via Homebrew on macOS/Linux, or download the binary for Linux x86_64/aarch64 or macOS Apple Silicon.
  — <https://github.com/huggingface/hf-mount>
2. Mount a public model or dataset as a read-only path: `hf-mount start repo openai-community/gpt2 /tmp/gpt2`; pass `HF_TOKEN` or `--hf-token` for a private resource.
  — <https://huggingface.co/docs/hub/main/models-downloading>
3. Mount a Bucket for mutable checkpoints, logs, and artifacts: `hf-mount start --hf-token $HF_TOKEN bucket username/my-bucket /mnt/data`.
  — <https://huggingface.co/docs/hub/storage-buckets-access>
4. Check and stop the mount with `hf-mount status` and `hf-mount stop <mount-path>`; logs live in `~/.hf-mount/logs/`.
  — <https://github.com/huggingface/hf-mount>

## Best practices

- Choose NFS by default: it requires no root, kernel extension, or system FUSE dependencies; choose FUSE when closer kernel cache and metadata integration matter.
  — <https://github.com/huggingface/hf-mount>
- Do not use the mount as a distributed filesystem: it lacks cross-client locks and concurrent write conflict detection, and views can stay stale until the polling interval ends.
  — <https://github.com/huggingface/hf-mount>
- Enable `--advanced-writes` for interactive editing: streaming mode blocks editor unlink-and-create saves and loses buffers on crashes before close().
  — <https://github.com/huggingface/hf-mount>
- Prefer managed volume mounts on HF Jobs and Spaces unless you need a standalone mount on the host.
  — <https://huggingface.co/docs/hub/storage-buckets-access>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact tag or commit matching hf-mount on 2026-03-25 is unconfirmed by primary pages. The official announcement is dated 2026-03-24, so we treat it as clarification for the 2026-03-25 event rather than a separate event.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/huggingface/hf-mount | GitHub - huggingface/hf-mount | 2026-09-05 |
| https://huggingface.co/changelog/hf-mount | Introducing hf-mount | 2026-09-05 |
| https://huggingface.co/docs/hub/main/models-downloading | Downloading models | 2026-09-05 |
| https://huggingface.co/docs/hub/storage-buckets-access | Access Patterns | 2026-09-05 |
| https://github.com/huggingface/hf-mount/releases | Releases · huggingface/hf-mount | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:hf-mount`, thread `hf-mount-development`, 1 dated events 2026-03-25 → 2026-03-25.
- **Practical note:** As of 2026-03-25, practitioners can use the hf-mount GitHub repository as the starting point for evaluating the project, while verifying its capabilities and maturity from primary documentation.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
