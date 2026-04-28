# Serendie UI コンポーネント詳細API

`@serendie/ui` の全コンポーネントと、頻出コンポーネントの詳細API仕様。

---

## Button

```tsx
import { Button } from '@serendie/ui'

<Button styleType="filled" size="medium" type="submit" disabled={loading}>
  保存
</Button>
```

| Prop | 型 | 備考 |
|------|-----|------|
| `styleType` | `"filled"` \| `"outlined"` \| `"ghost"` \| `"rectangle"` | ❌ `variant` ではない |
| `size` | `"small"` \| `"medium"` | `"large"` は無い |
| `type` | `"submit"` \| `"button"` \| `"reset"` | HTML標準 |
| `disabled` | `boolean` | |
| `onClick` | `(e) => void` | |
| `style` | `CSSProperties` | インラインスタイル（幅指定など） |

**注意**: 全幅にしたい場合は `style={{ width: '100%' }}` を使用する（`fullWidth` propは無い）。

---

## IconButton

```tsx
import { IconButton } from '@serendie/ui'
import { SerendieSymbolLogout } from '@serendie/symbols'

<IconButton
  shape="circle"
  styleType="ghost"
  size="small"
  icon={<SerendieSymbolLogout width={20} height={20} />}
  onClick={handleLogout}
  aria-label="ログアウト"
/>
```

| Prop | 型 | 必須 |
|------|-----|------|
| `shape` | `"circle"` \| `"rectangle"` | ✅ |
| `icon` | `ReactElement` | ✅ |
| `styleType` | Button同様 | - |
| `size` | Button同様 | - |
| `aria-label` | `string` | ✅（アクセシビリティ） |

---

## TextField

```tsx
import { TextField } from '@serendie/ui'

<TextField
  label="メールアドレス"
  type="email"
  name="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  placeholder="example@company.com"
  autoComplete="email"
  required
  fullWidth
  disabled={isSubmitting}
/>
```

| Prop | 型 | 備考 |
|------|-----|------|
| `label` | `string` | ラベル表示 |
| `type` | HTML input type | `"email"`, `"text"`, `"number"` 等 |
| `value` | `string` | 制御コンポーネント |
| `onChange` | `(e: ChangeEvent) => void` | |
| `placeholder` | `string` | |
| `required` | `boolean` | |
| `disabled` | `boolean` | |
| `fullWidth` | `boolean` | 全幅表示 |
| `name` | `string` | フォーム名 |
| `autoComplete` | `string` | HTML標準 |
| `error` | `boolean \| string` | エラー状態（要確認） |

---

## PasswordField

パスワード入力専用。表示/非表示トグル付き。

```tsx
import { PasswordField } from '@serendie/ui'

<PasswordField
  label="パスワード"
  name="password"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  autoComplete="current-password"
  required
  fullWidth
  disabled={isSubmitting}
/>
```

TextFieldとほぼ同じAPI、ただし `type` は自動で `"password"`。

---

## Select

```tsx
import { Select } from '@serendie/ui'

const OPTIONS = [
  { label: '日本語', value: 'ja' },
  { label: 'English', value: 'en' },
]

<Select
  label="言語"
  name="language"
  items={OPTIONS}
  value={[selectedValue]}                        // ← 配列で渡す
  onValueChange={(detail) => setValue(detail.value[0])}  // ← detail.value は配列
  disabled={isSaving}
/>
```

| Prop | 型 | 備考 |
|------|-----|------|
| `items` | `{ label: string; value: string }[]` | オプション配列 |
| `value` | `string[]` | **配列で渡す** (単一選択でも) |
| `onValueChange` | `(detail: { value: string[] }) => void` | **`detail.value` は配列** |
| `label` | `string` | |
| `name` | `string` | |
| `disabled` | `boolean` | |

**重要**: Ark UIベースのため `value` / `onValueChange` が配列形式。単一選択でも `value={[x]}` が必要。

---

## ModalDialog

