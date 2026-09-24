# Contributing to vv-synth

Thanks for your interest in `vv-synth`. It is a thin Typer CLI that sends text to a
separately prepared VOICEVOX Engine over HTTP and writes a local WAV file. Please keep
changes small and focused.

## Scope and philosophy

- `vv-synth` only talks to the Engine HTTP API (`http://127.0.0.1:50021` by default).
- Do **not** vendor VOICEVOX Engine, voice libraries, model files, official binaries,
  Docker images, or generated WAV files. They must never be committed.
- Prefer editing existing modules over adding new abstractions. Avoid out-of-scope
  refactors and large test additions unless they are requested.

The runtime logic lives in three files:

| Path | Responsibility |
|------|----------------|
| `main.py` | Typer CLI and the `vv-synth` entry point |
| `vv_synth/engine_client.py` | Engine HTTP calls, speech rate, WAV saving |
| `vv_synth/output_paths.py` | Output path resolution (`output/`, `-o`, timestamps) |

## Development setup

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```shell
uv sync --group dev
uv run vv-synth --help
```

Start the VOICEVOX Engine with Docker or an official binary, then confirm it responds:

```shell
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
curl -sSf http://127.0.0.1:50021/version
```

See [README.md](README.md#prepare-voicevox-engine) for full Engine setup (CPU, Windows GPU,
official binaries) and troubleshooting.

## Quality checks

Run these before opening a pull request:

```shell
uv run ruff check .
uv run ruff format .
uv run ty check
uv run pytest
```

`pytest` runs the suite in `tests/` and does not require a running VOICEVOX Engine
(network calls are mocked).

Manual smoke test with the Engine running:

```shell
uv run vv-synth "contribution smoke test"
ls -la output/
```

## Coding conventions

- Strict `ruff` (`select = ["ALL"]`) and `ty` settings are defined in `pyproject.toml`.
- Relative imports are banned; use absolute imports.
- Keep `vv-synth --help` text in **English**. Japanese user-facing prose belongs in
  `README.ja.md`.
- Synthesis errors must be a **single English line** on stderr (exit code 1). Do not expose
  tracebacks to users.
- Keep business logic in `vv_synth/`; `main.py` stays CLI-only.

## Documentation sync

When module boundaries, Engine APIs, or the CLI flow change, update the two Mermaid diagrams
in `README.md` and keep these in sync as needed:

- `README.ja.md` (Japanese user docs)
- `AGENTS.md` and `CLAUDE.md` (agent guidance)
- Agent Skills: `skills/vv-synth/SKILL.md`, `skills/vv-synth-dev/SKILL.md`

The full checklist lives in [README.md](README.md#documentation-sync-checklist).

## Commit and pull request style

- Use a single-line English message: `prefix: message`.
- Prefixes: `feat`, `fix`, `docs`, `chore`, `update`, `refactor`, `test`, `style`.
- Examples: `feat: add --pitch option`, `docs: update engine setup`.
- Keep each pull request scoped to one logical change.
- Never commit `output/*.wav`, `voicevox_core/`, `download`, Engine binaries, models, voice
  libraries, or virtual environments.

## VOICEVOX terms

Generated audio is subject to the latest official VOICEVOX terms and each voice library /
speaker's own terms, including credit requirements. Before sharing or redistributing any
generated audio, confirm the applicable terms. See
[OSS Publication And VOICEVOX Terms](README.md#oss-publication-and-voicevox-terms).

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
