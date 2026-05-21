# vv-synth skill reference

## Output path rules

| Invocation (cwd = target project) | Typical result |
|------------|----------------|
| (no `-o`) | `output/YYYYMMDD-HHMMSS.wav` |
| `-o hello.wav` | `output/hello.wav` |
| `-o path/to/a.wav` | `path/to/a.wav` |
| `--output-dir artifacts` | `artifacts/...` |

Implementation: `vv_synth/output_paths.py` in the vv-synth repository.

## Publishing this skill (maintainers)

From the vv-synth repository root:

```shell
gh skill publish --dry-run    # validate only
gh skill publish --tag v1.0.0   # release (adds agent-skills topic)
```

Discovery path: `skills/vv-synth/SKILL.md` ([Agent Skills specification](https://agentskills.io/specification)).

After CLI or Engine changes, bump `metadata.version` in `SKILL.md`, publish a new tag, and tell users to run `gh skill update vv-synth`.

## Engine image

[voicevox/voicevox_engine](https://hub.docker.com/r/voicevox/voicevox_engine) — tag `cpu-latest` for most Mac/Linux dev hosts.