```tsx
import { ModalDialog } from '@serendie/ui'

<ModalDialog
  isOpen={open}
  title="確認"
  submitButtonLabel="削除"
  cancelButtonLabel="キャンセル"
  onButtonClick={() => {
    handleDelete()
    setOpen(false)
  }}
  onOpenChange={(details) => {
    if (!details.open) setOpen(false)
  }}
>
  <p>本当に削除しますか？</p>
</ModalDialog>
```

| Prop | 型 | 備考 |
|------|-----|------|
| `isOpen` | `boolean` | |
| `title` | `string` | ダイアログタイトル |
| `submitButtonLabel` | `string` | 送信ボタン |
| `cancelButtonLabel` | `string` | キャンセルボタン |
| `onButtonClick` | `() => void` | submit時のみ呼ばれる |
| `onOpenChange` | `(details: { open: boolean }) => void` | 閉じる検出 |
| `children` | `ReactNode` | 本文 |

**閉じる処理**: `onOpenChange` で `!details.open` を検知してstate更新する。

---

## ProgressIndicatorIndeterminate

ローディング表示。**`CircularProgress` は存在しない**ので必ずこれを使用する。

```tsx
import { ProgressIndicatorIndeterminate } from '@serendie/ui'

<ProgressIndicatorIndeterminate type="circular" size="medium" />
<ProgressIndicatorIndeterminate type="linear" size="small" />
```

| Prop | 値 |
|------|-----|
| `type` | `"circular"` \| `"linear"` |
| `size` | `"small"` \| `"medium"` \| `"large"` |

---

## 全コンポーネント一覧（32個）

`@serendie/ui` の全コンポーネント（`serendie/serendie` リポジトリの `src/components/` 基準）。上記で詳細API記載済みは ✅ マーク。

### フォーム入力
- ✅ `TextField` — 一行テキスト入力
- ✅ `PasswordField` — パスワード入力（表示切替付き）
- `TextArea` — 複数行テキスト
- ✅ `Select` — セレクトボックス
- `DatePicker` — 日付選択
- `Search` — 検索フィールド
- `CheckBox` — チェックボックス
- `RadioButton` — ラジオボタン
- `Switch` — オン/オフトグル
- `ChoiceBox` — 選択肢カード

### ボタン・アクション
- ✅ `Button` — 標準ボタン
- ✅ `IconButton` — アイコンのみボタン
- `DropdownMenu` — ドロップダウンメニュー

### ナビゲーション
- `TopAppBar` — トップアプリバー
- `BottomNavigation` — ボトムナビゲーション
- `Drawer` — サイドドロワー
- `Tabs` — タブ切替
- `Pagination` — ページネーション

### フィードバック・オーバーレイ
- ✅ `ModalDialog` — モーダルダイアログ
- `Toast` — 一時通知
- `Banner` — ページ内通知バナー
- `Tooltip` — ツールチップ
- ✅ `ProgressIndicator` / `ProgressIndicatorIndeterminate` — 進捗表示
- `NotificationBadge` — 通知バッジ

### 表示・データ
- `DataTable` — ソート・ページング付き表
- `List` — リスト表示
- `Chart` — チャート
- `DashboardWidget` — ダッシュボード用ウィジェット
- `Accordion` — アコーディオン
- `Avatar` — アバター画像
- `Badge` — バッジラベル
- `Divider` — 区切り線

### ⚠ 存在しないコンポーネント（よくある誤解）

`@serendie/ui` に **含まれていない** ので、類似機能で代替：

| 想定される名前 | 代替 |
|----------------|------|
| `Card` | `DashboardWidget` またはPanda CSSで独自実装 |
| `Chip` | `Badge` または `ChoiceBox` |
| `Breadcrumb` | 独自実装 or 別ライブラリ |

**詳細確認方法**:
1. 公式GitHub（最新反映・インストール不要）:
   ```bash
   gh api "repos/serendie/serendie/contents/src/components?per_page=200" --jq '.[] | select(.type=="dir") | .name'
   ```
2. Storybook: https://storybook.serendie.design
3. ローカル型定義: `cat node_modules/@serendie/ui/dist/*.d.ts`
4. Node.js 列挙: `node --input-type=module -e "import('@serendie/ui').then(m => console.log(Object.keys(m).sort()))"`

