# Shin-sibainu/cc-secretary

- **URL**: https://github.com/Shin-sibainu/cc-secretary
- **著者**: Shin-sibainu
- **プラットフォーム**: GitHub
- **ライセンス**: MIT

## 概要

Claude Code用のパーソナル秘書プラグイン。ユーザーの役割や日常をヒアリングし、Markdownベースの管理フォルダを自動生成する秘書アシスタント。cc-companyの軽量版的な位置づけ。

## インストール方法

```
/plugin marketplace add Shin-sibainu/cc-secretary
/plugin install secretary@cc-secretary
```

## 主な機能

### 初回セットアップ（オンボーディング）

1. ユーザーの職業や役割をヒアリング
2. 日常のワークフローを聴取
3. 管理したい領域を選択
4. 役割に最適化されたフォルダ構成を自動生成

### 日常管理モード

- タスク追加・確認
- アイデア・リサーチのクイック記録
- メモをinboxにキャプチャ
- 週次レビューの自動生成
- ダッシュボード表示

## 管理コマンド

| コマンド | 機能 |
|---------|------|
| タスク追加 | TODOに項目追加 |
| 今日のタスク | 本日のタスク表示 |
| メモ | inboxへ記録 |
| 週次レビュー | レビュー自動生成 |

## 対応カテゴリ

todos, ideas, research, knowledge, content-plan, meetings, clients, journal, reading-list, debugging, projects, finances, inbox, reviews（常に含まれる）

## ロール別プリセット

| ロール | デフォルトカテゴリ |
|--------|------------------|
| 開発者 | todos, projects, ideas, knowledge, debugging |
| クリエイター | todos, content-plan, ideas, research |
| フリーランス | todos, clients, projects, ideas, research |

## ファイル構成

```
plugins/secretary/
├── .claude-plugin/plugin.json
└── skills/secretary/
    ├── SKILL.md
    └── references/templates.md
```

## 技術スタック

- Claude Code用プラグイン
- Markdown形式の管理システム

## cc-companyとの違い

| 観点 | cc-secretary | cc-company |
|------|-------------|------------|
| 規模 | 個人向け軽量 | 組織向けフル機能 |
| 部署概念 | なし（カテゴリ） | あり（秘書室、PM等） |
| オンボーディング | シンプル | 詳細（部署選択、組織図等） |
| 対象ユーザー | 個人の生産性向上 | チーム・組織の管理 |
