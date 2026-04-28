# DX Portal 全体像

## 1. システム全体図

```
┌─────────────────────────────────────────────────────────────┐
│                     あなた（リーダー）                         │
│                                                             │
│   やること: 書く → 判断する → レビューする                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ /company（唯一の窓口）
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    秘書（統合窓口）                            │
│                                                             │
│   できること:                                                │
│   - 思考・メモの受付 → 個人/チームを判断して振り分け             │
│   - 壁打ち・アイデア整理                                      │
│   - 朝のダッシュボード（Issue提案 + 未処理 + 依頼状況）          │
│   - 週次/月次レビュー生成                                     │
│   - PJ管理・依頼追跡・ナレッジ管理                             │
│   - /brain-status, /kickoff, /work 等のコマンド               │
│                                                             │
│   実体: dx-portal/.claude/skills/company/                    │
│   アクセス: ~/.claude/skills/company/ (symlink)               │
│                                                             │
└────────┬──────────────────────┬──────────────────────────────┘
         │                      │
         │ 個人的な思考           │ チームに関わること
         ▼                      ▼
┌──────────────────┐  ┌──────────────────────────────────────┐
│                  │  │                                      │
│  dx-brain        │  │  dx-portal                           │
│  (個人リポ)       │  │  (チームリポ)                          │
│  private         │  │  team shared                         │
│                  │  │                                      │
│  00_Inbox/       │  │  ┌─────────────┐ ┌────────────────┐  │
│  10_Journal/     │  │  │ コード部分    │ │ データ部分      │  │
│  20_Projects/    │  │  │             │ │                │  │
│  30_Tech_Notes/  │  │  │ skills/     │ │ company-data/  │  │
│  50_Business/    │  │  │ agents/     │ │  secretary/    │  │
│  90_System/      │  │  │ scripts/    │ │  projects/     │  │
│  99_Archives/    │  │  │ workflows/  │ │  dx-group/     │  │
│                  │  │  │ templates/  │ │  collaboration/│  │
│                  │  │  │ setup.sh    │ │  tech-knowledge│  │
│                  │  │  │             │ │  reviews/      │  │
│                  │  │  └─────────────┘ └────────────────┘  │
│                  │  │                                      │
└──────────────────┘  └──────────┬───────────────────────────┘
                                 │
                                 │ reusable workflows を提供
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  各プロジェクトリポ (app-x, app-y, ...)                        │
│                                                              │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐  │
│  │ アプリコード    │  │ .github/      │  │ .dx/             │  │
│  │              │  │ workflows/    │  │ pdm-config.yml   │  │
│  │ src/         │  │  auto-fix.yml │  │ pdm-prompt.md    │  │
│  │ tests/       │  │  pdm.yml      │  │ pdm-stats.json   │  │
│  │ ...          │  │  (数行で       │  │                  │  │
│  │              │  │   dx-portal   │  │ (PJ固有の         │  │
│  │              │  │   を呼ぶだけ)  │  │  AI設定)          │  │
│  └──────────────┘  └───────────────┘  └──────────────────┘  │
│                                                              │
│  ここで動くもの:                                               │
│  - PdM AI: 毎朝Issue自動提案 (gpt-4o-mini)                    │
│  - auto-fix: ラベル貼付 → 自動修正 → PR作成 (claude-code-action)│
│  - plan-first: 設計レビュー (claude-code-action)               │
│  - self-improve: 週次プロンプト自己改善 (gpt-4o-mini)           │
│  - /sprint-plan, /implement: AIスクラムチーム                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 2. 各リポの役割

### dx-brain（個人リポ・private）

```
目的: 個人の思考を蓄積する場所。他人には見えない。

誰が使う: メンバー各自（1人1リポ）
何を置く: 日記、アイデアメモ、個人的な学習記録、内省
更新頻度: 毎日（個人のペースで）
```

### dx-portal（チームリポ・shared）

```
目的: チームの共有基盤。2つの性質のものが同居している。

┌─────────────────────────────────────────────────┐
│  【コード部分】                                    │
│  更新頻度: 週1〜月1（機能追加・改善時）              │
│  変更方法: PR → レビュー → マージ                   │
│                                                   │
│  - skills/    秘書・brain・スプリントのスキル定義     │
│  - agents/    8つのAIエージェント設定               │
│  - scripts/   自動化スクリプト (auto-fix等)          │
│  - workflows/ 再利用可能なGitHub Actions            │
│  - templates/ dx-brain初期化テンプレート             │
│  - setup.sh   初回セットアップスクリプト             │
├─────────────────────────────────────────────────┤
│  【データ部分】 ← ★ここが問題                       │
│  更新頻度: 毎日・複数人が同時に                      │
│  変更方法: 秘書が直接ファイルを追加・更新             │
│                                                   │
│  - company-data/secretary/    壁打ち・会議メモ      │
│  - company-data/projects/     PJ進捗・タスク        │
│  - company-data/dx-group/     メンバー管理          │
│  - company-data/collaboration/ 依頼追跡             │
│  - company-data/tech-knowledge/ チーム技術ナレッジ   │
│  - company-data/reviews/       週次・月次レビュー    │
└─────────────────────────────────────────────────┘
```

### 各プロジェクトリポ（app-x, app-y, ...）

```
目的: 実際のアプリケーションコード + AI自動化

