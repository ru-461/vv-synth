---
paths:
  - "**/*.py"
  - "pyproject.toml"
---

# Development workflow

## Setup

```shell
uv sync --group dev
uv run vv-synth --help
```

## Required checks (after any Python change)

```shell
uv run ruff check .
uv run ruff format .
uv run ty check
uv run pytest
```

`pytest` runs the suite in `tests/`. Tests mock the Engine via `urllib`, so they pass
without a running VOICEVOX Engine.

## Prepare the Engine (Docker or binary)

`vv-synth` needs an HTTP Engine on `http://127.0.0.1:50021`. The GUI app is not required.

```shell
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
curl -sSf http://127.0.0.1:50021/version
```

If Docker is not used, run an official binary from VOICEVOX Engine Releases. Full setup
(CPU, Windows GPU, binaries, troubleshooting) lives in
[README.md](../../README.md#prepare-voicevox-engine).

## Smoke test (Engine running)

```shell
uv run vv-synth "smoke test"
ls -la output/
```

## Adding a CLI option

1. Edit `main.py` (CLI only); put logic in `vv_synth/`.
2. Run the required checks above.
3. Smoke test against a running Engine.
4. Update the README Usage option table and `vv-synth --help` wording. See `docs.md`.

## Global install

```shell
uv tool install --editable .   # installs both `vv-synth` and the alias `vvs`
```
