# 自作したい Skills 一覧（設計メモ）

## 前提
- 対象環境：Gitea（自社運用）+ Claude Code Team + team-standards リポ
- 土台：`gitea/gitea-mcp`（★必須）、`superpowers`、`claude-md-management`、`code-review`
- 設計思想：v2 デッキ「Gitea を作業場所と脳に変える」を実装として具体化する

---

## A. Issue ライフサイクル支援（優先度：高）

日々の「何をやるか・なぜやるか・どこまで進んだか」を Gitea 上に残す仕組み。**ここが集合知化の入り口**になる。

### A-1. `/morning-brief` — 朝のダッシュボード

**目的**：朝一番、チーム全員が同じ状況認識でスタートできるようにする。

**動き**：
1. Gitea MCP で自分のアサインド Issue・未処理 Issue・Draft PR を取得
2. CLAUDE.md の「Issue 起票ルール」（15分以上は Issue 化等）に照らして優先順位を提案
3. 「今日やるならこの 3 つ、理由は○○」と提示
4. 未処理の依頼・レビュー待ちも併せて表示

**出力**：Markdown の箇条書きサマリ（コピペで朝会に使える形）

**作る順序**：パイロット期（Month 1）に v0、Month 2 で提案ロジックを育てる。
**工数目安**：初版 4 時間、育てながら拡張。

---

### A-2. `/triage-gitea` — Issue の健康診断と優先順位提案

**目的**：Issue 一覧を定期的に棚卸しし、放置・ブロック・属人化を見える化する。

**動き**：
1. Gitea MCP で全 open Issue を取得
2. 以下 4 項目で分類：
   - **stale**：30 日以上更新なし
   - **blocked**：ブロッカーラベル / 依存 Issue が open / 「待ち」コメント検出
   - **orphaned**：assignee なし / 直近 14 日コミット活動なし
   - **mismatch**：ラベル（bug / critical 等）と実態（放置・着手済）の不整合
3. 並び替え提案 ＋ ヘルスサマリ（stale 率・blocked 率・orphan 率）を出す

**出力**：
- 優先度付き Issue リスト（CSV / Markdown）
- ヘルスサマリ 1 枚

**実行タイミング**：週次の振り返り前に 1 回（金曜 15 分ミーティングの準備資料として使う）

**作る順序**：Month 2 以降。まずは手動 triage を 4 週間やって「何が本当に欲しいか」を見極めてから。
**工数目安**：4〜8 時間。Linear 版 triage Skill の考え方を Gitea に移植。

---

### A-3. `/post-to-gitea-issue` — 壁打ちログを Issue にコメント投稿

**目的**：壁打ちの結論と経緯を Gitea に残し、後から追える形にする。

**動き**：
1. 直近のセッションから壁打ち内容を抽出
2. 4 項目テンプレに整形：
   - 【前提】状況・背景
   - 【検討した選択肢】2〜3 個
   - 【結論】採用した案
   - 【却下理由】選ばなかった理由
3. Gitea MCP 経由で `create_issue_comment` を呼ぶ

**出力**：Issue へのコメント投稿 ＋ 投稿 URL をユーザーに返す

**v2 デッキでの位置づけ**：レイヤー 3 の自作 Skill、**Week 1 で作る必須アイテム**。
**工数目安**：2〜4 時間。

---

## B. 開発フロー（優先度：中）

Issue から PR までの流れを滑らかにする補助 Skill。

### B-1. セルフレビュー拡張（CLAUDE.md 準拠チェッカー）

**目的**：PR を出す前に、CLAUDE.md のチームルールを自分で確認できる。

**動き**：
1. ベース：`Git Diff Reviewer` を拡張
2. diff を読みつつ CLAUDE.md を参照
3. 違反候補（例：`any` 使用、Serendie 非使用、コミット prefix 欠落）を列挙
4. テストファイルの存在確認（実装があるのにテストがない場合は警告）

**出力**：違反候補リスト＋修正提案

**v2 デッキでの位置づけ**：レイヤー 2 の拡張、**Month 1 終盤**に作る。
**工数目安**：4〜6 時間。

---

### B-2. `/issue-to-draft-pr` — Issue の結論から Draft PR を立ち上げる

**目的**：壁打ち結論がついた Issue から、ブランチ＋雛形 PR を自動生成する。

