# Security Policy

`vv-synth` is a small command-line client that talks to a separately prepared VOICEVOX
Engine over local HTTP and writes WAV files to disk. It does not run a server, handle
credentials, or process untrusted network input by default.

## Supported versions

This project is pre-1.0. Releases are published to [PyPI](https://pypi.org/project/vv-synth/)
and as GitHub Releases. Security fixes are applied to the latest release and `main`; older
versions are not maintained. Upgrade with `uv tool upgrade vv-synth`.

| Version | Supported |
|---------|-----------|
| `0.1.x` / `main` | Yes |
| older | No |

## Reporting a vulnerability

Please report security issues **privately**. Do not open a public issue for a vulnerability.

- Use GitHub's **"Report a vulnerability"** button under this repository's **Security** tab
  (Security Advisories). This opens a private report visible only to the maintainers.
- Include the affected version (`uv tool list` shows the installed one) or commit,
  environment (OS, Python, Engine type), reproduction steps, and the impact you observed.

You can expect an initial acknowledgement within a reasonable time. If a fix is needed, we
will coordinate a disclosure timeline with you before publishing details.

## Out of scope

- **VOICEVOX Engine** vulnerabilities: report these upstream at
  [VOICEVOX/voicevox_engine](https://github.com/VOICEVOX/voicevox_engine). `vv-synth` only
  calls its HTTP API.
- **VOICEVOX terms / credit / licensing** questions about generated audio: these are not
  security issues. See [OSS Publication And VOICEVOX Terms](README.md#oss-publication-and-voicevox-terms)
  and [VOICEVOX Q&A](https://voicevox.hiroshiba.jp/qa/).
- Connecting `vv-synth` to an untrusted or remote Engine URL is the operator's
  responsibility; the default target is `http://127.0.0.1:50021`.
