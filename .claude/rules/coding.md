---
paths:
  - "**/*.py"
---

# Coding rules

- Python **3.14** (`requires-python = ">=3.14"`).
- Keep `vv-synth --help` text in **English**. Japanese user prose belongs in `README.ja.md`.
- Synthesis errors must be a **single English line** on stderr with exit code 1
  (`typer.echo(..., err=True)`). Do not expose tracebacks (`logger.exception`) to users.
- Print `INFO: wrote <absolute-path>` to stdout on success. Argument and option parsing
  errors use Typer's usage error on stderr with exit code 2.
- CLI speech rates must be finite numbers from `0.01` to `10.0`.
- Keep business logic in `vv_synth/`; `main.py` stays CLI-only. See `architecture.md`.
- Absolute imports only — relative imports are banned (`ban-relative-imports = "all"`).
- Do **not** document `Raises: typer.Exit` in `--help` docstrings (`main.py` ignores `DOC501`
  for this reason).

## Checks after Python changes

```shell
uv run ruff check .
uv run ruff format .
uv run ty check
```

`ruff` (`select = ["ALL"]`) and `ty` run in strict mode; both are configured in
`pyproject.toml`. See `workflow.md` for pytest and smoke testing.
