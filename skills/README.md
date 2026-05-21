# Agent Skills (vv-synth)

[Agent Skills](https://agentskills.io/specification) 形式のスキルです。GitHub CLI の `gh skill` で **Cursor / Claude Code / Codex / GitHub Copilot** などにインストールできます。

## スキル一覧

| ディレクトリ | 名前 | 用途 |
|-------------|------|------|
| [`vv-synth/`](vv-synth/) | `vv-synth` | **任意のプロジェクト**で `vv-synth` CLI による TTS |
| [`vv-synth-dev/`](vv-synth-dev/) | `vv-synth-dev` | **本リポジトリ**の開発・スモークテスト |

正本は `skills/*/SKILL.md` です。手動コピー用の旧パス `share/cursor-skill-vv-synth/` は非推奨です。

## グローバルインストール（推奨）

GitHub CLI **v2.90+** が必要です。リポジトリを GitHub に push し、`OWNER/vv-synth` として公開したあと:

```shell
# 複数エージェント共通（~/.agents/skills など）
gh skill install OWNER/vv-synth vv-synth --scope user --agent universal

# エージェントを指定する例
gh skill install OWNER/vv-synth vv-synth --scope user --agent cursor
gh skill install OWNER/vv-synth vv-synth --scope user --agent claude-code
gh skill install OWNER/vv-synth vv-synth --scope user --agent codex
gh skill install OWNER/vv-synth vv-synth --scope user --agent github-copilot

# 本リポジトリ開発用（任意）
gh skill install OWNER/vv-synth vv-synth-dev --scope user --agent cursor
```

ローカル clone から（公開前の検証）:

```shell
gh skill install /path/to/vv-synth vv-synth --from-local --scope user --agent universal
gh skill preview /path/to/vv-synth vv-synth --from-local
```

更新・固定:

```shell
gh skill update vv-synth
gh skill install OWNER/vv-synth vv-synth@v1.0.0 --scope user --pin v1.0.0
```

## プロジェクトスコープ

そのリポジトリだけで使う場合:

```shell
cd /path/to/your-app
gh skill install OWNER/vv-synth vv-synth --scope project --agent cursor
```

## 公開（メンテナ）

```shell
cd /path/to/vv-synth
gh skill publish --dry-run
gh skill publish --tag v1.0.0
```

`agent-skills` トピック付きの GitHub Release が作成されます。スキル内容を変えたらタグを上げ、利用者に `gh skill update` を案内してください。

## ディレクトリ構成

```
skills/
├── README.md           # このファイル
├── vv-synth/
│   ├── SKILL.md        # ポータブル TTS（gh で配布）
│   └── references/
│       └── REFERENCE.md
└── vv-synth-dev/
    └── SKILL.md        # 本リポジトリ開発用
```

## エージェント別の配置先（`--scope user` の例）

`gh skill install` がホストごとにコピーします（手動で触る必要は通常ありません）。

| Agent | 典型的なパス |
|-------|----------------|
| universal / 共有 | `~/.agents/skills/vv-synth/` |
| Cursor | `~/.cursor/skills/vv-synth/` |
| Claude Code | `~/.claude/skills/vv-synth/` |
| Codex | Codex 設定の skills ディレクトリ |
| GitHub Copilot | `~/.copilot/skills/vv-synth/` |

## 本リポジトリ内 Cursor

`.cursor/skills/vv-synth-dev/` は clone 直後から Cursor が読めるように同梱しています。内容は `skills/vv-synth-dev/` と同期してください。

## 事前準備（CLI 利用者）

1. Docker で VOICEVOX Engine（`skills/vv-synth/SKILL.md` 参照）
2. `uv tool install --editable .` で `vv-synth` を PATH に追加（README 参照）
