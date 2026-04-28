---
description: Gitea issue を元に feature-dev ワークフローで改修し、PR を作成
argument-hint: <issue番号>
---

# Gitea Issue → Feature Dev 改修 + PR 作成フロー

引数で指定された Gitea issue を取得し、**専用ブランチを切って feature-dev スキルで実装し、最後に PR を作成**してください。マージは人間が判断します。

## 📋 プロジェクト設定（導入時に書き換える）

| 項目 | 値の例 | このプロジェクトの値 |
|---|---|---|
| 作業ディレクトリ（`{{WORKDIR}}`） | `.` / `packages/app` | `.` |
| Git リモート名（`{{REMOTE}}`） | `origin` / `aws` | `origin` |
| ベースブランチ（`{{BASE_BRANCH}}`） | `main` / `develop` / `feature/xxx` | `main` |
| Gitea リポジトリ（`{{GITEA_REPO}}`） | `All_Users/your-repo` | `All_Users/your-repo` |

以下の手順内 `{{WORKDIR}}` / `{{REMOTE}}` / `{{BASE_BRANCH}}` / `{{GITEA_REPO}}` は上表の値に読み替えて実行する。

## 手順

### Step 1: Issue 取得

```bash
node scripts/gitea/gitea.mjs get $ARGUMENTS
```

保存先: `.tmp/issue-$ARGUMENTS.md`

引数が数値でない・未指定の場合は一覧を表示して選択を促す:
```bash
node scripts/gitea/gitea.mjs list --state open --limit 20
```

### Step 2: Issue 内容確認 + ブランチ slug 提案

Read ツールで `.tmp/issue-$ARGUMENTS.md` を読み、以下をユーザーに提示:
- タイトル / 状態 / ラベル
- 要求内容の要約（3-5 行）
- 受け入れ条件
- **ブランチ名案**: `issue-$ARGUMENTS/<slug>` 形式で提案（issue タイトルから kebab-case で導出）
  - 例: タイトル「ログイン画面のパスワード強度チェック追加」→ `issue-15/password-strength`
  - ユーザー承認を得る（変更希望なら新 slug で再提示）

### Step 3: ブランチ作成 + ステータス遷移

作業ディレクトリで承認済みのブランチを作成:

```bash
cd {{WORKDIR}}
git fetch {{REMOTE}} {{BASE_BRANCH}}
git checkout -b issue-$ARGUMENTS/<slug> {{REMOTE}}/{{BASE_BRANCH}}
```

既に同名ブランチが存在する場合は `checkout` のみ:
```bash
git rev-parse --verify issue-$ARGUMENTS/<slug> && git checkout issue-$ARGUMENTS/<slug> || git checkout -b issue-$ARGUMENTS/<slug> {{REMOTE}}/{{BASE_BRANCH}}
```

ブランチ作成成功後、issue のステータスを **対応中** に遷移:

```bash
node scripts/gitea/gitea.mjs label add $ARGUMENTS "status/in-progress"
```

`status/*` は排他スコープのため、既存の `status/todo` は自動的に外れる。

### Step 4: feature-dev スキル起動

Skill ツールを使って `feature-dev:feature-dev` スキルを起動:

```
Skill(skill="feature-dev:feature-dev", args="Gitea issue #$ARGUMENTS: <タイトル>\n\n要件:\n<本文要約>\n\n受け入れ条件:\n<抽出したチェックリスト>\n\n関連コンテキスト:\n- .tmp/issue-$ARGUMENTS.md を参照\n- リポジトリ: {{GITEA_REPO}} (Gitea)\n- ブランチ: issue-$ARGUMENTS/<slug>\n- ベースブランチ: {{BASE_BRANCH}}")
```

スキル起動後は feature-dev が自動実行:
- code-explorer による既存コード調査
- code-architect による実装計画
- ユーザー確認 → 実装
- code-reviewer によるレビュー

### Step 5: 実装中の注意点

feature-dev のワークフローに従いつつ、プロジェクトの `CLAUDE.md` のコーディング規則を遵守してください。主要な共通規則:

- **TDD**: 新規機能は test-first
- **セキュリティ**: 秘匿情報をハードコードしない
- **CLAUDE.md**: プロジェクト固有の型規則 / 命名規則 / ファイルサイズ上限等に従う

### Step 6: commit + push（ブランチへ）

実装・レビュー完了後:

```bash
# commit (コミットメッセージは <type>: <summary> 形式。type = feat / fix / refactor / docs / test / chore / perf / ci)
# closes #$ARGUMENTS は commit ではなく PR 本文で記載する
git add <files>
git commit -m "<type>: <summary>"

# ブランチを Gitea に push
git push {{REMOTE}} issue-$ARGUMENTS/<slug>
```

### Step 7: PR 本文を作成

`.tmp/pr-$ARGUMENTS.md` に PR 本文を作成:

```markdown
## 関連 issue
Closes #$ARGUMENTS

## 変更概要
<実装した内容の要約、どのファイル・どの機能を変えたか>

## 変更ファイル
- `path/to/file1`
- `path/to/file2`

## テスト
- 新規テスト: N 件
- 既存テスト: N pass / M fail (M は pre-existing の場合その旨)

## 動作確認
- [ ] typecheck
- [ ] 単体テスト
- [ ] 実機確認（必要な場合）

## レビュー観点
- [ ] 機能要件の満たし
- [ ] テストカバレッジ
- [ ] 既存挙動との後方互換
- [ ] CLAUDE.md 規約遵守

🤖 Generated with /gitea-feature
```

### Step 8: PR 作成

```bash
node scripts/gitea/gitea.mjs pr create \
  --title "<PR タイトル>" \
  --head "issue-$ARGUMENTS/<slug>" \
  --base "{{BASE_BRANCH}}" \
  --body-file ".tmp/pr-$ARGUMENTS.md"
```

PR タイトルの推奨形式: `<type>: <summary> (#$ARGUMENTS)`
- 例: `feat: ログイン画面のパスワード強度チェックを追加 (#15)`

### Step 9: Issue に PR URL コメント + ステータス遷移

PR URL を issue にコメント投稿:
```bash
node scripts/gitea/gitea.mjs comment $ARGUMENTS "PR #<PR番号> を作成しました: <PR URL>"
```

ステータスを **レビュー中** に遷移:
```bash
node scripts/gitea/gitea.mjs label add $ARGUMENTS "status/in-review"
```

`status/*` は排他なので、`status/in-progress` は自動的に外れる。

**Issue は close しない**。PR がマージされたら手動 or Gitea の自動 close（PR 本文の `Closes #<番号>` による）で閉じる。

## 完了後の手動作業（参考）

ユーザーが PR をレビュー・マージした後:

1. ローカルをベースブランチに戻し pull:
   ```bash
   git checkout {{BASE_BRANCH}}
   git pull {{REMOTE}} {{BASE_BRANCH}}
   ```
2. マージ済みブランチをローカル・Gitea から削除:
   ```bash
   git branch -d issue-$ARGUMENTS/<slug>
   git push {{REMOTE}} --delete issue-$ARGUMENTS/<slug>
   ```

## 参考: feature-dev を使わず単発エージェントで済ませる場合

小さな修正（タイポ・設定値変更・1 ファイルの簡易バグ修正）では、Step 4 で feature-dev スキルを使わず直接実装することもあります:

- `feature-dev:code-explorer` — 調査のみ
- `feature-dev:code-architect` — 設計のみ
- `feature-dev:code-reviewer` — レビューのみ

その場合も Step 3（ブランチ作成）と Step 6〜9（push/PR/コメント）は同様に行ってください。
