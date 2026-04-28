---
name: serendie-design
description: 三菱電機のSerendie Design System（@serendie/ui + @serendie/symbols + @serendie/design-token）でUIを実装するための汎用ガイドライン。公式リポジトリに基づくパッケージ名・全32コンポーネント・全92カラートークン・305+アイコンを網羅。
---

# Serendie Design System ガイドライン

三菱電機のSerendie Design Systemを使ってUIを実装するための汎用skillです。公式リポジトリ（`github.com/serendie`）の情報に基づき、実装でつまずきやすい点を優先して記載しています。公式ドキュメントやGitHub Org名 `serendie/serendie` と実際のnpmパッケージ名が異なる点に特に注意してください。

詳細な情報は `references/` の各ファイルを参照してください。

---

## 1. 必須事項（これだけは絶対に間違えない）

### 1.1 パッケージ名

| 用途 | パッケージ名 | 誤りやすい名前 |
|------|--------------|----------------|
| UIコンポーネント | `@serendie/ui` | ❌ `@serendie/serendie` |
| アイコン | `@serendie/symbols` | ❌ `@serendie/serendie-symbols` |
| デザイントークン | `@serendie/design-token` | - |

```bash
npm install @serendie/ui @serendie/symbols @serendie/design-token
```

### 1.2 CSS変数の命名規則

Panda CSSがプレフィックスを付与し、キャメルケース→ケバブケースに変換する：

```css
/* ✅ 正しい（実ビルドで使える） */
var(--colors-sd-system-color-impression-primary)
var(--colors-sd-system-color-impression-on-primary)
var(--colors-sd-system-color-component-outline-bright)

/* ❌ 間違い（公式ドキュメントで見かけるが実ビルドで存在しない） */
var(--sd-system-color-impression-primary)
var(--sd-system-color-impression-onPrimary)
```

### 1.3 CSS import順序

`src/main.tsx` での読み込み順序は固定：

```typescript
import '@serendie/design-token/tokens.css'   // 1. トークン
import '@serendie/ui/styles.css'             // 2. UI styles
import './index.css'                         // 3. プロジェクト固有
```

### 1.4 Panda CSS layer宣言

`src/index.css` の先頭に必須：

```css
@layer reset, base, tokens, recipes, utilities;
```

### 1.5 テーマ切り替え

`<html>` の `data-panda-theme` 属性で制御：

```html
<html lang="ja" data-panda-theme="konjo">
```

---

## 2. Foundation（技術基盤）

- **Ark UI**: 見た目を持たないheadless UIライブラリ。ロジック・アクセシビリティのみを提供し、スタイリングは利用側で行う
- **Panda CSS**: ビルド時にCSS-in-JSを静的CSSに変換するスタイリングライブラリ
- **ESMのみ**: CJSサポートなし。モダンバンドラー必須（Vite推奨）

### なぜCSS import順序が固定なのか

`@layer reset, base, tokens, recipes, utilities;` の順序はPanda CSSのカスケード優先度制御のため。`tokens` layerが `base`/`reset` より高優先度でUIコンポーネントに色を渡し、`utilities` が最上位で個別スタイルを上書きできる設計になっている。順序を逆にすると、UIコンポーネントがトークンの色を受け取れない、または上書きができなくなる。

---

## 3. 主要コンポーネント（クイックリファレンス）

詳細API仕様は `references/components.md` を参照。

### Button

```tsx
import { Button } from '@serendie/ui'

<Button styleType="filled" size="medium" type="submit">保存</Button>
```

- `styleType`: `"filled"` / `"outlined"` / `"ghost"` / `"rectangle"` （❌ `variant` ではない）
- `size`: `"small"` / `"medium"`

### IconButton

```tsx
import { IconButton } from '@serendie/ui'
import { SerendieSymbolClose } from '@serendie/symbols'

<IconButton
  shape="circle"
  styleType="ghost"
  icon={<SerendieSymbolClose width={20} height={20} />}
  aria-label="閉じる"
/>
```

### TextField / PasswordField / Select

