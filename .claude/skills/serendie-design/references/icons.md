# Serendie Symbols（アイコン）リファレンス

`@serendie/symbols` パッケージのアイコン使用ガイド。

> **💡 想定したアイコン名が見つからない場合**は、まず末尾「存在確認のベストプラクティス」セクションのコマンドで実際のexportsを列挙してください。よくある誤り（Chat→ChatRectangleなど）は下記「よくある誤りと対応」を参照。

---

## 基本ルール

1. **全アイコンに `SerendieSymbol` プレフィックス** が付く
2. 個別import（Tree Shakingを有効化するため）
3. SVGコンポーネントとして `width` / `height` で寸法指定
4. 色は親要素の `color` を継承
5. 装飾のみの場合は `aria-hidden` を付ける

## 基本的な使い方

```tsx
import { SerendieSymbolHome } from '@serendie/symbols'

// サイズ指定
<SerendieSymbolHome width={24} height={24} />

// 色指定（CSS変数を使う）
<SerendieSymbolHome
  width={24}
  height={24}
  style={{ color: 'var(--colors-sd-system-color-impression-primary)' }}
/>

// 装飾用（テキストラベルと併用）
<SerendieSymbolHome width={20} height={20} aria-hidden />
```

## Navigationなどで使う場合（コンポーネントを変数として）

```tsx
import { SerendieSymbolPlus, SerendieSymbolHistory } from '@serendie/symbols'

const NAV_ITEMS = [
  { path: '/chat', label: '新しいチャット', icon: SerendieSymbolPlus },
  { path: '/history', label: 'チャット履歴', icon: SerendieSymbolHistory },
]

{NAV_ITEMS.map(({ icon: Icon, label, path }) => (
  <Link to={path} key={path}>
    <Icon width={20} height={20} aria-hidden />
    <span>{label}</span>
  </Link>
))}
```

---

## よくある誤りと対応

想定した名前が存在しないことが多いので注意：

| 想定される名前 | 実際の名前 | 用途 |
|----------------|-----------|------|
| `SerendieSymbolChat` | `SerendieSymbolChatRectangle` | チャット |
| `SerendieSymbolAdd` | `SerendieSymbolPlus` | 追加 |
| `SerendieSymbolCategory` | `SerendieSymbolTag` | カテゴリ・タグ |
| `SerendieSymbolPalette` | `SerendieSymbolTag` | テーマ・色 |
| `SerendieSymbolSettings` | `SerendieSymbolGear` | 設定 |
| `SerendieSymbolLog` | `SerendieSymbolClipboard` | ログ・記録 |
| `SerendieSymbolPeople` | `SerendieSymbolGroup` | ユーザー・グループ |

---

## よく使うアイコン（カテゴリ別）

アイコンは305個以上あります。以下は代表例（全一覧は「存在確認」セクションのGitHub APIで取得）：

### ドキュメント・記録
- `SerendieSymbolArticle` - 記事・報告書・日報
- `SerendieSymbolStickyNote` - メモ・付箋
- `SerendieSymbolClipboard` - ログ・議事録
- `SerendieSymbolFileText` - テキストファイル
- `SerendieSymbolBookOpen` - 開いた本・マニュアル
- `SerendieSymbolBook` - 本
- `SerendieSymbolBookmark` - ブックマーク

### ナビゲーション・UI
- `SerendieSymbolChatRectangle` / `SerendieSymbolChatCircle` - チャット
- `SerendieSymbolHistory` - 履歴
- `SerendieSymbolFolder` - フォルダ
- `SerendieSymbolGear` - 設定
- `SerendieSymbolGroup` - グループ・ユーザー
- `SerendieSymbolHome` - ホーム

### アクション
- `SerendieSymbolPlus` - 追加・新規
- `SerendieSymbolClose` - 閉じる
- `SerendieSymbolEdit` / `SerendieSymbolPencil` - 編集
- `SerendieSymbolSend` - 送信
- `SerendieSymbolLogout` - ログアウト
- `SerendieSymbolTag` - タグ

