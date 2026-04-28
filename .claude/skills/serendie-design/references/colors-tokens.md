# Serendie Design Tokens / CSS変数リファレンス

Serendie Design Systemのカラートークン・CSS変数の完全一覧。公式 `@serendie/design-token` の `tokens/system/` 基準。

---

## 命名規則の重要点

Panda CSSがビルド時にトークンを処理し、**プレフィックスとケバブケース変換** を行う：

```
元のトークン名:  sd.system.color.impression.onPrimary
↓ Pandaが処理
実CSS変数名:    --colors-sd-system-color-impression-on-primary
                ^^^^^^^                      ^^^^^^^^^^^^
                プレフィックス              ケバブケース化
```

**結論**:
- ✅ 実装で使用: `var(--colors-sd-system-color-impression-on-primary)`
- ❌ ドキュメントに書かれている形式: `var(--sd-system-color-impression-onPrimary)`

---

## カラーテーマ

5つのカラーテーマ。`<html data-panda-theme="...">` で切り替え：

| テーマ | 意味 | ベース色 |
|--------|------|---------|
| `konjo` | 紺青 | ブルー（デフォルト） |
| `asagi` | 浅葱 | グリーン |
| `kurikawa` | 栗皮 | イエロー |
| `sumire` | 菫 | パープル |
| `tsutsuji` | 躑躅 | ピンク |

各テーマは同じトークン名を共有し、色値だけが変わる。

---

## カラートークン全一覧（92個）

全テーマで **同じトークン名** が使われ、`data-panda-theme` 属性の値により色が切り替わる。以下はKonjoテーマでの代表値。

### Impression Colors（ブランド・セマンティック）— 30個

すべて `--colors-sd-system-color-impression-*` プレフィックス。

**Primary系:**
- `primary` / `on-primary` / `primary-container` / `on-primary-container`

**Secondary系:**
- `secondary` / `on-secondary` / `secondary-container` / `on-secondary-container`

**Tertiary系:**
- `tertiary` / `on-tertiary` / `tertiary-container` / `on-tertiary-container`

**Notice（警告）系:**
- `notice` / `on-notice` / `notice-container` / `on-notice-container`
- `notice-container-variant` / `on-notice-container-variant`

**Negative（エラー）系:**
- `negative` / `on-negative` / `negative-container` / `on-negative-container`
- `negative-container-variant` / `on-negative-container-variant`

**Positive（成功）系:**
- `positive` / `on-positive` / `positive-container` / `on-positive-container`
- `positive-container-variant` / `on-positive-container-variant`

**Konjoテーマの代表値:**
| トークン | 値 |
|---------|---|
| `impression-primary` | `#0353AA` (Blue 700) |
| `impression-on-primary` | `#FFFFFF` |
| `impression-secondary` | `#C0CFFD` (Blue 300) |
| `impression-tertiary` | `#EFF2FC` (Blue 100) |
| `impression-positive` | `#2EAB80` (Green 500) |
| `impression-negative` | `#D00138` (Red 600) |
| `impression-notice` | `#EDD857` (Yellow 300) |

他テーマ（asagi/kurikawa/sumire/tsutsuji/konjo-dark）は同じトークン名で色値が異なる。

### Component Colors（UI要素）— 15個

すべて `--colors-sd-system-color-component-*` プレフィックス。

| トークン | 用途 |
|----------|------|
| `surface` | 背景（メイン・カードなど） |
| `on-surface` | 本文テキスト |
| `on-surface-variant` | セカンダリテキスト |
| `surface-dim` | 控えめな背景 |
| `surface-bright` | 明るい背景 |
| `surface-container` | コンテナ背景 |
| `surface-container-bright` | 明るめコンテナ |
| `surface-container-dim` | 薄めコンテナ（Hover面等） |
| `outline` | 強調outline |
| `outline-bright` | 明るいoutline（区切り線） |
| `outline-dim` | 薄いoutline |
| `scrim` | スクリム（モーダル背景の覆い） |
| `inverse-surface` | 反転サーフェス |
| `inverse-on-surface` | 反転サーフェス上のテキスト |
| `inverse-primary` | 反転時のプライマリ |

### Interaction Colors（状態表現）— 7個

すべて `--colors-sd-system-color-interaction-*` プレフィックス。

| トークン | 用途 |
|----------|------|
| `disabled` | 無効状態の背景 |
| `disabled-on-surface` | 無効状態のテキスト |
| `selected` | 選択状態の背景 |
| `selected-surface` | 選択状態のサーフェス |
| `hovered` | Hover時（標準） |
| `hovered-variant` | Hover時（控えめ） |
| `hovered-on-primary` | Primary要素のHover |