```tsx
import { TextField, PasswordField, Select } from '@serendie/ui'

<TextField label="氏名" value={v} onChange={e => setV(e.target.value)} fullWidth required />
<PasswordField label="パスワード" value={p} onChange={e => setP(e.target.value)} fullWidth />
<Select
  label="言語"
  items={[{ label: '日本語', value: 'ja' }]}
  value={[lang]}                              // ← 配列で渡す
  onValueChange={(d) => setLang(d.value[0])}  // ← d.valueは配列
/>
```

### ModalDialog

```tsx
import { ModalDialog } from '@serendie/ui'

<ModalDialog
  isOpen={open}
  title="確認"
  submitButtonLabel="削除"
  cancelButtonLabel="キャンセル"
  onButtonClick={handleConfirm}
  onOpenChange={(d) => setOpen(d.open)}
>
  本当に削除しますか？
</ModalDialog>
```

### Loading

```tsx
import { ProgressIndicatorIndeterminate } from '@serendie/ui'

<ProgressIndicatorIndeterminate type="circular" size="medium" />
```

❌ `CircularProgress` は存在しない。

---

## 4. アイコン（`@serendie/symbols`）

全アイコンに **`SerendieSymbol`** プレフィックス：

```tsx
import { SerendieSymbolHome, SerendieSymbolPlus } from '@serendie/symbols'

<SerendieSymbolHome width={24} height={24} />
```

**想定と異なる名前があるので注意**：

| 期待される名前 | 実際の名前 |
|----------------|-----------|
| Chat | `SerendieSymbolChatRectangle` |
| Add | `SerendieSymbolPlus` |
| Category / Palette | `SerendieSymbolTag` |

詳細: `references/icons.md`

---

## 5. カラーテーマ

5つのテーマが利用可能：

- `konjo`（紺青 / ブルー）← デフォルト
- `asagi`（浅葱 / グリーン）
- `kurikawa`（栗皮 / イエロー）
- `sumire`（菫 / パープル）
- `tsutsuji`（躑躅 / ピンク）

色トークンの詳細は `references/colors-tokens.md`

---

## 6. アクセシビリティ & レイアウト原則

- **セマンティックHTML分離**: `<header>`（ブランド）+ `<aside>` + `<nav>`（リンクのみ）+ `<main>`
- **skip-link** 必須、`focus-visible` に4pxの主色リング
- **IconButton** には `aria-label` 必須
- **モノクロSVGアイコン** のみ使用（色付きアイコン禁止）
- **ハードコードされた色値を使用しない** → 必ずCSS変数

---

## 7. トラブルシューティング

import エラー・CSS変数の不具合・テーマが効かない等の症状と対処法は `references/troubleshooting.md` を参照（10以上の症状別診断コマンド付き）。

---

## 8. Claude への動作指示

UI実装時は**常に以下を遵守**：

1. パッケージ名は `@serendie/ui` / `@serendie/symbols` を使用する
2. Buttonには `styleType`（`variant` ではない）
3. CSS変数は `--colors-sd-system-color-*`（プレフィックス必須）
4. アイコンは `SerendieSymbol*` プレフィックス
5. ハードコードされた色・サイズを使わず、CSS変数/Design Tokens を使用
6. `<html data-panda-theme>` でテーマ切り替え
7. WCAG 2.2対応（skip-link, focus-visible, ARIA）
8. 不明な場合は `references/` を参照する、または `node_modules/@serendie/ui/` の型定義を確認する

---

## 9. 参照ファイル

| ファイル | 内容 |
|---------|------|
| `references/components.md` | 全コンポーネントAPI詳細 |
| `references/icons.md` | SerendieSymbol命名規則とよく使うアイコン一覧 |
| `references/colors-tokens.md` | CSS変数・カラートークン完全一覧 |
| `references/troubleshooting.md` | トラブルシューティング詳細 |

---

## 10. 公式リソース

- ガイドライン: https://serendie.design
- Storybook: https://storybook.serendie.design
- GitHub: https://github.com/serendie
