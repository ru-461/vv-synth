# vv-synth — Claude Code

Claude Code reads this file. The shared agent guide is imported from [`AGENTS.md`](AGENTS.md)
below; Claude-specific notes follow.

@AGENTS.md

## Claude Code notes

- Claude Code auto-loads [`.claude/rules/`](.claude/rules/) natively: `commit.md`, `security.md`,
  and `terms.md` every session, and the path-scoped `coding.md` / `architecture.md` /
  `workflow.md` / `docs.md` when you edit files they target (`paths:` frontmatter).
- `README.md` is the source of truth for implementation detail and the two Mermaid diagrams.
- Commit only when the user explicitly asks ([`.claude/rules/commit.md`](.claude/rules/commit.md)).
