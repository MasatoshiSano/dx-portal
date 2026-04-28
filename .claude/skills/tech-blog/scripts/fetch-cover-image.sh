#!/usr/bin/env bash
# Unsplash APIから記事のカバー画像を取得するスクリプト
#
# Usage: ./fetch-cover-image.sh <query> <slug>
#   query: 検索キーワード（例: "DynamoDB AWS"）
#   slug:  記事のスラッグ（例: "dynamodb-gsi-rag-knowledge-search"）
#
# 環境変数:
#   UNSPLASH_ACCESS_KEY: Unsplash APIキー（.env.localから読み込み可）
#
# 出力:
#   成功時: /images/posts/<slug>-cover.jpg をstdoutに出力（coverImage用パス）
#   失敗時: exit 1
#
# 検索戦略（フォールバック付き）:
#   1. "technology <query>" で検索
#   2. 結果0件なら <query> のみで検索
#   3. それでも0件なら "technology programming" で検索

set -uo pipefail

QUERY="${1:?Usage: fetch-cover-image.sh <query> <slug>}"
SLUG="${2:?Usage: fetch-cover-image.sh <query> <slug>}"

BLOG_ROOT="$(pwd)"
OUTPUT_DIR="${BLOG_ROOT}/content/posts"
OUTPUT_FILE="${SLUG}-cover.jpg"
OUTPUT_PATH="${OUTPUT_DIR}/${OUTPUT_FILE}"
COVER_IMAGE_PATH="content/posts/${OUTPUT_FILE}"

# .env.localからAPIキーを読み込み（未設定の場合）
if [ -z "${UNSPLASH_ACCESS_KEY:-}" ] && [ -f "${BLOG_ROOT}/.env.local" ]; then
  UNSPLASH_ACCESS_KEY=$(grep '^UNSPLASH_ACCESS_KEY=' "${BLOG_ROOT}/.env.local" | cut -d= -f2-)
fi

if [ -z "${UNSPLASH_ACCESS_KEY:-}" ]; then
  echo "Error: UNSPLASH_ACCESS_KEY is not set" >&2
  exit 1
fi

mkdir -p "${OUTPUT_DIR}"

# Unsplash API検索関数: 画像URLを返す。見つからなければ空文字を返す
search_unsplash() {
  local q="$1"
  local encoded
  encoded=$(printf '%s' "${q}" | sed 's/ /%20/g')
  local response
  response=$(curl -sf \
    "https://api.unsplash.com/search/photos?query=${encoded}&per_page=1&orientation=landscape" \
    -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}" \
    2>/dev/null) || { echo ""; return; }
  local url
  url=$(echo "${response}" | grep -o '"regular":"[^"]*"' | head -1 | cut -d'"' -f4 || true)
  echo "${url}"
}

# フォールバック付き検索
DOWNLOAD_URL=""
for try_query in "technology ${QUERY}" "${QUERY}" "technology programming"; do
  DOWNLOAD_URL=$(search_unsplash "${try_query}")
  if [ -n "${DOWNLOAD_URL}" ]; then
    break
  fi
done

if [ -z "${DOWNLOAD_URL}" ]; then
  echo "Error: No image found after all fallback attempts" >&2
  exit 1
fi

# 画像をダウンロード
curl -sf -L -o "${OUTPUT_PATH}" "${DOWNLOAD_URL}" 2>/dev/null || {
  echo "Error: Failed to download image" >&2
  exit 1
}

# 成功: coverImageパスを出力
echo "${COVER_IMAGE_PATH}"