**動き**：
1. 対象 Issue を指定（番号またはリンク）
2. Issue の【結論】を読んで、想定ファイル一覧と変更方針を抽出
3. `feature/issue-<番号>` ブランチを作成
4. PR 本文に Issue の 4 項目テンプレを転記、テスト観点・影響範囲の叩き台を追加
5. Draft 状態で作成

**出力**：Draft PR の URL

**作る順序**：Month 2〜3。`/post-to-gitea-issue` の運用が定着してから。
**工数目安**：半日〜1 日。

---

## C. チーム基盤のメンテナンス（優先度：中）

team-standards リポを腐らせないための運用 Skill。

### C-1. `/trim-claude-md` — CLAUDE.md の月 1 刈り込み

**目的**：CLAUDE.md が 200 行を超えないよう、定期的に整理する。

**動き**：
1. ベース：`claude-md-management` + `Auto Dream`
2. 現在の行数・セクション構成を分析
3. 以下を候補として洗い出す：
   - 直近 30 日で参照されていない（コミット log から推定）
   - 他のルールと重複
   - Skills に切り出すべき手順書
4. 削除・移動の提案をチームに出す（PR として）

**出力**：刈り込み PR のドラフト

**v2 デッキでの位置づけ**：レイヤー 2、**Month 1 仕上げ**で導入。
**工数目安**：6〜10 時間。

---

### C-2. `team-standards 初期設定` — リポジトリ雛形の自動生成

**目的**：新しくチームを立ち上げるとき、team-standards リポの骨組みを一気に作る。

**動き**：
1. Gitea に空リポジトリを作成
2. 以下を初期コミット：
   - `CLAUDE.md` 初版（30 行の雛形）
   - `skills/` / `agents/` / `hooks/` / `mcp/` のディレクトリ構造
   - `.mcp.json` テンプレート（gitea-mcp 前提）
   - `settings.json` テンプレート（Day 1 Hooks 3 つ含む）
3. README に運用ガイドを生成

**出力**：初期化された team-standards リポ

**v2 デッキでの位置づけ**：レイヤー 3、**Day 1** で使う。
**工数目安**：半日。

---

### C-3. Gitea 自動レビュー CI（Phase 3 以降・任意）

**目的**：PR 作成時に Claude が自動でレビューコメントを付ける。

**動き**：
1. Gitea Actions で `pull_request` イベントを受ける
2. worktree 上で `code-review` プラグイン相当を起動
3. 5 並列エージェントで型チェック・テスト・CLAUDE.md 準拠・過去失敗事例を確認
4. PR にレビューコメントを投稿

**参考**：`markwylde/claude-code-gitea-action`

**作る順序**：Month 3 以降、チームが PR レビュー運用に慣れてから。
**工数目安**：1〜2 日。

---

## D. 将来作るかもしれないもの（優先度：低・保留）

- `/weekly-review`：週次の振り返りを壁打ちログ・PR・Issue から自動生成（yamapiiii 参考）
- `/sprint-plan`：スクラム的な運用に寄せる場合（nogataka 参考、パイロットでは不要）
- `/orchestrate`：5 軸スコアリングで完全自動化（推進役依存の罠対策が固まってから）
- `/deep-research`：社内ドキュメント＋Web を横断検索（MCP の種類が増えてから）

---

## 導入順序のまとめ

| Phase | 期間 | 作る Skill |
|---|---|---|
| Phase 1 | Day 1 | `team-standards 初期設定`（C-2） |
| Phase 1 | Week 1 | `/post-to-gitea-issue`（A-3） |
| Phase 2 | Month 1 前半 | `/morning-brief` v0（A-1） |
| Phase 2 | Month 1 後半 | セルフレビュー拡張（B-1）、`/trim-claude-md`（C-1） |
| Phase 3 | Month 2 | `/triage-gitea`（A-2）、`/issue-to-draft-pr`（B-2） |
| Phase 3 | Month 3 以降 | Gitea 自動レビュー CI（C-3）、D 群を検討 |

---

## 制約・考え方

- **既存 Skill で足りる部分は自作しない**：v2 デッキ p16 の「13 機能中 10 は既存活用」原則を守る
- **最初から完璧を目指さない**：`/morning-brief` v0 は 4 時間、使いながら育てる
- **Gitea MCP に依存する**：すべての Skill は Gitea MCP 経由で動く前提（独自 API 実装はしない）
- **team-standards/skills/ に集約**：個人リポには置かない。チーム共有が前提
- **CLAUDE.md との整合性**：Skill が参照する軸（優先順位のルール等）は CLAUDE.md に書く。Skill は手順、CLAUDE.md は規範
