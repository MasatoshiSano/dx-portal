# 既存記事の管理

## list: 記事一覧の表示

`content/posts/*.md` を Glob で取得し、各ファイルのフロントマター（title, date, published, topics）を一覧表示する。

```
# | date       | published | title                          | slug
1 | 2026-02-28 | true      | DynamoDB Single-Table Design… | 2026-02-28-dynamodb-single-table-chat-design
2 | 2026-02-21 | true      | WSL2でCDK deployが失敗する…    | 2026-02-21-aws-cdk-deploy-permission-error
```

## edit: 記事の修正

1. **対象記事の特定**: slug が指定されていれば `content/posts/[slug].md` を Read する。slug が曖昧・未指定なら `list` を表示してユーザーに選んでもらう
2. **現在の内容を表示**: フロントマターと本文を読み込み、ユーザーに現在の状態を提示する
3. **修正内容の確認**: ユーザーに何を修正したいか確認する（タイトル、本文、タグ、カテゴリ等）
4. **修正を適用**: Edit ツールでファイルを更新する
5. **Read ツールで検証**: 更新後の内容を確認する
6. **commit & push**:

```bash
git add content/posts/[file].md && git commit -m "Update: [title]" && git push origin main
```

## unpublish: 記事の非公開化

1. **対象記事の特定**: edit と同様
2. **現在の状態を確認**: フロントマターの `published` が既に `false` なら「既に非公開です」と通知して終了
3. **ユーザーに確認**: 記事タイトルを表示し、非公開にしてよいか確認する
4. **`published: false` に変更**: Edit ツールで `published: true` → `published: false` に書き換える
5. **Read ツールで検証**
6. **commit & push**:

```bash
git add content/posts/[file].md && git commit -m "Unpublish: [title]" && git push origin main
```

再公開する場合は `edit` で `published: true` に戻す。

## delete: 記事の完全削除

1. **対象記事の特定**: edit と同様
2. **ユーザーに確認**: 記事タイトルを表示し、**完全に削除してよいか明確に確認する**（この操作は不可逆）
3. **カバー画像の確認**: フロントマターの `coverImage` パスに対応するファイルが `public/` にあれば一緒に削除する
4. **ファイル削除と commit & push**:

```bash
git rm content/posts/[file].md content/posts/[slug]-cover.jpg && git commit -m "Delete: [title]" && git push origin main
```

※ カバー画像が存在しない場合は `git rm` から省く。
