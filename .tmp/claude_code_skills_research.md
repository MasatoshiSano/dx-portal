# Claude Code Skills / Plugins 調査レポート
日時: 2026-04-10

## 調査範囲
- awesome-claude-code リポジトリ群
- GitHub トレンド（最近3-6ヶ月）
- Zenn/Qiita 記事
- obra/superpowers プロジェクト
- Anthropic 公式プラグイン

---

## 1. 強くおすすめしたい Skill（用途別）

### 1.1 壁打ち/ブレインストーミング用
**Superpowers: Brainstorming** (obra/superpowers の一部)
- GitHub: https://github.com/obra/superpowers
- Stars: 144,000
- 最終更新: 2026-03-31
- 用途: 設計議論のサポート、アイデア整理、設計の視覚化
- 特徴: 粗い考えを詳細な仕様に変換、複数案を並列提示、セクション単位で検証

**Official Frontend Design Skill** (Anthropic)
- URL: https://claude.com/plugins/frontend-design
- インストール数: 277,000+ (2026年3月時点)
- 用途: UI/UXデザイン議論、ブランド定義
- 特徴: bold aesthetic choices を強制、typography/animation の具体化

### 1.2 コードレビュー用
**Superpowers: Requesting Code Review**
- 同上（obra/superpowers の一部）
- 用途: PR レビュー、セキュリティ確認、アーキテクチャ検証
- 特徴: 実装計画との符合性チェック → コード品質チェック（2段階）

**Code Review Plugin** (Anthropic Official)
- URL: https://claude.com/plugins/code-review
- 用途: 自動コードレビュー、confidence-based filtering
- 特徴: 専門化された subagent による多角的レビュー

### 1.3 TDD/テスト生成用
**Superpowers: Test-Driven-Development**
- 同上（obra/superpowers の一部）
- 用途: テストファースト開発の強制
- 特徴: RED-GREEN-REFACTOR サイクルの厳格な実行
  - Step 1: failing test を先に書く
  - Step 2: 実行して fail を確認
  - Step 3: minimal code で pass させる
  - Step 4: refactor

### 1.4 CLAUDE.md 管理用
**CLAUDE.md Management** (Anthropic Official)
- URL: https://claude.com/plugins/claude-md-management
- GitHub: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-md-management
- 用途: CLAUDE.md の品質監査、更新支援
- 特徴: 
  - stale commands の検出
  - missing dependencies の洗い出し
  - architecture documentation の検証
  - quality score の生成

**claude-config-doctor** (tyabu12)
- URL: https://github.com/tyabu12/claude-config-doctor
- 用途: 設定ファイルの semantic conflict 検出
- 特徴: CLAUDE.md, rules, commands, hooks, settings.json を横断的に検証

### 1.5 デバッグ/根本原因分析用
**Superpowers: Systematic Debugging**
- 同上（obra/superpowers の一部）
- 用途: 本質的な問題解決
- 特徴: 
  - "NO FIXES WITHOUT ROOT CAUSE FIRST" の厳格適用
  - 4フェーズ: root cause investigation → pattern analysis → hypothesis testing → implementation
  - 実績: ~95% first-time fix rate vs ~40% ad-hoc

---

## 2. 著名な Skill 集リポジトリ

### メジャーな Awesome リポジトリ群
1. **hesreallyhim/awesome-claude-code**
   - URL: https://github.com/hesreallyhim/awesome-claude-code
   - 特徴: skills, hooks, slash-commands, agent orchestrators, applications を網羅
   - 更新: active

2. **travisvn/awesome-claude-skills**
   - URL: https://github.com/travisvn/awesome-claude-skills
   - 特徴: Claude Code 特化、community-driven

3. **karanb192/awesome-claude-skills**
   - URL: https://github.com/karanb192/awesome-claude-skills
   - 説明: "50+ verified Awesome Claude Skills"
   - 特徴: TDD, debugging, git workflows, document processing

4. **VoltAgent/awesome-agent-skills**
   - URL: https://github.com/VoltAgent/awesome-agent-skills
   - 説明: "1000+ agent skills" + Codex, Gemini CLI, Cursor との互換性

5. **sickn33/antigravity-awesome-skills**
   - URL: https://github.com/sickn33/antigravity-awesome-skills
   - 説明: "1370+ installable skills" + CLI installer

