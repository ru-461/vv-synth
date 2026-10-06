# vv-synth skill reference

## Output path rules

| Invocation (cwd = target project) | Typical result |
|------------|----------------|
| (no `-o`) | `output/YYYYMMDD-HHMMSS.wav` (local time) |
| `-o hello.wav` | `output/hello.wav` |
| `-o path/to/a.wav` | `path/to/a.wav` |
| `--output-dir artifacts` | `artifacts/...` |
| `VV_SYNTH_OUTPUT_DIR=/abs/dir` (env) | `/abs/dir/...` (when `--output-dir` is not given) |

`output/` is auto-created on first run. Timestamps use the host's local timezone.
Implementation: `vv_synth/output_paths.py` in the vv-synth repository.

## Install / update this skill

`gh skill` is recommended; `npx skills` (Vercel Labs) is a supported alternative. Replace `ru-461` with the GitHub user or org that hosts the repository.

### `gh skill` (requires GitHub CLI v2.90+)

```shell
# All supported agents (~/.agents/skills or agent-specific dirs)
gh skill install ru-461/vv-synth vv-synth --scope user --agent universal

# Or pick one host: cursor / claude-code / codex / github-copilot
gh skill install ru-461/vv-synth vv-synth --scope user --agent claude-code

# From a local clone
gh skill install /path/to/vv-synth vv-synth --from-local --scope user --agent universal
```

Update later: `gh skill update vv-synth`. Pin a release: `gh skill install ru-461/vv-synth vv-synth --scope user --pin v0.1.1`. Pinned skills are skipped by `gh skill update`.

### `npx skills` (requires Node.js)

```shell
npx skills@latest add ru-461/vv-synth --skill vv-synth --global
npx skills@latest add ru-461/vv-synth --skill vv-synth --global --agent claude-code
```

Update later: `npx skills update vv-synth`.

## Publishing this skill (maintainers)

From the vv-synth repository root:

```shell
gh skill publish --dry-run    # validate only
gh skill publish --tag v0.1.1   # release (adds agent-skills topic)
```

Discovery path: `skills/vv-synth/SKILL.md` ([Agent Skills specification](https://agentskills.io/specification)).

After CLI, Engine setup, or terms guidance changes, bump `version` in `pyproject.toml` and `metadata.version` in both skills' `SKILL.md` files to the same value, publish with the matching `v<version>` tag, upload the same version to PyPI (Release section of the vv-synth README), and tell users to run `gh skill update vv-synth` and `uv tool upgrade vv-synth`.

## Engine preparation and terms

- Docker image: [voicevox/voicevox_engine](https://hub.docker.com/r/voicevox/voicevox_engine) — tag `cpu-latest` for CPU, `nvidia-latest` for NVIDIA GPU hosts.
- Official binaries: [VOICEVOX Engine Releases](https://github.com/VOICEVOX/voicevox_engine/releases).
- Do not vendor VOICEVOX Engine, voice libraries, model files, official binaries, Docker images, or generated WAV files into this skill.
- Generated audio use/distribution must follow the latest VOICEVOX Engine terms, voice library / speaker-specific terms, and credit requirements.
