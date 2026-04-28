---
description: ユーザーの要望を整理・切り分けて Gitea issue に登録（ラベル自動推定 + ユーザー確認）
argument-hint: <要望内容>
---

# Gitea Issue 新規登録フロー（要望整理付き）

ユーザーの漠然とした要望を分析し、必要に応じて複数 issue に切り分け、ラベルを自動推定したうえでユーザー確認を経て Gitea に登録してください。

## 手順

### Step 1: 要望受領

引数 `$ARGUMENTS` があればそれを使用。未指定の場合はユーザーに「どんな要望を登録しますか？」と尋ねる。

複数行の要望や曖昧な記述（例: 「XX が遅い、あと YY も追加したい」）でも受け付ける。

### Step 2: 要望の分析・切り分け

受領した要望を分析し、**独立した関心事かどうか** を判定:

**同一 issue にすべき条件**:
- 同じドメイン（backend/frontend 等）
- 同じ種別（bug/feature/等）
- 密接に関連し、独立リリースが困難

**別 issue に切り分ける条件**:
- 異なるドメイン
- 異なる種別（bug と feature の混在）
- 異なる優先度
- 独立してリリース可能
- 互いに依存しない

切り分け結果を TodoWrite で管理（「issue-1 作成」「issue-2 作成」...）。

### Step 3: 各 issue の素案作成

各 issue について以下を整理:

#### 3.1 タイトル
- 簡潔な名詞句（50 文字以内目安）
- 例: 「ログイン画面のパスワード強度チェック追加」

#### 3.2 種別ラベルの自動推定 (`type/*`)

| 判定キーワード | 推定値 |
|---|---|
| バグ、不具合、動かない、エラー、直したい、壊れている、失敗する | `type/bug` |
| 追加したい、新機能、できるようにしたい、対応したい | `type/feature` |
| 整理、リファクタ、コード改善、構造見直し | `type/refactor` |
| ドキュメント、資料、説明、README、Wiki | `type/docs` |
| 遅い、速く、パフォーマンス、応答時間、最適化 | `type/perf` |

該当なしの場合はデフォルトで `type/feature`。

#### 3.3 優先度ラベルの自動推定 (`priority/*`)

| 判定キーワード・状況 | 推定値 |
|---|---|
| 障害、データ損失、クラッシュ、本番停止、緊急 | `priority/critical` |
| エラー、不具合、ユーザー影響大、急ぎ、仕事が止まる | `priority/high` |
| （デフォルト、明確な緊急性なし） | `priority/medium` |
| 改善要望、nice to have、余裕があれば、時間あるとき | `priority/low` |

#### 3.4 本文テンプレート

```markdown
## 概要
<1-2 行で要件を端的に記述>

## 背景
<なぜこの対応が必要か、何がきっかけで認識したか>

## 期待する動作
<実装後にどうなってほしいか>

## 再現手順 (type/bug の場合)
1. <手順 1>
2. <手順 2>
3. <結果>

## 影響範囲
<想定される変更対象: 例 "backend/xxx.service.ts", UI の xxx パネル 等>

## 関連 issue
<Step 4 で調査した結果を記載、なければ「(なし)」>
```

type/bug 以外では「再現手順」セクションは省略。

### Step 4: 関連 issue の調査

`gitea.mjs list --state open` で open issue の一覧を取得:

```bash
node scripts/gitea/gitea.mjs list --state open --limit 30
```

各 issue のタイトルを要望のキーワードと突き合わせ、関連しそうなものを抽出。本文の「関連 issue」セクションに記載:

```markdown
## 関連 issue
- #22 XX 機能拡張（本 issue の前提）
```

関連度が曖昧なものは無理に追加せず、明らかに関連するもののみ記載。

### Step 5: ユーザー確認

整理した issue 案を以下の形式で提示:

```
## 作成予定の issue (N 件)

### Issue 1/N
- タイトル: <タイトル>
- ラベル: priority/<値> + status/todo + type/<値>
- 本文:
  <本文プレビュー>

### Issue 2/N
...

---

これで登録してよろしいですか？
- OK: そのまま登録
- 修正: 「Issue 1 の優先度を high に」「Issue 2 のタイトルを...」等で指示
- キャンセル: 登録中止
```

ユーザー返答に応じて:
- **OK** → Step 6 へ
- **修正** → 該当箇所を修正して再提示
- **追加分割** → Step 2 に戻り再分析
- **キャンセル** → 何もせず終了

### Step 6: Gitea に登録

確認が取れた issue を 1 件ずつ登録:

```bash
# issue 本文を .tmp/new-issue-<連番>.md に保存してから作成
# （ここでは issue 1 件目の例）
node scripts/gitea/gitea.mjs create \
  --title "<タイトル>" \
  --body-file ".tmp/new-issue-1.md"
```

作成後、レスポンスから issue 番号を取得し、ラベルを付与:

```bash
node scripts/gitea/gitea.mjs label add <作成された番号> \
  "priority/<値>,status/todo,type/<値>"
```

### Step 7: 結果報告

すべての issue 登録完了後、以下を提示:

```
## 登録完了 ✅

| # | タイトル | ラベル | URL |
|---|---|---|---|
| #24 | ... | priority/medium, status/todo, type/feature | <URL> |
| #25 | ... | priority/high, status/todo, type/bug | <URL> |

## 次のアクション
- `/gitea-feature <番号>` で実装に着手可能
- Gitea UI で各 issue を確認・微調整
```

## 注意事項

- **ラベル推定は初期値**: ユーザーが明確に「bug として扱う」「緊急」等指定していれば優先
- **本文の品質重視**: 曖昧な記述があれば Step 5 でユーザーに詳細を聞く
- **関連 issue の乱用を避ける**: キーワードが一致しただけで無関係なものは含めない
- **Gitea API 認証**: `.env.local` の `GITEA_TOKEN` / `GITEA_REPO` / `GITEA_API_BASE` を使用（事前設定必須）
- **ラベル未投入時**: `gitea.mjs label init-scheme` を先に実行してもらうか、ユーザーに促す

## よくあるケース

### ケース 1: 単一の明確な要望
> 「ログインボタンを押しても反応しない」

→ 1 件の issue、`type/bug` + `priority/high`

### ケース 2: 複合要望
> 「画面のドラッグが重いのと、背景画像を複数登録したい」

→ 2 件に分割:
- Issue A: `type/perf` + `priority/medium`
- Issue B: `type/feature` + `priority/low`

### ケース 3: 既存 issue と関連
> 「XX 計算の精度を上げたい」

→ 1 件、関連 issue として既存の同系統 issue を本文に記載

### ケース 4: 優先度判断が曖昧
要望に緊急性の手がかりがない場合は **medium** をデフォルトとし、Step 5 でユーザーに「この優先度で登録しますか？」と明示確認。
