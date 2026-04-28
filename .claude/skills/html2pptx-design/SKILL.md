---
name: html2pptx-design
description: "ピクセルパーフェクトなデザイン品質のPowerPointプレゼンテーションをHTML+CSS → Playwright screenshot → PPTX の3ステップで作成する。テキスト編集不要でデザイン優先のプレゼンを作るときに使用。トリガー: 「デザインの良いPP/スライドを作って」「プレゼン資料を作りたい」「〇〇の紹介スライドを作って」など、見栄えの良いPowerPoint作成を依頼されたとき。"
---

# HTML → Playwright → PPTX デザインスライド作成

HTMLとCSSでスライドを設計し、Playwrightでスクリーンショット→PPTXに変換するワークフロー。
テキスト編集は不要で、ビジュアル優先の高品質プレゼンを作成できる。

## ワークフロー概要

```
1. HTMLファイル設計 (slides.html)
       ↓
2. Playwright でスクリーンショット (1920×1080 PNG × N枚)
       ↓
3. python-pptx でPPTX化 (PNG画像をフルスライドで埋め込み)
```

## Step 1: slides.html の設計

### ファイル構造の基本

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>プレゼンタイトル</title>
<!-- Google Fontsを必ず読み込む -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* CSSをここに記述 */
</style>
</head>
<body>
<!-- スライド1 -->
<section class="slide" id="s1">...</section>
<!-- スライド2 -->
<section class="slide" id="s2">...</section>
<!-- ... -->
</body>
</html>
```

### 絶対に守るルール

- スライドは `<section class="slide" id="sN">` (N=1から連番)
- スライドサイズは **1920×1080px** 固定
- `body` は `background: #24324a; display: flex; flex-direction: column; align-items: center; gap: 32px;`
- CSS変数でカラーパレットを定義する (後でテーマ変更しやすくなる)

### カラーパレットの選択

コンテンツに合ったパレットを選ぶ。デフォルトはSerendie(紺+紫)。
詳細なCSSパターンは `references/css-patterns.md` を参照。

**よく使うパレット例:**
- Serendie Blue: `--primary: #174ECC; --accent: #8A42FF;`
- Deep Dark: `--primary: #0B2D7A; --accent: #8A42FF;`
- Green Tech: `--primary: #12A07F; --accent: #1E8FCC;`

### スライドの種類と選択

| スライド種別 | 使用場面 | CSSクラス |
|---|---|---|
| カバー | タイトル・表紙 | グラデーション背景 + `.cover-wrap` |
| チャプター | セクション区切り | `.ch-wrap` + 大きなタイトル |
| フィーチャー | 機能紹介（テキスト＋スクショ） | `.ft-layout` (grid 1:1.55) |
| ワンライナー | 価値提案・インパクト | `.one-liner` (中央揃え大文字) |
| リスト | 箇条書き説明 | `.blist` |
| サンキュー | 最終スライド | グラデーション背景 + `.ty-wrap` |

### スライドの数と構成

典型的な15〜20枚構成:
1. カバー (グラデーション背景)
2. ワンライナー (価値提案)
3. チャプター (セクション1)
4〜7. フィーチャースライド (機能紹介)
8. チャプター (セクション2)
9〜12. フィーチャースライド
13. まとめ
14. サンキュー

## Step 2: スクリーンショット変換

このスキルの `scripts/render_slides.py` を使用する。スキルのベースディレクトリはスキルロード時に表示される（例: `C:\Users\...\skills\html2pptx-design`）。

```bash
python "C:/Users/dw35816/.claude/skills/html2pptx-design/scripts/render_slides.py" \
  ./slides.html \
  ./output.pptx
```

スライド枚数を指定する場合（省略時は自動検出）:
```bash
python "C:/Users/dw35816/.claude/skills/html2pptx-design/scripts/render_slides.py" \
  ./slides.html ./output.pptx --total 15
```

スクリーンショットは `./slides-png/slide-01.png` 〜 に保存され、PPTXも自動で生成される。

### 依存関係の確認

```bash
pip install playwright python-pptx
python -m playwright install chromium
```

## Step 3: 確認と調整

1. 生成されたPPTXをPowerPointで開いて確認
2. テキストが見切れていないか、コントラストは十分か確認
3. 問題があればHTMLのCSSを修正して `render_slides.py` を再実行

## よくあるデザインパターン

詳細は `references/css-patterns.md` を参照。

### コンテンツスライドの共通ヘッダー

```html
<section class="slide" id="s2">
  <div class="header">
    <div class="title-wrap">
      <div class="bar"></div>
      <div><div class="t">スライドタイトル</div><div class="st">サブタイトル</div></div>
    </div>
    <div class="logo"><div class="dot"></div>APP NAME</div>
  </div>
  <div class="content">
    <!-- ここにコンテンツ -->
  </div>
  <div class="brandline"><span class="bl-dot"></span>AppName</div>
  <div class="pager">02 / 15</div>
</section>
```

### 画像の埋め込み

スクリーンショット等を表示する場合は `.shot` クラスで囲む:

```html
<div class="shot" style="flex:1;">
  <img src="../screenshots/screen.png" alt="">
</div>
```

## 設計上の注意点

- **Google Fonts使用**: ローカルフォントを使わず、Noto Sans JP + Interを使う
- **スライドはposition:relative + overflow:hidden**: 要素がはみ出しても切り取られる
- **テキストの最小サイズ**: 本文は16px以上、見出しは32px以上
- **スクリーンショット内の画像パス**: HTMLから見た相対パスで指定する
- **Playwrightフォント待機**: `await page.wait_for_timeout(1500)` でフォント読み込みを待機
