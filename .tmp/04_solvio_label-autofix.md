# 「Claude Code × GitHub Actions」Issueにラベル貼るだけで自動修正＆PR作成する仕組みを作ってみた

- **URL**: https://zenn.dev/solvio/articles/63842f1417883a
- **著者**: @sho_（Solvio株式会社）
- **公開日**: 2026-03-26
- **プラットフォーム**: Zenn

## 概要

GitHub Issueに「auto-fix」ラベルを付与するだけで、Claude Codeによる自動コード修正とPR作成を実現するシステムの構築方法。

## アーキテクチャ

1. ユーザーがIssueに「auto-fix」ラベルを付与
2. GitHub Actionsが発火してスクリプト実行
3. Claude CodeがGit worktree上でコード修正
4. 自動的にPR作成

## ラベルベースのステータス管理

| ラベル | 意味 |
|--------|------|
| `auto-fix` | 修正リクエスト |
| `auto-fix-in-progress` | 修正実行中 |
| `auto-fix-done` | 完了・PR作成済み |
| `auto-fix-failed` | 失敗 |

## ディレクトリ構成

```
プロジェクトルート/
├── .github/workflows/auto-fix-issue.yml
├── scripts/auto-fix-issue.mjs
├── CLAUDE.md
└── package.json
```

## コード実装の3ステップ

### Step 1: Worktreeの準備

```javascript
execSync(`git worktree add -B ${branchName} ${worktreeDir} main`)
```

メインの作業ディレクトリを汚さず、隔離された環境を作成。複数Issue同時処理にも対応可能。

### Step 2: Claude Code実行

プロンプトでClaude Codeに指示:
- Git設定
- コード修正とセルフレビュー
- Lint実行
- コミット・プッシュ
- PR作成（対話的入力を避けるため全オプション指定）

`cwd`オプションでworktreeディレクトリを指定することが重要。

### Step 3: 後片付け

```javascript
finally {
  execSync(`git worktree remove -f ${worktreeDir}`)
}
```

成功・失敗を問わず必ずworktreeを削除。

## GitHub Actionsワークフロー設定

- **トリガー**: `issues.labeled`
- **権限**: contents・pull-requests・issuesへの書き込み権限
- **タイムアウト**: 30分
- **Concurrency制御**: 同一Issue番号での同時実行防止

## Git Worktreeの利点

| 観点 | ブランチ切り替え | git worktree |
|------|-----------------|-------------|
| 作業ディレクトリ | 共有（1つ） | 分離独立 |
| 既存作業への影響 | あり | なし |
| 並列実行 | 不可 | 可能 |

## セルフホステッドランナーの採用理由

コスト比較（月20回実行想定）:
- **GitHub-hosted**: 約$2.4/月（Actions課金）+ Claude Code利用料
- **Self-hosted**: $0/月（Actions課金なし）+ Claude Code利用料

## 自動修正に向いているIssue

**向いている**:
- 明確なバグ修正（エラーメッセージ・再現手順が記載）
- 軽微なUI修正やtypo
- 単純なロジック変更

**向いていない**:
- 大規模リファクタリング
- 要件が曖昧な新機能
- データベースマイグレーション
- セキュリティ関連

## 重要な注意

- 自動作成されたPRは**必ず人間がレビューしてからマージ**する
- 本システムはあくまでドラフト作成のサポートツール

## 事前準備

1. セルフホステッドランナー（またはGitHub-hosted）にClaude Code CLIと`ANTHROPIC_API_KEY`を設定
2. GitHub CLI認証（`gh`コマンドと`GITHUB_TOKEN`）
3. 4つのラベルをリポジトリに事前作成
