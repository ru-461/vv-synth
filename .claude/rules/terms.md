# VOICEVOX terms and no-vendoring

This repository is an open-source (MIT) thin HTTP client CLI. The Engine and its assets are
always external.

## Do not vendor (never commit, never ship in the PyPI sdist / wheel)

- VOICEVOX Engine itself, official binaries, or Docker images
- Voice libraries and model files
- `voicevox_core/`, `download`
- Generated WAV files (`output/*.wav`, or `*.wav` anywhere)

Common Engine/Core/archive/audio paths are excluded by `.gitignore`. Do not add them back or
commit equivalent vendored assets under another path.

## Generated audio and credit

- Generated audio is subject to the **latest official VOICEVOX terms** and each voice
  library / speaker's own terms, including credit requirements.
- Before sharing or redistributing generated audio, confirm the applicable terms and the
  required VOICEVOX credit notation.
- If audio is embedded in an app or redistributed, the final distribution must also satisfy
  those terms.

## Official references

- VOICEVOX software terms: https://voicevox.hiroshiba.jp/term/
- VOICEVOX Q&A: https://voicevox.hiroshiba.jp/qa/
- Docker image: https://hub.docker.com/r/voicevox/voicevox_engine
- Engine releases: https://github.com/VOICEVOX/voicevox_engine/releases

The canonical policy text lives in
[README.md](../../README.md#oss-publication-and-voicevox-terms). Keep these links and the
no-vendoring policy intact.
