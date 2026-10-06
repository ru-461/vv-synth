# vv-synth — Agent Guide

`vv-synth` is a thin Typer CLI for VOICEVOX Engine: it sends text to a separately prepared
Engine over HTTP (default `http://127.0.0.1:50021`) and writes a WAV file. Package: `vv-synth`
(published on [PyPI](https://pypi.org/project/vv-synth/)); library: `vv_synth/`; entry point:
`main:main`. Keep changes small and the CLI thin.

This repository is open source (MIT). Do **not** vendor VOICEVOX Engine, voice libraries,
model files, binaries, Docker images, or generated WAV files (see
[`.claude/rules/terms.md`](.claude/rules/terms.md)).

User-facing docs: [`README.md`](README.md) (English; source of truth for the Mermaid diagrams
and maintenance) and [`README.ja.md`](README.ja.md) (Japanese).

## Recommended agents

Development is set up for **Codex CLI** and **Claude Code**. This `AGENTS.md` is the shared
entry both read: Codex auto-loads it, and Claude Code reads it via [`CLAUDE.md`](CLAUDE.md).
Claude Code additionally auto-loads `.claude/rules/*.md` natively — the always-on rules
(`commit`, `security`, `terms`) every session, and the path-scoped rules when you edit matching
files; Codex and other agents read them on demand from the index below.

## Rules index

Detailed rules live in [`.claude/rules/`](.claude/rules/). Read the one that matches your change:

| File | Contents |
|------|----------|
| [`commit.md`](.claude/rules/commit.md) | Commit message format and prefixes |
| [`coding.md`](.claude/rules/coding.md) | Python 3.14, ruff/ty, English `--help`, one-line errors |
| [`architecture.md`](.claude/rules/architecture.md) | Module responsibilities and synthesis flow |
| [`workflow.md`](.claude/rules/workflow.md) | uv, quality checks, Engine setup, smoke test |
| [`docs.md`](.claude/rules/docs.md) | README/Mermaid/skills sync, MD placement |
| [`terms.md`](.claude/rules/terms.md) | VOICEVOX terms, no-vendoring, credit |
| [`security.md`](.claude/rules/security.md) | Secret files and hardcoding |

## Quick reference

```shell
uv sync --group dev
uv run ruff check . && uv run ruff format . && uv run ty check && uv run pytest
uv run vv-synth "Test"   # Engine must be running on :50021
```

Global CLI: `uv tool install --editable .` (users install from PyPI: `uv tool install vv-synth`).
Engine setup (Docker / Windows GPU / binary) is in
[README.md](README.md#prepare-voicevox-engine). Releases (GitHub Release + PyPI) follow
[README.md](README.md#release); publish only when the user explicitly asks.

## Skills

- [`skills/vv-synth/`](skills/vv-synth/) — portable TTS for other projects
- [`skills/vv-synth-dev/`](skills/vv-synth-dev/) — developing this repository
- [`skills/README.md`](skills/README.md) — install and publish

Commit only when the user explicitly asks ([`.claude/rules/commit.md`](.claude/rules/commit.md)).
