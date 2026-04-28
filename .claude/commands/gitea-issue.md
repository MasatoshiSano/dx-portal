---
description: Gitea issue を取得して .tmp/issue-<番号>.md に保存
argument-hint: <issue番号>
---

# Gitea Issue 取得

引数で指定された Gitea issue 番号を API 経由で取得し、本文・コメント・メタデータを整形した Markdown を `.tmp/issue-<番号>.md` に保存してください。

## 手順

1. 引数 `$ARGUMENTS` から issue 番号を取得。数値でない場合はエラーを返す
2. 以下のコマンドを実行:
   ```bash
   node scripts/gitea/gitea.mjs get $ARGUMENTS
   ```
3. 保存先パス `.tmp/issue-$ARGUMENTS.md` を Read ツールで読み込み、内容を要約してユーザーに提示
4. 要約には以下を含める:
   - タイトル
   - 状態（open/closed）
   - ラベル
   - 本文の要点（3-5 行）
   - 主要コメント数

## 引数が指定されていない場合

`.env.local` の設定（`GITEA_REPO`）を元に open issue 一覧を表示:
```bash
node scripts/gitea/gitea.mjs list --state open --limit 20
```

そのあと「どの issue を取得しますか？」とユーザーに尋ねる。

## 前提

- プロジェクトルートに `.env.local` があり、`GITEA_TOKEN` / `GITEA_REPO` / `GITEA_API_BASE` が設定されていること
- `scripts/gitea/gitea.mjs` がプロジェクトに配置されていること

未設定・未配置の場合は、`team-standards` リポの `SETUP.md` を参照するよう案内してください。
