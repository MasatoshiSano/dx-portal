# Claude CodeでGitHubのIssueを自動作成・PR作成・自己成長させてみた

- **URL**: https://qiita.com/umamichi/items/ee3c5b6aee3b4c3e8b0e
- **著者**: @umamichi (Masataka Umamichi)
- **公開日**: 2026-03-27
- **プラットフォーム**: Qiita

## 概要

GitHub Actionsを使い、AI駆動の開発ワークフロー自動化システムを構築した事例。毎朝自動でIssueを提案し、ラベル付けによってコード実装とPR作成を自動化する。

## システム構成

| コンポーネント | 役割 | 技術 |
|--------------|------|------|
| PdM AI | 毎朝6時にIssue自動提案 | OpenAI gpt-4o-mini |
| plan-firstフロー | ラベル付与で実装プランをコメント | Claude Code |
| auto-implementフロー | ラベル付与でコード実装とPR作成 | Claude Code |
| 自己改善ループ | 毎週月曜、過去の提案採否を分析してプロンプト自動更新 | gpt-4o-mini |

## 技術的実装

### PdM AI（提案役）

```typescript
const response = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    { role: "system", content: systemPrompt },
    { role: "user", content: userPrompt },
  ],
  temperature: 0.9,
});
```

### GitHub Actionsトリガー

```yaml
on:
  schedule:
    - cron: "0 21 * * *"  # UTC 21:00 = JST 6:00
```

### Claude Code Action設定

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    claude_args: "--max-turns 45 --dangerously-skip-permissions"
```

## 実装上の課題と解決策

| 課題 | 解決策 |
|------|--------|
| ターン数制限（デフォルト10で途中停止） | `--max-turns 45`に増加 |
| 大規模機能の実装失敗 | サブIssueへの自動分割 |
| AIの的外れなコード生成 | CLAUDE.mdにアーキテクチャ説明とファイルパスを記載 |
| 対話確認のスキップ | `--dangerously-skip-permissions`（CI環境用） |

## コスト概算

| 用途 | モデル | 月コスト |
|------|--------|---------|
| PdM AI（毎日） | gpt-4o-mini | 数十円 |
| 自己改善（週次） | gpt-4o-mini | 数円 |
| 実装処理 | Claude API | 実装複雑度による |

## 重要なポイント

- 人間の担当は「ラベル貼付」と「PRレビュー＆マージ」のみ
- 企画から実装までの工程をAIが自動化
- 採用/却下の統計から自身のプロンプトを進化させる自己改善の仕組み
- CLAUDE.mdの質がAIの実装品質に直結する
- 権限管理はGitHub Actionsの`permissions`セクションで厳密に制御
