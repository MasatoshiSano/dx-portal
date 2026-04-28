# 集合知化ワークフロー：構成要素インベントリ

4視点レビュー後に合計7エージェント（Skills 調査4体 + Subagents/Hooks/MCP 調査3体）で調査した、
このワークフローに必要な Claude Code の5つの構成要素（CLAUDE.md / Skills / Subagents / Hooks / MCP）を
公式・コミュニティ・自作の3レイヤーで整理する。

---

## エグゼクティブサマリ

- **必要な機能の 80% は既存の公式プラグインまたは超メジャーな Skill/Subagent でカバーできる**
- **完全自作が必要なのは 4 つだけ**（Gitea 連携の一部、team-standards 初期設定、CI 連携、任意の社内 API MCP）
- 調査対象の13シナリオのうち、10シナリオは既存でそのまま使える
- **⚠️ 警告**: MCP には重大な脆弱性が見つかっているものがある（CVE複数）。導入前にセキュリティチェックリスト必須

---

## レイヤー1：そのまま使える（最優先インストール）

### 1.1 Anthropic 公式プラグイン

| プラグイン | 配布元 | 用途 | このワークフローでの使い道 |
|---|---|---|---|
| **superpowers** | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 統合ワークフロー Skill 集 | 壁打ち・計画・TDD・並列レビュー・デバッグの総合 |
| **claude-md-management** | 公式 Plugin Marketplace | CLAUDE.md 品質監査 | `/revise-claude-md` で肥大化検出、stale 削除 |
| **code-review** | 公式 | 5並列エージェント PR レビュー | 信頼度フィルタで重要指摘のみ抽出 |
| **feature-dev** | 公式 | 7段階機能開発フロー | Issue→設計→実装→レビューの誘導 |
| **pr-review-toolkit** | 公式 | 6種類の専門レビュー | コメント・テスト・エラー・型・品質・簡潔性 |
| **commit-commands** | 公式 | Git 自動化 | `/commit`, `/commit-push-pr` |
| **hookify** | 公式 | カスタム Hook 作成 | 不要な行動の自動防止 |
| **skill-creator** | 公式 | Skill 開発テンプレ | 自作 Skill の土台生成 |

**インストール方法**:
```
/plugin install <plugin-name>@claude-plugins-official
```

### 1.2 超メジャーなコミュニティ Skill

