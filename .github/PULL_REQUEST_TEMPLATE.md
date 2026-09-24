## Summary

<!-- What does this change and why? Keep the PR scoped to one logical change. -->

## Type of change

- [ ] `fix` — bug fix
- [ ] `feat` — new feature
- [ ] `docs` — documentation only
- [ ] `refactor` / `chore` / `style` / `test` — other

## Checklist

- [ ] `uv run ruff check .` passes
- [ ] `uv run ruff format .` applied
- [ ] `uv run ty check` passes
- [ ] `uv run pytest` passes
- [ ] Smoke tested with a running Engine (`uv run vv-synth "..."`), or N/A
- [ ] `vv-synth --help` text stays English
- [ ] Synthesis errors remain a single English line (no tracebacks)
- [ ] Docs synced as needed (README.md / README.ja.md / AGENTS.md / CLAUDE.md / Mermaid / Skills)
- [ ] No VOICEVOX Engine binaries, voice libraries, models, or `output/*.wav` are committed
