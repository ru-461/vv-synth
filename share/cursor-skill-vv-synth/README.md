# 非推奨: 手動コピー用パス

Agent Skills の正本はリポジトリ直下の [`skills/vv-synth/`](../../skills/vv-synth/) です。

## 推奨: GitHub CLI でインストール

```shell
gh skill install OWNER/vv-synth vv-synth --scope user --agent universal
```

詳細: [`skills/README.md`](../../skills/README.md)

## 旧来の手動コピー（非推奨）

```shell
mkdir -p ~/.cursor/skills/vv-synth
cp ../../skills/vv-synth/SKILL.md ~/.cursor/skills/vv-synth/SKILL.md
```

`SKILL.md` はこのディレクトリには置かず、`skills/vv-synth/SKILL.md` のみをメンテナンスしてください。