| Skill | URL | スター・評価 | 用途 |
|---|---|---|---|
| **obra/superpowers** | [github.com/obra/superpowers](https://github.com/obra/superpowers) | 144k stars | 統合スキル集 |
| **awesome-claude-code** | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | キュレーション決定版 | リポジトリ集 |
| **awesome-claude-code-subagents** | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 130+ subagents | 専門エージェント集 |
| **claude-config-doctor** | [tyabu12/claude-config-doctor](https://github.com/tyabu12/claude-config-doctor) | - | CLAUDE.md 複数ファイルの conflict 検出 |

### 1.3 superpowers に含まれる主要 Skill（obra/superpowers）

このワークフローで使うもの：

| Skill | 用途 | いつ使う |
|---|---|---|
| `brainstorming` | 設計議論の構造化 | 壁打ちフェーズ |
| `writing-plans` | 仕様→実装計画 | 設計フェーズ |
| `test-driven-development` | TDD サイクル強制 | 実装フェーズ |
| `dispatching-parallel-agents` | 複数エージェント並列実行 | レビューフェーズ |
| `requesting-code-review` | スペック準拠確認 | PR 前 |
| `systematic-debugging` | 根本原因分析 | バグ対応 |
| `using-git-worktrees` | 並列ブランチ作業 | 並列開発 |
| `verification-before-completion` | 完了前の検証強制 | PR 前 |

### 1.4 VoltAgent の専門 Subagents（130+から選ぶ）

この構想の「専門秘書」にそのまま使えるもの：

| Subagent | 用途 |
|---|---|
| **code-reviewer** | 一般的なコード品質レビュー |
| **architect-reviewer** | 設計・責務分離・拡張性 |
| **security-auditor** | 脆弱性・認証漏れ |
| **test-coverage-checker** | テスト不足の検出 |
| **debugger** | 根本原因分析 |

**導入方法**: `.claude/agents/` に該当 .md ファイルをコピー

### 1.5 Gitea 連携：公式 MCP

**`gitea/gitea-mcp`** — [gitea.com/gitea/gitea-mcp](https://gitea.com/gitea/gitea-mcp)

- Gitea 公式配布、Go 実装
- Issue 作成・コメント・PR 管理・リポジトリ操作
- 認証：Personal Access Token
- Windows/Mac/Linux 対応

**インストール**:
```bash
claude mcp add --transport stdio --scope user gitea \
  --env GITEA_ACCESS_TOKEN=xxxxx \
  --env GITEA_HOST=https://your-gitea.example.com \
  -- go run gitea.com/gitea/gitea-mcp@latest
```

### 1.6 サードパーティ Gitea MCP（代替候補）

| リポジトリ | 特徴 |
|---|---|
| [MushroomFleet/gitea-mcp](https://github.com/MushroomFleet/gitea-mcp) | TypeScript実装、マルチインスタンス |
| [raohwork/forgejo-mcp](https://github.com/raohwork/forgejo-mcp) | Forgejo（Gitea フォーク）特化 |

→ **推奨は公式版**。機能充実度で優る。

---

## レイヤー2：既存をカスタマイズ（低〜中難易度）

### 2.1 壁打ちログ → 4項目テンプレ抽出

- **ベースにする**: `superpowers:brainstorming` + `Meeting Notes Architect`（mcpmarket.com）
- **追加するもの**: 「前提・選択肢・結論・却下理由」の抽出ロジック
- **難易度**: 中（4-8時間）
- **ポイント**: 「却下された選択肢」の明示的抽出ロジックが既存にない

### 2.2 セルフレビュー Skill

- **ベースにする**: `Git Diff Reviewer`（mcpmarket.com）
- **追加するもの**:
  - CLAUDE.md 準拠チェック
  - 新規コードにテスト存在確認
  - 過去の失敗事例パターンマッチ
- **難易度**: 低（4-6時間）
- **ポイント**: `allowed-tools` で Grep/Bash を追加すれば実装可能

### 2.3 CLAUDE.md 月1刈り込み

- **ベースにする**: `claude-md-management` + `Auto Dream`（公式）
- **追加するもの**:
  - 200行上限の監視
  - 月1トリガー（Hook + cron 的運用）
  - 削除候補の判定ロジック
- **難易度**: 低〜中（6-10時間）
- **ポイント**: 判定基準（古い日付・冗長な例・アーカイブ対象）を team で合意が必要

---

## レイヤー3：完全自作が必要（3つだけ）

### 3.1 `/post-to-gitea-issue` slash command

**目的**: 壁打ちログの要約を Gitea の Issue に自動投稿

**実装方法**:
- Gitea MCP 経由で `POST /repos/{owner}/{repo}/issues/{index}/comments` を叩く
- 入力：Issue番号 + 要約内容
- 出力：投稿URL

**参考実装**: [markwylde/claude-code-gitea-action](https://github.com/markwylde/claude-code-gitea-action)

**難易度**: 低（2-4時間）

**Skill定義の骨格**:
```markdown
---
name: post-to-gitea-issue
description: 壁打ちログの要約を指定のIssueにコメント投稿する
---

# 壁打ちログを Gitea Issue に投稿

1. 現在の壁打ち内容を 4項目テンプレで要約する
2. Issue番号を確認する
3. gitea MCP を使って `create_issue_comment` を呼ぶ
4. 投稿結果の URL を返す
```

### 3.2 team-standards リポジトリの初期設定

**目的**: 全員が共有する基盤を用意

**難易度**: 低（半日）

**作るもの**:
```
team-standards/
├── CLAUDE.md              # チーム共通ルール（最初は200行以内）
├── README.md              # このリポジトリの使い方
├── skills/
│   └── README.md          # 空で OK、後から追加
├── agents/
│   └── README.md          # VoltAgent からコピーする予定
├── hooks/
│   └── README.md
├── mcp/
│   └── gitea-mcp.json     # Gitea MCP の設定テンプレ
└── .mcp.json              # プロジェクト用 MCP 設定
```

**初版 CLAUDE.md に入れる内容**（例）:
- 開発の流れ（Issue → 壁打ち → PR）
- コーディング規約（any 禁止、Serendie 使用など）
- 過去の失敗あるある（空の章を用意）
- 15分ルール、4項目テンプレ

### 3.3 Gitea ラベルトリガーの自動 PR レビュー CI

**目的**: 特定のラベルを PR に付けると、自動で Claude Code がレビューする

**ベース**: [markwylde/claude-code-gitea-action](https://github.com/markwylde/claude-code-gitea-action)

**難易度**: 中（1-2日）

**注意**: これは**パイロットの Phase 3（3ヶ月目以降）**の話。最初の1-2ヶ月は手動運用で十分

---

## カバレッジマトリックス：10シナリオ × 状況

| # | シナリオ | 既存 Skill | 使い方 |
|---|---|---|---|
| 1 | 壁打ち支援 | ✅ superpowers:brainstorming | そのまま |
| 2 | 4項目テンプレ抽出 | △ 部分的 | Meeting Notes Architect を拡張（L2） |
| 3 | 機能追加の標準手順 | ✅ superpowers spec-driven-dev | そのまま |
| 4 | TDD（テストファースト） | ✅ superpowers:test-driven-development | そのまま |
| 5 | セルフレビュー | ✅ Git Diff Reviewer | CLAUDE.md 準拠追加（L2） |
| 6 | PR 並列レビュー | ✅ VoltAgent + dispatching-parallel-agents | そのまま |
| 7 | CLAUDE.md 管理・刈り込み | △ 部分的 | claude-md-management + 月1独自（L2） |
| 8 | Gitea Issue/PR 操作 | ✅ gitea/gitea-mcp | そのまま |
| 9 | git worktree 並列開発 | ✅ superpowers:using-git-worktrees | そのまま |
| 10 | Issue コメント自動投稿 | ❌ なし | 自作（L3） |
| 11 | team-standards 基盤 | ❌ なし | 自作（L3） |
| 12 | Gitea ラベル自動レビュー CI | △ 参考実装あり | ベース流用（L3、Phase 3） |
| 13 | 根本原因分析 | ✅ superpowers:systematic-debugging | そのまま |

---

## 推奨インストール順序

### Phase 1：必須セット（Day 1、2時間以内）

```bash
# 1. Gitea MCP（各自の PC で実行）
claude mcp add --transport stdio --scope user gitea \
  --env GITEA_ACCESS_TOKEN=$GITEA_TOKEN \
  --env GITEA_HOST=https://your-gitea.example.com \
  -- go run gitea.com/gitea/gitea-mcp@latest

# 2. 公式プラグインのインストール
/plugin install superpowers@claude-plugins-official
/plugin install claude-md-management@claude-plugins-official

# 3. team-standards リポジトリ作成（Gitea 上）
#    CLAUDE.md 初版を3名で合意して commit
```

### Phase 2：強化（Week 1）

```bash
# 4. PR レビュー系プラグイン
/plugin install code-review@claude-plugins-official
/plugin install feature-dev@claude-plugins-official

# 5. VoltAgent の subagents をコピー
#    必要なもの（code-reviewer, architect-reviewer, security-auditor）を
#    team-standards/agents/ にコピー

# 6. /post-to-gitea-issue slash command を自作
#    team-standards/skills/post-to-gitea-issue.md に配置
```

### Phase 3：仕上げ（Month 1）

```bash
# 7. セルフレビュー Skill を拡張
#    team-standards/skills/review-my-changes.md（自作）

# 8. CLAUDE.md 月1刈り込みの Hook 設定
#    team-standards/hooks/monthly-prune.sh（自作）

# 9. Gitea CI 連携（Phase 3 以降、余力があれば）
#    markwylde/claude-code-gitea-action を参考に構築
```

---

## 注意点（調査で判明した実務的な罠）

### コミュニティ Skill の品質
- 2026年監査で **73%の community skills が 60/100 未満**
- **信頼できるのは**: Superpowers、VoltAgent、Anthropic公式のみ
- **他は慎重に選ぶ**（silent failure が多い）

### Gitea 連携の制限
- `claude-code-gitea-action` は**セキュリティ理由で formal PR reviews の提出が不可**
- コメント投稿は可能だが、レビュー承認はできない
- 参考実装として使う

### Token 管理
- Gitea Access Token は絶対に team-standards に入れない
- 各自の `.env` ファイルで管理
- `.gitignore` に `.env` を必ず追加

### Gitea バージョン
- `gitea-mcp` は Gitea 1.20+ 推奨

### Skills の旧形式について
- `.claude/commands/` は廃止、`.claude/skills/` に統合済み
- 2026年1月の Skills 体系統合で変更
- 古いドキュメントを参考にするときは注意

### CLAUDE.md サイズ
- 公式は「200行以下」を明言
- それ以上になると秘書が指示を見落とし始める
- 長文が必要なら Skills に切り出す

---

## 参考 URL

### 公式
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)
- [Anthropic 公式プラグインマーケットプレイス](https://github.com/anthropics/claude-plugins-official)
- [claude-md-management Plugin](https://claude.com/plugins/claude-md-management)
- [code-review Plugin](https://claude.com/plugins/code-review)

### コミュニティ
- [obra/superpowers](https://github.com/obra/superpowers)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills)

### Gitea
- [gitea/gitea-mcp 公式](https://gitea.com/gitea/gitea-mcp)
- [markwylde/claude-code-gitea-action](https://github.com/markwylde/claude-code-gitea-action)
- [Bringing Claude Code to Gitea (ブログ)](https://markwylde.com/blog/bringing-claude-code-to-gitea/)
- [Gitea API Documentation](https://docs.gitea.com/api/1.20/)

### その他有用
- [claude-config-doctor](https://github.com/tyabu12/claude-config-doctor) - CLAUDE.md conflict 検出
- [Pimzino/claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow) - Spec-driven 実装例

---

# 第2部：Subagents 調査結果

## Subagents とは

**特定の役割に特化した秘書**。独立したコンテキストウィンドウ、カスタム system prompt、ツール制限を持つ。
タスクに応じて Claude 本体が自動委譲するか、`@agent-name` で明示的に呼び出す。

## S1. 公式バンドル・プラグイン

Claude Code 本体に組み込みの自動委譲機能があり、公式プラグインには以下が含まれる：
- **general code reviewer**
- **security-focused reviewer**（OWASP 脆弱性・認証漏れ検出）
- **test generation agent**

**2026 年の新機能**:
- **Agent Teams**（2026-02）— 複数 Claude インスタンス並列実行、共有タスクリスト
- **@mention typeahead**（2026-04）— subagent 呼び出し簡素化

## S2. 決定版：VoltAgent/awesome-claude-code-subagents

**URL**: [github.com/VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

**規模**: 130+ subagents、10カテゴリ

**カテゴリ**:
1. Core Development
2. Language Specialists
3. Infrastructure
4. **Quality & Security**（16 subagents、我々の中心）
5. Data & AI
6. Developer Experience
7. Specialized Domains
8. Business & Product
9. Meta & Orchestration
10. Research & Analysis

**インストール**:
```bash
git clone https://github.com/VoltAgent/awesome-claude-code-subagents.git
./install-agents.sh  # 対話型、Global か Local 選択
```

## S3. このワークフローで使う6つの Subagent

team-standards/agents/ にコピーするもの：

| Subagent | 用途 | VoltAgent 内の場所 |
|---|---|---|
| **code-reviewer** | 一般的コード品質 | categories/04-quality-security/ |
| **architect-reviewer** | 設計妥当性・拡張性 | 同上 |
| **security-auditor** | 脆弱性・認証漏れ | 同上 |
| **test-coverage-checker** / **qa-expert** | テスト不足検出 | 同上 |
| **debugger** / **error-detective** | 根本原因分析 | 同上 |
| **dependency-manager** | 依存関係監査 | 同上 |

→ **自作の必要はほぼゼロ**。コピーするだけ。

## S4. Subagent のツール制限（必須設定）

各 subagent の frontmatter でツールを制限する。特にセキュリティ系は書き込みを禁止：

```yaml
---
name: security-auditor
description: 脆弱性・認証漏れの専門レビュー
tools: Read, Grep, WebSearch      # allowlist
disallowedTools: Write, Bash       # explicit deny
model: sonnet                       # 品質重視
---
```

**モデル別使い分け**:
| モデル | 用途 | コスト |
|---|---|---|
| **Haiku 4.5** | 探索・一次レビュー | 80% 削減、4-5x 高速 |
| **Sonnet 4.5** | 品質重視レビュー | 標準 |
| **Opus** | 複雑な推論 | 高 |

## S5. 並列実行

`superpowers:dispatching-parallel-agents` を使うと、複数 subagent を同時起動できる。
例：PR レビュー時に code-reviewer + architect-reviewer + security-auditor を並列起動。

## S6. その他の注目コミュニティ Subagent 集

| リポジトリ | 特徴 |
|---|---|
| [0xfurai/claude-code-subagents](https://github.com/0xfurai/claude-code-subagents) | 100+ production-ready |
| [wshobson/agents](https://github.com/wshobson/agents) | Multi-agent orchestration |
| [lst97/claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents) | Full-stack 開発向け |

---

# 第3部：Hooks 調査結果

## Hooks とは

**特定のイベントで自動実行されるスクリプト**。CLAUDE.md の「約束事」を「強制力のあるルール」に変える仕組み。
「CLAUDE.md は提案、Hooks は法律」とも言われる。

## H1. 全 Event Type（2026 年時点で 21 イベント）

主要なもの：

| Event | タイミング | ブロック可 | 我々の用途 |
|---|---|---|---|
| **SessionStart** | セッション開始時 | No | team-standards を `git pull` で最新化 |
| **UserPromptSubmit** | プロンプト送信時 | Yes | CLAUDE.md 違反検出、コンテキスト注入 |
| **PreToolUse** | ツール実行前 | Yes | 危険コマンド（rm -rf）ブロック、push 前テスト |
| **PermissionRequest** | パーミッション許可時 | Yes | 追加検証ゲート |
| **PostToolUse** | ツール実行後 | No | auto-format、lint、テスト実行 |
| **Stop** | Claude 応答終了時 | Yes | PR 作成前の最終チェック |
| **SessionEnd** | セッション終了時 | No | 壁打ちログ保存、統計収集 |

他に CompactStart、ConfigLoad、ConfigChange など計 21 イベント。

## H2. 4つのハンドラータイプ

1. **command** — Shell スクリプト（Node.js 推奨。後述）
2. **http** — 外部 API への POST リクエスト
3. **prompt** — LLM による単一ターン評価（Haiku デフォルト）
4. **agent** — フル subagent 統合

## H3. ⚠️ 必ず Node.js で書く

**Bash で書くと Windows/WSL で動かない**。クロスプラットフォーム対応のため、Hooks は Node.js（`.mjs`）で書くのが鉄則：

- Windows ネイティブの Claude Code でパス解決失敗
- WSL 経由で動かすと bash 解決問題
- Node.js なら 3 OS で同一動作

## H4. コミュニティの決定版

| リポジトリ | 特徴 |
|---|---|
| [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | 13 イベント実装、Python ベース |
| [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks) | 262 テスト、安全性レベル 3 段階 |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | コミュニティ集 |

## H5. Day 1 に入れる3つの Hook

team-standards/hooks/ に置く最小構成：

### Hook 1: `save-transcript.mjs`（SessionEnd）— 壁打ちログ自動保存

**settings.json**:
```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "node .claude/hooks/save-transcript.mjs"
      }]
    }]
  }
}
```

**save-transcript.mjs**:
```javascript
import fs from 'fs';
import path from 'path';

const input = JSON.parse(await fs.promises.readFile(0, 'utf-8'));
const content = await fs.promises.readFile(input.transcript_path, 'utf-8');
const logsDir = path.join(input.cwd, '.claude', 'logs', 'transcripts');
await fs.promises.mkdir(logsDir, { recursive: true });
const filename = `${new Date().toISOString().replace(/:/g, '-')}.md`;
await fs.promises.writeFile(path.join(logsDir, filename), content);
console.log(JSON.stringify({ decision: 'continue' }));
```

### Hook 2: `lint-on-edit.mjs`（PostToolUse）— 自動 lint/format

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$CLAUDE_FILE_PATH\"",
        "async": true,
        "timeout": 60
      }]
    }]
  }
}
```

### Hook 3: `bash-guard.mjs`（PreToolUse）— 危険コマンドブロック

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "if": "Bash(rm -rf *)",
      "hooks": [{
        "type": "command",
        "command": "node .claude/hooks/bash-guard.mjs",
        "timeout": 30
      }]
    }]
  }
}
```

## H6. Hooks のベストプラクティス

### やること
- ✅ `.claude/settings.json` を git commit（チーム共有）
- ✅ `.claude/settings.local.json` は個人設定（gitignore）
- ✅ `async: true` を積極的に使う（同期 hook は作業を妨げる）
- ✅ `timeout` を必ず設定
- ✅ Node.js で書く

### 避けること
- ❌ stdout に標準出力を混入（JSON のみ返す、shell 設定が邪魔になる）
- ❌ 全 PostToolUse で同期実行（180 秒遅延の実例あり）
- ❌ Bash ハードコード（Windows/WSL で動かない）
- ❌ matcher なしのグローバル hook

### Exit code 規則
- `0`: 成功（stdout JSON 処理）
- `2`: ブロック（stderr を Claude にフィードバック）
- その他: 警告レベル

## H7. デバッグ

```bash
claude --debug-file /tmp/debug.log
# or
claude --debug
# → ~/.claude/debug/<session-id>.txt に hook マッチング・exit code・stderr が記録される
```

---

# 第4部：MCP 調査結果（Gitea 以外）

## MCP とは

**Model Context Protocol** — Claude Code が外部ツール（Slack、DB、Wiki 等）と連携する仕組み。
秘書が「手元のコード以外」を読み書きできるようになる。

## M1. ⚠️ 最重要：セキュリティ警告

**2025-2026 年に発見された MCP の深刻な脆弱性**。導入前に必ず確認：

| MCP | 脆弱性 | 影響 |
|---|---|---|
| **mcp-remote (npm)** | **CVE-2025-6514** | 558K ダウンロード済み |
| **mcp-server-git** | **CVE-2025-68145-6** RCE | - |
| **SQLite 参考実装** | **SQL Injection** | 5000+ fork 被害 |
| **Microsoft MarkItDown** | **SSRF** | EC2 メタデータ露出 |
| **gemini-mcp-tool** | **Shell Injection CVSS 9.8** | 未パッチ |

→ **OWASP MCP Top 10** ([owasp.org](https://owasp.org/www-project-mcp-top-10/)) を必ず確認。
→ **コミュニティ MCP はレビューしてから導入**、できれば**公式のみに限定**する。

---

# 第3.5部：settings.json の禁止事項（permissions.deny）

## 3つの防御層

Hooks とは別に、settings.json でハード制限を設定できる。3つの防御層を使い分ける：

| 層 | 仕組み | 強制力 | たとえ |
|---|---|---|---|
| **CLAUDE.md** | 秘書への「お願い」 | 弱（守らないことがある） | 約束 |
| **settings.json** | ツール・コマンドの禁止 | **強（物理的にできない）** | 鍵 |
| **Hooks** | イベント時の自動検証 | 中〜強（exit 2 でブロック） | 番人 |

→ **「絶対ダメ」は settings.json、「状況による」は Hooks、「心がけ」は CLAUDE.md**

## チームで入れるべき禁止事項

`.claude/settings.json`（git commit してチーム全員に配布）:

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force*)",
      "Bash(git push * --force*)",
      "Bash(git reset --hard*)",
      "Bash(git checkout -- .)",
      "Bash(git clean -fd*)",
      "Bash(DROP *)",
      "Bash(DELETE FROM * WHERE 1*)",
      "Bash(chmod 777*)",
      "Bash(curl * | bash*)",
      "Bash(curl * | sh*)"
    ]
  }
}
```

## 各禁止項目の理由

| 禁止コマンド | 理由 |
|---|---|
| `rm -rf *` | ファイル全消失。取り返しがつかない |
| `git push --force` | リモートの履歴を上書き。他メンバーの作業が消える |
| `git reset --hard` | ローカルの未コミット変更が全て消える |
| `git checkout -- .` | 作業中の変更が全て消える |
| `git clean -fd` | 未追跡ファイルが全て消える |
| `DROP / DELETE FROM` | DB の破壊的操作 |
| `chmod 777` | セキュリティ無効化 |
| `curl | bash` | 外部スクリプトの盲目的実行 |

## settings.json と Hooks の使い分け

| やりたいこと | settings.json | Hooks |
|---|---|---|
| 特定コマンドを**完全禁止** | ✓ | - |
| 条件付きで**判断して**ブロック | - | ✓ |
| **実行後**に整形・チェック | - | ✓（PostToolUse） |
| **ログを残す** | - | ✓（SessionEnd） |

## settings.json + Hooks の統合例（team-standards 用）

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force*)",
      "Bash(git push * --force*)",
      "Bash(git reset --hard*)",
      "Bash(git checkout -- .)",
      "Bash(git clean -fd*)",
      "Bash(DROP *)",
      "Bash(chmod 777*)",
      "Bash(curl * | bash*)"
    ]
  },
  "hooks": {
    "SessionEnd": [{
      "hooks": [{ "type": "command", "command": "node .claude/hooks/save-transcript.mjs" }]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{ "type": "command", "command": "npx prettier --write \"$CLAUDE_FILE_PATH\"", "async": true, "timeout": 60 }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "node .claude/hooks/bash-guard.mjs", "timeout": 30 }]
    }]
  }
}
```

→ permissions（鍵）と hooks（番人）を1つのファイルに統合。git commit でチーム全員に配布。

---

## M2. Anthropic 公式・参照実装 MCP サーバー

**リポジトリ**: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

| サーバー | 用途 | 閉域OK |
|---|---|---|
| **Fetch** | Web コンテンツ取得・変換 | ⚠️ 外部URL必須 |
| **Filesystem** | ファイル操作（制御可能） | ✓ |
| **Git** | Git リポジトリ操作 | ✓ |
| **Memory** | グラフベース永続記憶 | ✓ |
| **Time** | 時刻・タイムゾーン | ✓ |
| **Sequential Thinking** | 思考過程の動的追跡 | ✓ |

**注**: PostgreSQL、GitHub、Slack、GitLab、Google Drive の参照実装はアーカイブされ、別リストに移行。

## M3. 我々のワークフローで使う MCP（閉域環境対応）

データを社外に出せない前提で厳選：

| 用途 | MCP 名 | 種別 | 推奨度 |
|---|---|---|---|
| **Gitea 連携**（必須） | [gitea/gitea-mcp](https://gitea.com/gitea/gitea-mcp) | 公式 | ★★★★★ |
| **PostgreSQL 参照**（任意） | `@modelcontextprotocol/server-postgres` | 公式 | ★★★★★ |
| **ファイルシステム**（任意） | `@modelcontextprotocol/server-filesystem` | 公式 | ★★★★☆ |
| **Git 操作**（任意） | 公式 Git MCP | 公式 | ★★★★☆ |
| **Playwright（E2E）**（任意） | 公式 Puppeteer MCP | 公式 | ★★★★★ |

## M4. 閉域環境で避けるもの

SaaS 前提のため、閉域環境では使えないか慎重な検討が必要：

| MCP | 理由 |
|---|---|
| Slack MCP | Slack 自体が SaaS（オンプレ Slack でなければ不可） |
| Confluence MCP | Atlassian Cloud 前提、オンプレ版は要検証 |
| Notion MCP | SaaS、データが Notion に送信される |
| Google Calendar MCP | Google アカウント前提 |

## M5. team-standards での共有戦略

### `.mcp.json` の配置
```
team-standards/
└── mcp/
    └── .mcp.json          # 公式推奨のプロジェクトスコープ設定
```

### `.mcp.json` の例
```json
{
  "mcpServers": {
    "gitea": {
      "command": "go",
      "args": ["run", "gitea.com/gitea/gitea-mcp@latest"],
      "env": {
        "GITEA_ACCESS_TOKEN": "${GITEA_TOKEN}",
        "GITEA_HOST": "${GITEA_HOST}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres", "${DB_URL}"]
    }
  }
}
```

### 認証情報管理（絶対ルール）
- **トークンは絶対に team-standards に commit しない**
- 各自の `.env.local` で管理（`.gitignore` に登録）
- `${ENV_VAR}` 形式で設定ファイルから参照

### スコープの使い分け
- **Managed**（Anthropic管理）= 閉域では使わない
- **Project**（`.mcp.json`）= チーム共有、必須のもの
- **User**（`~/.claude/mcp.json`）= 個人固有の設定

## M6. 自作 MCP（社内 API 用）

**難易度**:
- 低（1-2日）: Read-only DB wrapper、REST API ラッパー
- 中（3-5日）: 複雑な認可、監査ログ
- 高（1週間+）: ストリーミング、リアルタイム同期

**セキュリティ必須事項**:
1. **Read-only から始める**
2. **SQL/Command Injection 対策**（Zod 等でスキーマ検証）
3. **監査ログ**（全操作を記録）
4. **認可チェック**（ユーザー・スコープ分離）

**参考実装**: [FreeCodeCamp: Build MCP Servers for Internal Data](https://www.freecodecamp.org/news/how-to-build-mcp-servers-for-your-internal-data/)

## M7. コミュニティキュレーション

| リポジトリ | スター | 特徴 |
|---|---|---|
| [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) | 3.2k+ | 34カテゴリ・450+ |
| [tolkonepiu/best-of-mcp-servers](https://github.com/tolkonepiu/best-of-mcp-servers) | 800+ | 週次更新、ランキング付き |
| [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) | 公式 | 最新リスト |

---

# 第5部：team-standards リポジトリの完全な構造

調査結果を総合した推奨ディレクトリ構造：

```
team-standards/
│
├── README.md                       # このリポジトリの使い方
├── CLAUDE.md                       # 常に読まれる基本ルール (200行以内)
│
├── skills/                         # 呼び出し式の手順書
│   ├── implement-feature.md        # 機能追加の標準手順
│   ├── post-to-gitea-issue.md      # 壁打ちログを Issue にポスト (自作)
│   ├── review-my-changes.md        # セルフレビュー (拡張)
│   └── brainstorm-log-to-4items.md # 4項目テンプレ抽出 (自作)
│
├── agents/                         # 専門秘書 (VoltAgent からコピー)
│   ├── code-reviewer.md
│   ├── architect-reviewer.md
│   ├── security-auditor.md
│   ├── test-coverage-checker.md
│   ├── debugger.md
│   └── dependency-manager.md
│
├── hooks/                          # 自動化スクリプト (Node.js)
│   ├── save-transcript.mjs         # SessionEnd: 壁打ちログ保存
│   ├── lint-on-edit.mjs            # PostToolUse: 自動 lint/format
│   ├── bash-guard.mjs              # PreToolUse: 危険コマンドブロック
│   └── team-standards-pull.mjs     # SessionStart: 最新化
│
├── mcp/                            # 外部ツール連携
│   └── .mcp.json                   # Gitea, PostgreSQL 等の接続設定 (テンプレ)
│
├── .claude/
│   └── settings.json               # Hook 設定 (git commit する)
│
├── .env.example                    # トークン等のテンプレ (空値)
└── .gitignore                      # .env, .env.local, secrets 等
```

## 各ディレクトリに何を置くか

| ディレクトリ | 何を置く | Git 管理 |
|---|---|---|
| `CLAUDE.md` | チーム共通ルール・規約 | ✓ |
| `skills/` | 呼び出し式の手順 | ✓ |
| `agents/` | 専門秘書の定義 | ✓ |
| `hooks/` | 自動化スクリプト本体 | ✓ |
| `.claude/settings.json` | Hook の有効化設定 | ✓ |
| `mcp/.mcp.json` | MCP 接続設定（テンプレ） | ✓ |
| `.env` | 実際のトークン | ❌（gitignore） |
| `.claude/settings.local.json` | 個人の追加設定 | ❌（gitignore） |

---

# 第6部：MCP 導入前の必須セキュリティチェックリスト

**どの MCP サーバーも、導入前に必ず以下を確認すること。**

## □ 1. 配布元の確認
- [ ] Anthropic 公式 (`modelcontextprotocol/servers`) か？
- [ ] または配布元のベンダー自身（例: Gitea 公式、Notion 公式）か？
- [ ] コミュニティ実装の場合、GitHub スター数・最終コミット日・Issue 対応状況を確認したか？

## □ 2. CVE の確認
- [ ] [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) で該当 MCP が警告リストに入っていないか？
- [ ] GitHub の Security Advisories タブを確認したか？
- [ ] 検索エンジンで「<mcp名> CVE」「<mcp名> vulnerability」を確認したか？

## □ 3. 権限範囲の確認
- [ ] 読み取り専用で動かせるか？（書き込み権限は後から段階的に追加）
- [ ] ネットワークアクセス先を確認したか？（閉域で動くか）
- [ ] 必要以上のスコープ・権限を要求していないか？

## □ 4. トークン管理
- [ ] トークンは `.env` で管理され、`team-standards` に commit されないか？
- [ ] トークンの有効期限・ローテーション方針が決まっているか？
- [ ] トークンのスコープが最小権限になっているか？

## □ 5. 監査ログ
- [ ] MCP が何をしたかのログが残るか？
- [ ] 障害時のログが調査できるか？

## □ 6. コードレビュー
- [ ] ソースコードを実際に見たか？（特にコミュニティ MCP）
- [ ] 外部通信先がソースから分かるか？
- [ ] 怪しい依存パッケージが含まれていないか？

## □ 7. テスト運用
- [ ] 本番ではない環境で 1 週間試したか？
- [ ] 想定外の動作がないか？
- [ ] パフォーマンスが許容範囲か？

**一つでも ❌ があれば、導入見送りまたは保留。**

---

## Subagents / Hooks / MCP の参考 URL

### Subagents
- [Claude Code Subagents 公式](https://code.claude.com/docs/en/sub-agents)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [0xfurai/claude-code-subagents](https://github.com/0xfurai/claude-code-subagents)
- [wshobson/agents](https://github.com/wshobson/agents)
- [How and when to use subagents (Anthropic Blog)](https://claude.com/blog/subagents-in-claude-code)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)

### Hooks
- [Claude Code Hooks 公式](https://code.claude.com/docs/en/hooks)
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)
- [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)
- [Cross-Platform Hooks Guide](https://claudefa.st/blog/tools/hooks/cross-platform-hooks)
- [Hooks Automate Guide](https://code.claude.com/docs/en/hooks-guide)

### MCP
- [MCP 公式仕様](https://modelcontextprotocol.io/specification/2025-11-25)
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- [MCP Registry 公式](https://registry.modelcontextprotocol.io)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- [awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
- [State of MCP Security 2025](https://astrix.security/learn/blog/state-of-mcp-server-security-2025/)
- [Build MCP Servers for Internal Data](https://www.freecodecamp.org/news/how-to-build-mcp-servers-for-your-internal-data/)
