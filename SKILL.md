---
name: wechat-article-downloader
description: Download WeChat account articles (with images) into an Obsidian vault and generate title classification.
---

# wechat-article-downloader

Use this skill when user asks to download articles from a WeChat public account and store outputs in Obsidian.

## What it does
- Searches account by keyword
- Fetches all article links from the account
- Downloads article content and images via `opencli weixin download`
- Writes metadata and URL list files
- Generates title-based classification markdown
- Optionally exports markdown files to local path or Lobster workspace via `LOCAL_MD_PATH`

## Required environment
- `WX_AUTH_KEY`
- `VAULT_PATH`

## Quick run
```bash
cp .env.example .env
./scripts/run.sh --account "Target Account"
```
