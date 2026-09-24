---
paths:
  - "vv_synth/**"
  - "main.py"
---

# Architecture rules

`vv-synth` is a thin Typer CLI that sends text to a separately prepared VOICEVOX Engine over
HTTP and writes a WAV file. Keep it thin.

## Module responsibilities

| Path | Responsibility |
|------|----------------|
| `main.py` | Typer CLI and the `vv-synth` entry point (`main:main`) — CLI only |
| `vv_synth/engine_client.py` | Engine HTTP calls, speech rate, WAV saving |
| `vv_synth/output_paths.py` | Output path resolution (`output/`, `-o`, timestamp names) |

## Current synthesis flow

1. `main.synth` calls `resolve_output_file()` to decide the save path.
2. `synthesize_text_to_file()` connects to the Engine.
3. `POST /audio_query` → `apply_speed_scale()` → `POST /synthesis` → `save_wav()`.

HTTP timeouts in `engine_client.py`: `/audio_query` 60s, `/synthesis` 120s.

## Design principles

- **vv_synth/ first**: implement shared logic in `vv_synth/`, call it from `main.py`.
- **main.py thin**: no business logic in the CLI layer.
- The Engine is external. Do not vendor it, voice libraries, models, or binaries
  (see `terms.md`).

## Diagrams

The canonical Mermaid diagrams (Component Layout, Synthesis Flow) live in `README.md`. When
module boundaries, Engine endpoints, or call order change, update both diagrams. See
`docs.md`.
