# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリの性質

このリポジトリは現時点では**実装コードを持たない設計・企画段階**のプロジェクトである。`.tmp/` に共同開発プラットフォーム（AI駆動型チーム開発基盤「dx-portal」）の設計メモ、機能リスト、アーキテクチャ図、研究ノート、スライド生成スクリプト（Python / python-pptx）が蓄積されている。ソースコード、パッケージマニフェスト（package.json 等）、ビルド設定、テスト基盤はまだ存在しない。

新たに実装を始める場合は、**まず `.tmp/` の以下を読んでから着手する**：

- `.tmp/architecture-overview.md` — 全体構成（dx-brain / dx-portal / プロジェクトリポの3層、秘書・スキル・データ層の分離、既知の問題点4つ）
- `.tmp/feature-list.md` — 欲しい機能19項目 + 秘書の知識3層構造（チーム共有 / 匿名化ナレッジ / 個人層）
- `.tmp/collective-intelligence-direction.md` — 集合知の方向性
- `.tmp/skills-inventory.md`, `.tmp/claude_code_skills_research.md` — Claude Code スキルの調査
- `.tmp/CLAUDE-md-initial-sample.md` — チーム共通 CLAUDE.md の雛形（別リポ `team-standards` 用、30行→200行に育てる想定）
- `.tmp/01_*.md`〜`.tmp/06_*.md` — 参考プロジェクト調査（`sample_urls.txt` の URL 1〜6 に対応）

## アーキテクチャ上の重要な前提

設計上、以下の構造で動く想定になっている（まだ実装されていない）：

- **dx-portal（このリポ）** = チーム共有のスキル・エージェント・ワークフロー + チームデータ（`company-data/`）を置く予定
- **dx-brain** = 各メンバーの個人リポ（private、思考の蓄積）
- **各プロジェクトリポ** = アプリコード + dx-portal の reusable workflow を呼び出す
- **`/company` コマンド（秘書）** が唯一の窓口で、入力を個人/チーム/プロジェクトに振り分ける
- symlink で `~/.claude/skills/company` → `dx-portal/skills/company` を張って全プロジェクトから参照する

`.tmp/architecture-overview.md` の「5. 問題点」で既知の課題4つ（コード/データ混在、同時編集コンフリクト、Windows symlink 制約、private 間 reusable workflow 制約）が整理されている。**これらは未解決なので、実装方針を決める前に必ず参照する。**

## 実行環境

- OS: Windows 11（bash シェル使用、パスは forward slash 推奨）
- `.tmp/build-*.py` は python-pptx を使う PPTX 生成スクリプト。`python build-team-slides-v2.py` のように直接実行する想定。
- 出力される `.pptx` / `ai-collab-unpacked/` / `v2-check/` はスクリプトの生成物。

## 作業上の注意

- `.tmp/` は設計メモの保管場所であり、ユーザー CLAUDE.md の指示通り「設計の一時メモは `.tmp/` に markdown で保存」の運用が既に行われている。新しい設計ノートもここに置く。
- 実装段階に入る場合は、ユーザー CLAUDE.md の **Specification-Driven Development**（`/requirements` → `/design` → `/tasks` → 実装）に従う。
- 参考 URL は `sample_urls.txt` に集約されている。
