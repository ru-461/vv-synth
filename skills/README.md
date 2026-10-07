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
```

Preview the published skill: `gh skill preview ru-461/vv-synth vv-synth`.

Update or pin:

```shell
gh skill update vv-synth
gh skill install ru-461/vv-synth vv-synth --scope user --pin v0.1.2
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
gh skill publish --tag v0.1.2
```

This creates a GitHub Release with the `agent-skills` topic, using the same `v<version>` tag as the CLI (`version` in `pyproject.toml`). For a new release, bump `version` in `pyproject.toml` and `metadata.version` in both skills' `SKILL.md` files to the same value, publish with the matching tag, and tell users to run `gh skill update`. The same version is also uploaded to PyPI; the full steps are in [README.md](../README.md#release).

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
2. Install the CLI from PyPI with `uv tool install vv-synth` (or run it without installing via `uvx vv-synth`), or with Homebrew via `brew install ru-461/tap/vv-synth`. From a local clone, `uv tool install --editable .` also works. See README.

This skill does not include VOICEVOX Engine, voice libraries, models, official binaries, or generated WAV files. When using or distributing generated audio, follow the latest VOICEVOX terms, speaker-specific terms, and credit requirements.
