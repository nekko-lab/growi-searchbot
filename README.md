# growi-searchbot

Discord から部内 Growi の情報を検索するための Bot。

## 背景

部内の情報が Growi 上に増えるにつれ、目的のページを見つけるまでに何ページも辿る必要が出てきた。Discord からタイトル・本文を検索できるようにし、情報を探す手間を減らすために作成した。

## 機能

Slash Command として以下を提供する。

- `/search_title <keyword>`
  Growi のページタイトルにキーワードが含まれるページを検索する
- `/search_text <keyword>`
  Growi のページ本文にキーワードが含まれるページを検索する（全ページの本文を走査するため時間がかかる）

検索結果は Discord の1メッセージあたりの文字数上限に収まるよう、自動で分割して送信する。

## 仕組み

- Growi REST API (`/_api/v3/pages/list`, `/_api/v3/page`) から全ページのタイトル・本文・URL を取得し、メモリ上にキャッシュする
- キャッシュは起動時に構築したのち、1時間ごとにバックグラウンドで再取得する（検索のたびに Growi へ問い合わせない）
- ページ取得は `aiohttp` で非同期・並列に行う

## 技術スタック

- Python 3.12
- discord.py（Slash Command）
- aiohttp
- Docker

## セットアップ

1. `.env` に以下を設定する

   \`\`\`
   GROWI_URL=https://your-growi-instance
   GROWI_API_TOKEN=xxxx
   DISCORD_TOKEN=xxxx
   \`\`\`

2. Docker で起動する

   \`\`\`
   docker build -t growi-searchbot .
   docker run --env-file .env growi-searchbot
   \`\`\`

起動後、Growi の全ページを取得し終えるまで（`ready` になるまで）は検索コマンドが「準備中です」と応答する。
