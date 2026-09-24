# Commit rules

- Commit only when the user explicitly asks. Never commit without permission.
- Use a single-line English message: `prefix: message`.
- Pick one prefix that matches the change.

## Prefixes

| Prefix | Use for |
|--------|---------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `update` | Enhancement to an existing feature |
| `refactor` | Refactor with no behavior change |
| `style` | Formatting only, no logic change |
| `test` | Tests only |
| `chore` | Build, deps, tooling, misc |

Examples: `feat: add --pitch option`, `docs: update engine setup`, `fix: show one-line error`.

## Never commit

`output/*.wav`, `voicevox_core/`, `download`, VOICEVOX Engine binaries, models, voice
libraries, `*.7z`, `*.vvpp`, or virtual environments. See `terms.md` for the no-vendoring
policy.