---

## 典型的な実装パターン

### 確認ダイアログラッパー

```tsx
import { ModalDialog } from '@serendie/ui'

interface ConfirmDialogProps {
  isOpen: boolean
  title: string
  message: string
  onConfirm: () => void
  onCancel: () => void
}

export function ConfirmDialog({ isOpen, title, message, onConfirm, onCancel }: ConfirmDialogProps) {
  return (
    <ModalDialog
      isOpen={isOpen}
      title={title}
      submitButtonLabel="OK"
      cancelButtonLabel="キャンセル"
      onButtonClick={onConfirm}
      onOpenChange={(d) => { if (!d.open) onCancel() }}
    >
      <p style={{ fontSize: '14px' }}>{message}</p>
    </ModalDialog>
  )
}
```

### ローディングスピナーラッパー

```tsx
import { ProgressIndicatorIndeterminate } from '@serendie/ui'

export function LoadingSpinner({ size = 'medium' }: { size?: 'small' | 'medium' | 'large' }) {
  return (
    <div role="status" aria-label="読み込み中">
      <ProgressIndicatorIndeterminate type="circular" size={size} />
    </div>
  )
}
```

### トップバー with IconButton

```tsx
import { IconButton } from '@serendie/ui'
import { SerendieSymbolChatRectangle, SerendieSymbolLogout } from '@serendie/symbols'

<header className="top-bar">
  <Link to="/" aria-label="ホーム">
    <SerendieSymbolChatRectangle width={24} height={24} />
    <span>Chat Tracker</span>
  </Link>
  <IconButton
    shape="circle"
    styleType="ghost"
    size="small"
    icon={<SerendieSymbolLogout width={20} height={20} />}
    onClick={signOut}
    aria-label="ログアウト"
  />
</header>
```

### サイドバーナビゲーション（アイコン付きリンク）

セマンティックHTML（`<aside>` + `<nav>` + セクション分け）+ アイコン付きリンクの実装例：

```tsx
import { Link, useLocation } from 'react-router'
import {
  SerendieSymbolPlus,
  SerendieSymbolHistory,
  SerendieSymbolFolder,
  SerendieSymbolTag,
} from '@serendie/symbols'

const NAV_SECTIONS = [
  {
    label: 'チャット',
    items: [
      { path: '/chat', label: '新しいチャット', icon: SerendieSymbolPlus },
      { path: '/history', label: 'チャット履歴', icon: SerendieSymbolHistory },
    ],
  },
  {
    label: 'データ',
    items: [
      { path: '/data', label: '保存データ', icon: SerendieSymbolFolder },
      { path: '/themes', label: 'テーマ管理', icon: SerendieSymbolTag },
    ],
  },
]

export function Sidebar() {
  const { pathname } = useLocation()
  return (
    <aside className="sidebar">
      <nav aria-label="メインナビゲーション">
        {NAV_SECTIONS.map((section) => (
          <section key={section.label} aria-label={section.label}>
            <h2 className="nav-section-label">{section.label}</h2>
            <ul>
              {section.items.map(({ path, label, icon: Icon }) => (
                <li key={path}>
                  <Link
                    to={path}
                    aria-current={pathname === path ? 'page' : undefined}
                  >
                    <Icon width={20} height={20} aria-hidden />
                    <span>{label}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </nav>
    </aside>
  )
}
```

対応するCSS（抜粋）：

```css
.sidebar {
  background: var(--colors-sd-system-color-component-surface);
  border-right: 1px solid var(--colors-sd-system-color-component-outline-bright);
}
.sidebar nav a {
  color: var(--colors-sd-system-color-component-on-surface);
}
.sidebar nav a:hover {
  background: var(--colors-sd-system-color-interaction-hovered-variant);
}
.sidebar nav a[aria-current="page"] {
  background: var(--colors-sd-system-color-interaction-selected);
  color: var(--colors-sd-system-color-impression-primary);
}
```
