---
name: tech-blog
description: >
  技術的知見をブログ記事として投稿するスキル。デバッグ・機能実装・アーキテクチャ設計・
  パフォーマンス最適化・設定変更・AI指示の試行錯誤など、他の開発者に共有すべき
  技術的な学びを記事化する。記事の生成・編集・非公開・削除・一覧表示に対応。
  起動条件は CLAUDE.md の Blog Writing Rule を参照。
---

# Tech Blog

## コマンド体系

| コマンド | 動作 |
|---------|------|
| `/tech-blog` | 会話から新規記事の候補を提案する |
| `/tech-blog [キーワード]` | キーワードに関連する知見を収集して新規記事を作成する |
| `/tech-blog edit [slug]` | 既存記事を修正する |
| `/tech-blog unpublish [slug]` | 既存記事を非公開にする |
| `/tech-blog delete [slug]` | 既存記事を完全に削除する |
| `/tech-blog list` | 投稿済み記事の一覧を表示する |

引数の先頭が `edit` / `unpublish` / `delete` / `list` の場合は「既存記事の管理」フローへ進む。それ以外は「新規記事の作成」フローへ進む。

---

## 新規記事の作成

以下の手順で行う:

1. 会話を分析してブログ候補を提案する
2. 既存記事との重複を確認する
3. 記事を生成する（テンプレートは [references/article-template.md](references/article-template.md) を参照）
4. ユーザーに確認を取る
5. カバー画像を取得する
6. ファイル作成と git push する

## Blog Repository

- **パス**: スキル実行時のカレントディレクトリ（`$(pwd)`）
- **記事保存先**: `content/posts/`
- **デプロイ**: `main` ブランチへ push → GitHub Actions が S3 + CloudFront に自動デプロイ

## Step 1: Analyze Context and Propose Blog Candidates

何を書くかユーザーに聞き返さない。引数の有無に応じて情報源を切り替える。

### 1a. 情報源の決定

- **引数あり** (`/tech-blog DynamoDB GSI` 等): 引数をキーワードとして `content/posts/` やプロジェクト内のソースコードを Grep/Glob で検索し、関連する実装・設定・コミット履歴から技術的知見を収集する
- **引数なし**: 会話全体を振り返り、ブログ候補となるトピックを抽出する

### 1b. ブログ候補を抽出する

収集した情報から、以下の **いずれか** に該当するトピックを候補として列挙する:

| 基準 | 質問 |
|------|------|
| **検索される知見か** | 他の開発者が同じ状況でググったとき、この記事が役立つか？ |
| **再発防止の記録か** | 同じ間違いを繰り返さないために、原因と対策を残すべきか？ |
| **AI試行錯誤の知見か** | AIコーディングで試行錯誤があり、「最初からこうすれば回り道しなかった」と言えるか？ |

**対象例**: バグの原因と対策、環境構築のハマりどころ、ライブラリの非自明な使い方、デプロイ手順、ストリーミング実装のようなパターン。

**AI試行錯誤の対象例**:
- AIが最初に選んだアプローチでエラーが発生し、別のアプローチで解決した
- ユーザーの指示が曖昧でAIが誤解し、指示を具体化・変更して解決した
- 同じ目的でやり直し・方針転換が発生した
- → テンプレートの **Pattern A: 課題解決型** を使用する

**対象外**: 単純なタイポ、自明な設定ミス、一度限りの環境固有問題。

### 1c. 分割の判断

候補ごとに、1記事で収まるか複数回に分けるべきか判断する:
- **分割の目安**: 技術領域が3つ以上にまたがる、コード例が多い、前提知識の説明が長くなる場合
- **分割する場合**: 全何回の構成になるか、各回のテーマを提示する

### 1d. 候補をユーザーに提示する

候補が複数ある場合は一覧で提示し、どれを記事にするかユーザーに選んでもらう。候補が1つなら、その旨を伝えて確認する。分割が必要な場合は構成案も併せて提示する。

## Step 2: Check for Duplicates

Grep ツールで `content/posts/*.md` 内の `^title:` を検索し、既存記事のタイトル一覧を取得する。
テーマが重複していればユーザーに報告し判断を仰ぐ。

## Step 3: Generate Article

[references/article-template.md](references/article-template.md) のテンプレートに従い記事を生成する。

注意事項:
- 個人情報・認証情報（APIキー等）が含まれていないか確認し、センシティブな値はマスクする
- コードブロックには適切な言語指定をつける
- カテゴリは内容に応じて選ぶ: `Debugging`, `HowTo`, `Architecture`, `Performance`, `DevOps` 等
- **バイブコーディング用プロンプトを必ず含める**: 記事の内容をAIコーディングアシスタントに正しく実装させるためのプロンプト例を記載する（テンプレートの「バイブコーディングで実装する」セクションを参照）
- **初心者への配慮**: 難しい概念にはASCII図解やMermaid図、具体例を入れて読みやすくする
- **シリーズ記事の場合**: [references/series-rules.md](references/series-rules.md) に従い、フロントマターに `series` / `seriesOrder` を設定し、本文冒頭にナビゲーション（全何回の何回目か + 他回へのリンク）を入れる

## Step 4: Confirm with User

記事の草稿を提示し、ユーザーの承認を得てから次へ進む。

## Step 5: Fetch Cover Image

記事の topics からキーワードを作り、[scripts/fetch-cover-image.sh](scripts/fetch-cover-image.sh) でカバー画像を取得する。

```bash
bash ~/.claude/skills/tech-blog/scripts/fetch-cover-image.sh "<topics をスペース区切り>" "<slug>"
```

- **成功時**: stdout に `coverImage` 用パス（例: `/images/posts/slug-cover.jpg`）が返る。フロントマターに `coverImage: "<返されたパス>"` を追加する
- **失敗時**: `coverImage` をフロントマターに含めない（既存の Unsplash プリセット自動選択にフォールバック）

## Step 6: Create File and Git Push

1. Write ツールで `content/posts/YYYY-MM-DD-[slug].md` を作成する
2. Read ツールで書き込みを検証する
3. 現在のブランチを確認する:

```bash
git branch --show-current
```

**`main` ブランチの場合** → そのまま commit & push:

```bash
git add content/posts/[file].md content/posts/[slug]-cover.jpg && git commit -m "Add: [title]" && git push origin main
```

※ カバー画像の取得に失敗した場合は `public/images/posts/[slug]-cover.jpg` を git add から省く。

**`main` 以外の場合** → ユーザーに選択肢を提示:
- A) `main` に切り替えてから commit & push
- B) 現在のブランチにコミットし、後で `main` にマージ
- C) 投稿を後回しにする

---

## 既存記事の管理

既存記事の管理（list / edit / unpublish / delete）は [references/article-management.md](references/article-management.md) を参照。
