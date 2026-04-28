# Serendie Design System トラブルシューティング

Serendie利用時によく発生する問題と解決策。

---

## import / モジュール関連

### `Module not found: @serendie/serendie`

**原因**: パッケージ名が間違い。

**対応**:
```bash
npm uninstall @serendie/serendie
npm install @serendie/ui
```

`import` 文も修正：
```typescript
// ❌
import { Button } from '@serendie/serendie'
// ✅
import { Button } from '@serendie/ui'
```

### `has no exported member 'SomeIcon'`

**原因**: アイコン名が実在しない。

**対応**: `references/icons.md` の「よくある誤りと対応」を参照。または：

```bash
node --input-type=module -e "import('@serendie/symbols').then(m => console.log(Object.keys(m).sort().join('\n')))"
```

### `Cannot use import statement outside a module` / CJSエラー

**原因**: Serendie UIはESM専用（CJS非対応）。

**対応**:
- `package.json` に `"type": "module"` を追加、または
- モダンバンドラー（Vite, webpack 5+）を使用
- Node.jsでテストする場合は `.mjs` 拡張子、または `--experimental-vm-modules`

---

## スタイリング関連

### CSS変数が効かない（色が表示されない）

**原因1**: プレフィックスが間違っている

```css
/* ❌ 公式ドキュメントに書かれている形式（実ビルドには存在しない） */
background: var(--sd-system-color-impression-primary);

/* ✅ 実際のCSS変数名 */
background: var(--colors-sd-system-color-impression-primary);
```

**原因2**: `tokens.css` が読み込まれていない

`src/main.tsx` を確認：

```typescript
// 必ずこの順序
import '@serendie/design-token/tokens.css'
import '@serendie/ui/styles.css'
import './index.css'
```

**原因3**: package export pathから読み込んでいない

```typescript
// ❌ dist直接パス
import '@serendie/design-token/dist/tokens.css'
// ✅ package exports経由
import '@serendie/design-token/tokens.css'
```

### キャメルケース vs ケバブケース混同

Pandaがキャメルケースをケバブケースに変換する：

```
内部トークン:  sd.system.color.impression.onPrimary
CSS変数:      --colors-sd-system-color-impression-on-primary
                                                  ^^^^^^^^^^^
                                                  ケバブケース化
```

---

## テーマ関連

### テーマが切り替わらない

**チェック1**: `<html>` 要素の `data-panda-theme` 属性

```html
<!-- index.html -->
<html lang="ja" data-panda-theme="konjo">
```

**チェック2**: `@layer` 宣言が `index.css` の先頭にある

```css
@layer reset, base, tokens, recipes, utilities;

/* その後にカスタムスタイル */
```

**チェック3**: 動的切り替えコード

```typescript
document.documentElement.setAttribute('data-panda-theme', 'asagi')
```

### 特定のコンポーネントだけテーマが効かない

Ark UIのheadlessコンポーネントは propに渡されたstyleが優先。CSS変数を上書きしているインラインstyleを確認。

---

## コンポーネントAPI関連

### `Property 'variant' does not exist on Button`

**原因**: Buttonのpropは `styleType`（`variant` ではない）。

```tsx
// ❌
<Button variant="primary">
// ✅
<Button styleType="filled">
```

値のマッピング:
| 一般的な名前 | Serendie |
|--------------|----------|
| `primary` | `filled` |
| `secondary` | `outlined` |
| `text` | `ghost` |

### `CircularProgress is not exported`

**原因**: Serendie UIに `CircularProgress` は存在しない。

**対応**: `ProgressIndicatorIndeterminate` を使用：

```tsx
import { ProgressIndicatorIndeterminate } from '@serendie/ui'

<ProgressIndicatorIndeterminate type="circular" size="medium" />
```

### Selectの値が反映されない

**原因**: Ark UIベースのSelectは `value` / `onValueChange` が配列形式。

```tsx
// ❌
<Select value={selectedValue} onValueChange={(v) => setValue(v)} />

// ✅
<Select
  value={[selectedValue]}                       // 配列
  onValueChange={(d) => setValue(d.value[0])}  // d.value は配列
/>
```

### ModalDialogが閉じない

**原因**: `onOpenChange` を実装していない、または `onButtonClick` だけで閉じようとしている。

```tsx
<ModalDialog
  isOpen={open}
  onButtonClick={() => {
    handleSubmit()
    setOpen(false)   // submit時は明示的に閉じる
  }}
  onOpenChange={(d) => {
    if (!d.open) setOpen(false)   // 外側クリック・Escなどで閉じる
  }}
  ...
/>
```

---

## TypeScript関連

### `Cannot find module '@serendie/ui'` (TS2307)

**原因**: パッケージがインストールされていない、または `node_modules` が壊れている。

**対応**:
```bash
rm -rf node_modules package-lock.json
npm install
```

### JSON importのエラー (`Cannot find module '/xxx.json'`)

プロジェクトルートのJSONを import したい場合、絶対パス `/xxx.json` は TypeScript が解決できない。

**対応**: Viteの `import.meta.glob` を使う：

```typescript
const outputs = import.meta.glob('/amplify_outputs.json', { eager: true })
const data = outputs['/amplify_outputs.json'] as SomeType | undefined
```

---

## ビルド・バンドル関連

### バンドルサイズが大きい

**原因**: アイコンやコンポーネントを一括importしている。

**対応**: 必ず個別import：

```tsx
// ❌ 巨大なバンドル
import * as Symbols from '@serendie/symbols'

// ✅ Tree Shaking有効
import { SerendieSymbolHome, SerendieSymbolClose } from '@serendie/symbols'
```

### Panda CSSのビルドエラー

`panda.config.ts` の設定を確認：
- プリセットに `@serendie/ui/preset` が入っているか
- `include` パターンがsrcを含むか

---

## 診断用コマンド集

### 使用中のSerendieパッケージバージョン

```bash
npm ls @serendie/ui @serendie/symbols @serendie/design-token
```

### 実際のCSS変数を確認

```bash
grep -E "^\s+--colors-sd-" node_modules/@serendie/design-token/dist/tokens.css | head -30
```

### UIコンポーネントの一覧

```bash
node --input-type=module -e "import('@serendie/ui').then(m => console.log(Object.keys(m).sort().join('\n')))"
```

### アイコンの一覧

```bash
node --input-type=module -e "import('@serendie/symbols').then(m => console.log(Object.keys(m).sort().join('\n')))"
```
