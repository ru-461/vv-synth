---
paths:
  - "**/*.md"
---

# Documentation rules

## Source of truth

`README.md` is the source of truth for the two architecture diagrams and
maintenance procedures. `README.ja.md` is the Japanese mirror for user-facing content.

`README.md` is also the PyPI project description. Link repository files from it with absolute
GitHub URLs (`https://github.com/ru-461/vv-synth/blob/main/...`); relative links break on PyPI.

## Sync targets

When behavior or structure changes, keep these aligned:

| Change | Update |
|--------|--------|
| Module boundaries / Engine API / call order | Both README Mermaid diagrams |
| CLI flags | README Usage option table + `vv-synth --help` |
| User-facing behavior or Engine steps | `README.ja.md` |
| Agent rules / boundaries | `AGENTS.md`, `CLAUDE.md`, and the relevant `.claude/rules/*.md` |
| Output path rules | `vv_synth/output_paths.py`, README [Output Directory](../../README.md#output-directory), `README.ja.md` |
| CLI or Engine steps used by skills | `skills/vv-synth/SKILL.md`, `skills/vv-synth-dev/SKILL.md` |

## Mermaid

Update the README diagrams when modules are added/renamed/change responsibility, Engine
endpoints or call order change, or filesystem/external dependencies change. Keep the
Japanese README aligned. Use ` ```mermaid ` fences.

## MD file placement

- Root-level MD is limited to the existing fixed files: `README.md`, `README.ja.md`,
  `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`.
- Do not create new temporary/working MD files at the repository root.
- Agent rules live in `.claude/rules/*.md`; skill definitions in `skills/*/SKILL.md`.

The full pre-publish documentation checklist is in
[README.md](../../README.md#documentation-sync-checklist).
