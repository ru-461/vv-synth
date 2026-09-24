# Security

- Do not read or edit secret-like files (`.env*`, credentials, private keys, tokens).
- Do not add credentials to code, docs, examples, or tests. Use environment variables for
  configuration such as `VOICEVOX_ENGINE_URL`.
- Do not include credentials in new CLI error messages or logs.
- The default Engine URL is local (`http://127.0.0.1:50021`). Remote Engine use is the
  operator's responsibility.
