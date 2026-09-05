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

hf-mount is a Rust CLI for developers and ML infrastructure to mount Hugging Face storage to local filesystems.

- Hugging Face Buckets, mounted with write access over NFS or FUSE.
- Model and dataset repositories, mounted read-only with files loaded on first access.

Repositories remain read-only, and remote changes settle within 10 seconds under FUSE and 30 seconds under NFS. We run it for read-heavy ML tasks on constrained disks, but not for multi-user writes, cross-machine locking, or latency-sensitive random I/O.

## Development line

- **2026-03-25 — Hugging Face's hf-mount repository was publicly referenced.** On 2026-03-25, this development line recorded a link to Hugging Face's hf-mount GitHub repository. From the dated link alone, it can establish only that the project was publicly referenced on that date; no release, feature, or usage claim is supported.

## What changed

2026-03-25 — hf-mount became available to mount Hub models, datasets, and Storage Buckets to a local path; Buckets support writes, while repositories remain read-only.

An official announcement on 2026-03-24 clarifies the scale for the 2026-03-25 launch: users can connect remote storage claimed to reach up to 100 times local disk size; this is not a new release on 25 March, but clarification of the original launch.

New events:
- 2026-06-10 — v0.7.0 added JSON log formatting and FUSE/NFS shutdown fixes preventing pod hangs.
- 2026-07-08 — v0.9.0 capped remote chunk-read duration, cut CAS read timeout to 30 seconds, and turned FUSE link() into a server-side copy.
- 2026-08-14 — v0.9.2 fixed phantom directories during raw-prefix tree matches, path URL-encoding, and object_store writer support.

## How to use this

As of 2026-03-25, practitioners can use the hf-mount GitHub repository as the starting point for evaluating the project, while verifying its capabilities and maturity from primary documentation.

1. Install via Homebrew on macOS/Linux or download the binary for Linux x86_64/aarch64 or macOS Apple Silicon.
  — <https://github.com/huggingface/hf-mount>
2. Mount a public model or dataset as a read-only path: `hf-mount start repo openai-community/gpt2 /tmp/gpt2`; pass `HF_TOKEN` or `--hf-token` for a private resource.
  — <https://huggingface.co/docs/hub/main/models-downloading>
3. For mutable checkpoints, logs, and artifacts, mount a Bucket: `hf-mount start --hf-token $HF_TOKEN bucket username/my-bucket /mnt/data`.
  — <https://huggingface.co/docs/hub/storage-buckets-access>
4. Inspect and stop mounts with `hf-mount status` and `hf-mount stop <mount-path>`; logs live in `~/.hf-mount/logs/`.
  — <https://github.com/huggingface/hf-mount>

## Best practices

- Default to NFS: it requires no root, kernel extension, or system FUSE dependencies; choose FUSE when tighter integration with kernel cache and metadata matters.
  — <https://github.com/huggingface/hf-mount>
- Do not use the mount as a distributed filesystem: there are no cross-client locks, concurrent writes lack conflict detection, and stale views can persist up to the polling interval.
  — <https://github.com/huggingface/hf-mount>
- Enable `--advanced-writes` for interactive editing: streaming mode blocks typical editor unlink-and-create saves and drops the buffer on crash before `close()`.
  — <https://github.com/huggingface/hf-mount>
- Prefer managed volume mounts for HF Jobs and Spaces unless you need a standalone host mount.
  — <https://huggingface.co/docs/hub/storage-buckets-access>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact tag or commit matching the state of hf-mount on 2026-03-25 is unconfirmed by available primary pages. The official announcement is dated 2026-03-24, so it serves as a clarification source for the 2026-03-25 event rather than a separate event.

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