### Superpowers 関連
- **obra/superpowers-skills**: Community-editable skills library
  - URL: https://github.com/obra/superpowers-skills
- **obra/superpowers-lab**: Experimental skills
  - URL: https://github.com/obra/superpowers-lab

### Anthropic 公式
- **anthropics/claude-plugins-official**
  - URL: https://github.com/anthropics/claude-plugins-official

---

## 3. Gitea 統合周辺（チームワークフロー対応）

**Gitea MCP Server**
- 説明: "Model Context Protocol" によって Gitea を Claude Code から natural language で操作可能
- 用途: PR review, issue management, release handling
- 参考: https://about.gitea.com/resources/tutorials/gitea-mcp-server

**claude-code-gitea-action**
- URL: https://github.com/markwylde/claude-code-gitea-action
- 用途: Gitea インスタンスへの統合
- 制限: formal Gitea PR reviews の提出は不可（セキュリティ理由）

**Gitea Workflow Manager Skill**
- URL: https://mcpmarket.com/tools/skills/gitea-workflow-manager
- 用途: gitea-mcp + tea CLI による包括的ワークフロー

---

## 4. 「評価は分かれるが試す価値あり」なもの

**claude-code-showcase** (ChrisWiles)
- URL: https://github.com/ChrisWiles/claude-code-showcase
- 特徴: systematic-debugging など個別 skill の実装例
- 評価: Stars 多くはないが、実装テンプレートとして有用

**claude-code-ultimate-guide** (FlorianBruniaux)
- URL: https://github.com/FlorianBruniaux/claude-code-ultimate-guide
- 説明: beginner → power user への extensive documentation
- 評価: educational価値が高い、production-ready templates

**claude-code-workflows** (shinpr)
- URL: https://github.com/shinpr/claude-code-workflows
- 説明: "Production-ready development workflows"
- 特徴: specialized AI agents による workflow 実装

---

## 5. 調査して「ダメ」と分かったもの

### 課題のある領域
1. **スキル品質の低下**
   - 73% of 214 community Claude skills scored below 60/100 (2026 audit)
   - 大多数が silent failure

2. **GitHub Actions / Gitea Actions の制限**
   - claude-code-gitea-action は formal PR reviews を submit できない
   - Gitea にはまだ first-class Claude Code integration がない
   - tea CLI 経由の workaround が一般的

3. **.claude/commands/ の廃止予定**
   - 2026年初頭に .claude/skills/ に統一（2025年末に完了）
   - legacy commands への migration が必須
   - URL: https://github.com/anthropics/claude-code/issues/37447

### メンテナンス停止の例
- 明確に「廃止」と判定されたスキルはない
- ただし、個人配布の skill は maintenance が停止している可能性がある
  - GitHub の last commit を常に確認推奨

---

## 6. Zenn/Qiita 推奨記事

1. https://zenn.dev/cureapp/articles/fd00f58b065c7a
   - カスタムスラッシュコマンド → スキルへの migration

2. https://zenn.dev/long910/articles/2026-02-23-claude-code-skills
   - Claude Code のスキル作成方法

3. https://qiita.com/daishiro_jp/items/9e5caa569f0405b90841
   - Skill と Custom Slash Command の使い分け完全ガイド

4. https://zenn.dev/tmasuyama1114/articles/claude_code_best_practice_guide
   - Anthropic 公開のベストプラクティス解説

---

## 推奨インストール順序（開発チーム向け）

1. `/plugin install superpowers@claude-plugins-official`
   - brainstorming, TDD, code review, systematic debugging をカバー

2. `/plugin install code-review@claude-plugins-official`
   - Superpowers の code-review と相補

3. `/plugin install frontend-design@claude-plugins-official`
   - UI 設計議論用

4. `/plugin install claude-md-management@claude-plugins-official`
   - CLAUDE.md の lifecycle management

5. Gitea MCP Server のセットアップ（.claude/mcp.json）
   - チーム内の issue → PR → review フロー自動化用

---

## 注記
- 本調査は 2026-04-10 時点の情報
- GitHub Stars 数は参考程度（メンテナンス活動と相関あり）
- Superpowers (obra/superpowers) が最も包括的・活発
- Anthropic 公式プラグインの品質と安定性が最高
