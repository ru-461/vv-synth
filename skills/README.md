# Agent Skills (vv-synth)

These skills use the [Agent Skills](https://agentskills.io/specification) format. Install them with GitHub CLI [`gh skill`](https://cli.github.com/manual/gh_skill) (recommended) or [`npx skills`](https://github.com/vercel-labs/skills) for **Cursor, Claude Code, Codex, GitHub Copilot**, and similar agents.

## Skill List

| Directory | Name | Purpose |
|-----------|------|---------|
| [`vv-synth/`](vv-synth/) | `vv-synth` | TTS through the `vv-synth` CLI in **any project** |
| [`vv-synth-dev/`](vv-synth-dev/) | `vv-synth-dev` | Development and smoke testing for **this repository** |

The canonical files are `skills/*/SKILL.md`. Install them via `gh skill install` (recommended) — no manual copy needed.

## Global Install (Recommended)

Requires GitHub CLI **v2.90+**. Install from the `ru-461/vv-synth` repository on GitHub:

```shell
# Shared across multiple agents, such as ~/.agents/skills
gh skill install ru-461/vv-synth vv-synth --scope user --agent universal

# Examples for specific agents
gh skill install ru-461/vv-synth vv-synth --scope user --agent cursor
gh skill install ru-461/vv-synth vv-synth --scope user --agent claude-code
gh skill install ru-461/vv-synth vv-synth --scope user --agent codex
gh skill install ru-461/vv-synth vv-synth --scope user --agent github-copilot

# Optional skill for developing this repository
gh skill install ru-461/vv-synth vv-synth-dev --scope user --agent cursor
```

From a local clone:

```shell
gh skill install /path/to/vv-synth vv-synth --from-local --scope user --agent universal
gh skill preview /path/to/vv-synth vv-synth --from-local
```

Update or pin:

```shell
gh skill update vv-synth
gh skill install ru-461/vv-synth vv-synth@v1.0.0 --scope user --pin v1.0.0
```

### Alternative: `npx skills`

[`npx skills`](https://github.com/vercel-labs/skills) (Vercel Labs) installs the same skill without a GitHub CLI extension. `--global` targets your user directory:

```shell
# All detected agents, user-wide
npx skills@latest add ru-461/vv-synth --skill vv-synth --global

# One agent
npx skills@latest add ru-461/vv-synth --skill vv-synth --global --agent claude-code

# From a local clone
npx skills@latest add /path/to/vv-synth --skill vv-synth --global

# Update later
npx skills update vv-synth
```

## Project Scope

To use the skill only in one repository:

```shell
cd /path/to/your-app
gh skill install ru-461/vv-synth vv-synth --scope project --agent cursor

# Or with npx skills (omit --global for project scope)
npx skills@latest add ru-461/vv-synth --skill vv-synth --agent cursor
```

## Publishing (Maintainers)

```shell
cd /path/to/vv-synth
gh skill publish --dry-run
gh skill publish --tag v1.0.0
```

This creates a GitHub Release with the `agent-skills` topic. When skill content changes, bump the tag and tell users to run `gh skill update`.

## Directory Layout

```text
skills/
|-- README.md           # this file
|-- vv-synth/
|   |-- SKILL.md        # portable TTS distributed with gh
|   `-- references/
|       `-- REFERENCE.md
`-- vv-synth-dev/
    `-- SKILL.md        # development skill for this repository
```

## Agent-Specific Install Locations (`--scope user` Examples)

`gh skill install` copies files for each host. Manual edits are usually unnecessary.

| Agent | Typical path |
|-------|--------------|
| universal / shared | `~/.agents/skills/vv-synth/` |
| Cursor | `~/.cursor/skills/vv-synth/` |
| Claude Code | `~/.claude/skills/vv-synth/` |
| Codex | Codex settings skills directory |
| GitHub Copilot | `~/.copilot/skills/vv-synth/` |

## Prerequisites for CLI Users

1. Start VOICEVOX Engine (CPU / GPU) with Docker or an official binary. See `skills/vv-synth/SKILL.md`.
2. Add `vv-synth` to PATH with `uv tool install --editable .`. See README.

This skill does not include VOICEVOX Engine, voice libraries, models, official binaries, or generated WAV files. When using or distributing generated audio, follow the latest VOICEVOX terms, speaker-specific terms, and credit requirements.