### Chart Colors（グラフ用）— 40個

すべて `--colors-sd-system-color-chart-mark-*` プレフィックス。グラフの系列色として連番で用意されている。

- `primary.01` 〜 `primary.06`（計6色）
- `positive.01` 〜 `positive.06`
- `negative.01` 〜 `negative.06`
- `notice.01` 〜 `notice.06`
- `multi.01` 〜 `multi.16`（多系列用、16色）

---

## 使用例

### ボタン・プライマリ色

```css
.primary-action {
  background: var(--colors-sd-system-color-impression-primary);
  color: var(--colors-sd-system-color-impression-on-primary);
}
```

### フォーカスリング（WCAG 2.2対応）

```css
:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--colors-sd-system-color-component-surface),
    0 0 0 4px var(--colors-sd-system-color-impression-primary);
}
```

### ヘッダー・区切り線

```css
header {
  background: var(--colors-sd-system-color-component-surface);
  border-bottom: 1px solid var(--colors-sd-system-color-component-outline-bright);
}
```

### ナビゲーション（通常・Hover・選択）

```css
nav a {
  color: var(--colors-sd-system-color-component-on-surface);
}

nav a:hover {
  background: var(--colors-sd-system-color-interaction-hovered-variant);
}

nav a[aria-current="page"] {
  background: var(--colors-sd-system-color-interaction-selected);
  color: var(--colors-sd-system-color-impression-primary);
}
```

### エラー通知

```css
.error-banner {
  background: var(--colors-sd-system-color-impression-negative-container-variant);
  color: var(--colors-sd-system-color-impression-negative);
}
```

### 成功通知

```css
.success-banner {
  background: var(--colors-sd-system-color-impression-positive-container-variant);
  color: var(--colors-sd-system-color-impression-positive);
}
```

### 警告通知

```css
.notice-banner {
  background: var(--colors-sd-system-color-impression-notice-container-variant);
  color: var(--colors-sd-system-color-impression-notice);
}
```

---

## TypeScript からのトークン参照

`@serendie/design-token` には TS トークンも含まれる（CSS変数と併用）：

```typescript
import { tokens } from '@serendie/design-token'

// デザインtoken object（CSS変数名と対応）
const primaryColor = tokens.color.primary
```

ただし通常はCSS変数経由での使用が推奨（テーマ切り替えが動的に効くため）。

---

## トークン名の確認方法

### 方法1: `node_modules` のCSS変数を確認

```bash
cat node_modules/@serendie/design-token/dist/tokens.css | grep "impression-primary"
```

### 方法2: ブラウザDevToolsで確認

1. `<html>` 要素を選択
2. Computed stylesで `--colors-` で検索

### 方法3: プロジェクトに `.tmp/serendie-ref/` を作ってコピー

```bash
cp -r node_modules/@serendie/design-token/dist .tmp/serendie-ref/
```

参照ファイルとしてコミットせずに保持すると便利。

---

## タイポグラフィトークン

フォント系のトークン（`--fontFamilies-`, `--fontSizes-`, `--lineHeights-`, `--fontWeights-`）もPandaプレフィックスで展開される。

```css
.body-text {
  font-family: var(--fontFamilies-sd-reference-typography-font-family-primary);
  font-size: var(--fontSizes-sd-system-typography-body-medium-font-size);
  line-height: var(--lineHeights-sd-system-typography-body-medium-line-height);
  font-weight: var(--fontWeights-sd-reference-typography-font-weight-regular);
}

.heading-large {
  font-size: var(--fontSizes-sd-system-typography-headline-large-font-size);
  font-weight: var(--fontWeights-sd-reference-typography-font-weight-bold);
}
```

実トークン名はバージョンで変動するため、`tokens.css` を参照。

---

## スペーシングトークン

8pxベースのスペーシングトークンが `--spacing-*` として提供される。ハードコード値（`16px`等）の代わりに使用する。

```css
.card {
  padding: var(--spacing-sd-reference-dimension-scale-4);       /* 例: 16px相当 */
  gap: var(--spacing-sd-reference-dimension-scale-2);           /* 例: 8px相当 */
  margin-bottom: var(--spacing-sd-reference-dimension-scale-6); /* 例: 24px相当 */
}
```

---

## 半径（Radius）・影（Shadow）

角丸や影も同様にトークン化されている：

```css
.button {
  border-radius: var(--radii-sd-reference-dimension-radius-medium);
  box-shadow: var(--shadows-sd-system-elevation-level-2);
}
```