誰が使う: プロジェクトメンバー
何を置く: アプリコード、GitHub Actions呼び出し、PJ固有のAI設定
更新頻度: 毎日（開発中）
```

## 3. データの流れ（1日の例）

```
🌅 朝
   PdM AI ──(gpt-4o-mini)──→ プロジェクトリポにIssue提案
                                    │
   /company（秘書）                   │
      ↓                             │
   ダッシュボード表示 ◄───────────────┘
   「Issue 3件提案されています。依頼回答待ち 2件。」

🔧 作業中
   あなた: Issue #42 に auto-fix ラベルを貼る
      ↓
   GitHub Actions 発火
      ↓
   claude-code-action が worktree で修正
      ↓
   PR自動作成
      ↓
   あなた: PRをレビュー & マージ

💭 思考の記録
   あなた: 「稼働率の可視化、Grafanaがいいかも」
      ↓
   秘書が判断: これは個人の思考 → dx-brain/00_Inbox/ に保存

   あなた: 「品証の田中さんからトレサビの件で連絡あった」
      ↓
   秘書が判断: これはチームの依頼 → dx-portal/company-data/collaboration/ に保存

📊 週末
   /weekly-review
      ↓
   秘書が全データを集約してレビュー生成
      ↓
   自己改善ループ: PdM AIのプロンプトを統計から更新
```

## 4. 接続方法

```
~/.dx-config.yml (パスレジストリ)
┌─────────────────────────────┐
│ brain: ~/dx-brain            │──→ 秘書がここを読み書き
│ portal: ~/Apps/dx-portal     │──→ スキル・データの実体
│ company_data: (portal内)     │──→ 旧.companyの代替
│ projects:                    │
│   app-x: ~/Apps/app-x       │──→ プロジェクトリポの場所
│   app-y: ~/Apps/app-y       │
└─────────────────────────────┘

symlink (グローバルアクセス用)
┌──────────────────────────────────────────────────────┐
│ ~/.claude/skills/company → dx-portal/skills/company   │
│ ~/.claude/skills/brain   → dx-portal/skills/brain     │
│ ~/.claude/skills/sprint  → dx-portal/skills/sprint    │
│ ~/.company               → dx-portal/company-data     │
└──────────────────────────────────────────────────────┘
```

## 5. 問題点

### 問題1: dx-portal内のコード/データ混在

```
dx-portal/
├── skills/          ← コード（月1更新、PR経由）
├── agents/          ← コード
├── scripts/         ← コード
├── company-data/    ← データ（毎日更新、直接コミット）★ 性質が違う
│   ├── secretary/
│   ├── projects/
│   └── ...
```

【何が起きるか】
- company-dataは毎日何回もコミットされる（メモ追加、タスク更新等）
- スキル改修のPRに、データの変更が混ざってレビューしづらい
- git logがデータの変更で埋まり、コードの変更履歴が見づらい

【影響度】 ★★★ 高 — 日常運用で毎日ストレスになる
```

### 問題2: company-dataの同時編集コンフリクト

```
メンバーA: /company 「品証との打ち合わせメモ追加」
   → company-data/secretary/meetings/ にファイル追加
   → company-data/secretary/meetings/_index.md を更新

メンバーB: /company 「VSMプロジェクトのタスク更新」
   → company-data/projects/active/PJ-001/tasks/_index.md を更新

両者が同時にpush → _index.md でコンフリクト発生 ★
```

【何が起きるか】
- 同じ_index.mdを複数人が同時に更新するとコンフリクト
- 秘書がファイルを更新 → push → 別の人がpull忘れ → push失敗
- 手動マージが頻発して運用が破綻

【影響度】 ★★★ 高 — チーム利用で必ず発生する
```

### 問題3: WindowsでのSymlink

```
Linux/Mac:  ln -sf /path/to/target /path/to/link    ← 一般ユーザーで実行可能
Windows:    mklink /D link target                     ← 管理者権限が必要 ★

代替: junction (mklink /J)                            ← 管理者権限不要だがディレクトリのみ
```

【何が起きるか】
- チームメンバーがsetup.shを実行 → 管理者権限がなくて失敗
- junctionで代用可能だが、ファイル単位のsymlinkはできない

【影響度】 ★★ 中 — junctionで回避可能だが注意が必要
```

### 問題4: Reusable Workflowsの公開制限

```
GitHub の制約:
┌─────────────────────────────────────────────────┐
│ reusable workflow を別リポから呼ぶ条件:           │
│                                                   │
│ ✅ 呼び出し元が public リポ                        │
│ ✅ 同一 organization 内の private リポ              │
│ ❌ 個人アカウントの private リポ間 ★ ← 今回これ    │
└─────────────────────────────────────────────────┘

dx-portal (private) ──calls──→ ❌ 使えない
app-x (private)     ──calls──→ ❌ 使えない
```

【何が起きるか】
- 各プロジェクトリポからdx-portalのworkflowを呼べない
- 結局、各プロジェクトリポにworkflow全体をコピーする羽目になる
- 当初の「数行で呼ぶだけ」という設計が成り立たない

【影響度】 ★★★ 高 — アーキテクチャの前提が崩れる
```

## 6. 問題の全体マップ

```
dx-portal
┌──────────────────────────────────────────┐
│  skills/  agents/  scripts/  workflows/  │ ← コード
│         ┌────────────────────┐            │
│         │   company-data/    │ ★問題1     │ ← データが混在
│         │   (毎日更新)        │ ★問題2     │ ← コンフリクト
│         └────────────────────┘            │
└──────────────────┬───────────────────────┘
                   │
    symlink ★問題3 │ reusable WF ★問題4
    (Windows制約)   │ (private間で使えない)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
   ~/.claude/skills/    各プロジェクトリポ
```