### 状態・通知
- `SerendieSymbolAlertCircle` - 警告（丸）・エラー
- `SerendieSymbolAlertTriangle` - 警告（三角）・注意
- `SerendieSymbolAlertOctagon` - 重大警告
- `SerendieSymbolCheckCircle` / `SerendieSymbolCheckSquare` / `SerendieSymbolCheckShield` - チェック・完了
- `SerendieSymbolStopCircle` / `SerendieSymbolStop` - 停止

### 作業・工具
- `SerendieSymbolTool` - 工具・メンテナンス
- `SerendieSymbolBug` - バグ・不具合
- `SerendieSymbolTarget` - 目標・タスク
- `SerendieSymbolLightning` - 電気・アイデア

### メディア・入力
- `SerendieSymbolImage` / `SerendieSymbolCamera` - 画像
- `SerendieSymbolMic` / `SerendieSymbolMicMuted` - マイク
- `SerendieSymbolAttachment` - 添付

### その他
- `SerendieSymbolCalendar` - カレンダー
- `SerendieSymbolClock` - 時計
- `SerendieSymbolStar` - スター・お気に入り
- `SerendieSymbolPieChart` - 円グラフ

---

## 存在確認のベストプラクティス

`@serendie/symbols` には **305個以上のアイコン** が含まれており、実プロジェクトで使用中のものに限らず全て利用可能です。想定する名前が無い場合は以下で確認します：

### 方法1: GitHub APIで全アイコン一覧取得（インストール不要）

```bash
gh api "repos/serendie/serendie-symbols/contents/assets/outlined?per_page=500" --jq '.[] | .name'
```

結果のSVGファイル名（ケバブケース）を PascalCase 化して `SerendieSymbol` プレフィックスを付ける：

- `sticky-note.svg` → `SerendieSymbolStickyNote`
- `alert-triangle.svg` → `SerendieSymbolAlertTriangle`
- `chat-rectangle.svg` → `SerendieSymbolChatRectangle`

キーワード絞り込み例：

```bash
# 警告系
gh api "repos/serendie/serendie-symbols/contents/assets/outlined?per_page=500" --jq '.[] | .name' | grep -iE "alert|warn|error"
# 編集系
gh api "repos/serendie/serendie-symbols/contents/assets/outlined?per_page=500" --jq '.[] | .name' | grep -iE "edit|pencil|note|article"
```

### 方法2: Node.js で列挙（インストール済みの場合）

```bash
node --input-type=module -e "import('@serendie/symbols').then(m => console.log(Object.keys(m).sort().join('\n')))"
```

### 方法3: dist配下の型定義を確認

```bash
cat node_modules/@serendie/symbols/dist/index.d.ts | grep -E "^export" | head -50
```

### 方法4: Storybookで視覚的に検索

https://storybook.serendie.design の `Symbols` カテゴリで全アイコンを視覚的に確認可能。

### バリアント

- `assets/outlined/` — 標準（推奨）
- `assets/filled/` — 塗りつぶしバージョン

Reactコンポーネント側は outlined / filled を別名としてexportしている可能性あり（要確認）。

---

## パフォーマンスのヒント

- **必ず個別import**（namedimport）。`import * as Icons` は禁止
- アイコンが変わらない場合はJSX外でコンポーネント参照を確保：
  ```tsx
  const Icon = SerendieSymbolHome
  return <Icon width={24} height={24} />
  ```
- IconButton内で使う場合は `ReactElement` として渡す（`icon={<SerendieSymbolX />}`）

---

## アクセシビリティ

- 装飾のみ（隣にラベルテキストあり）: `aria-hidden`
- スタンドアロン: 親要素の `aria-label` またはSVGの `role="img"` + `aria-label`
- IconButton: `aria-label` 必須（Buttonの意味を記述）

```tsx
// 装飾用
<a href="/home">
  <SerendieSymbolHome width={20} height={20} aria-hidden />
  <span>ホーム</span>
</a>

// スタンドアロンIconButton
<IconButton
  icon={<SerendieSymbolClose />}
  aria-label="閉じる"
  shape="circle"
/>
```
