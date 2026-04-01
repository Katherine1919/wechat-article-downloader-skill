# WeChat Article Downloader Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a GitHub-ready OpenClaw skill that downloads all articles from a target WeChat account (with images), stores outputs in an Obsidian vault, and generates title-based classification.

**Architecture:** A shell entrypoint (`scripts/run.sh`) orchestrates three Python scripts: account/article discovery, batch download via `opencli weixin download`, and markdown classification output. Runtime settings are environment-variable driven and loaded from `.env` (optional) to keep the repository portable and publishable.

**Tech Stack:** Bash (zsh-compatible), Python 3 stdlib, opencli CLI, Markdown

---

### Task 1: Scaffold GitHub-ready skill package

**Files:**
- Create: `SKILL.md`
- Create: `README.md`
- Create: `.env.example`
- Create: `LICENSE`

- [ ] **Step 1: Create skill frontmatter and usage contract**

```md
---
name: wechat-article-downloader
description: Download all articles from a WeChat account into Obsidian with metadata and title classification.
---
```

- [ ] **Step 2: Write README for install/config/run**

```md
# wechat-article-downloader
cp .env.example .env
./scripts/run.sh --account "Account Name"
```

- [ ] **Step 3: Add portable env template**

```env
WX_EXPORTER_BASE=http://localhost:3101
WX_AUTH_KEY=
VAULT_PATH=
OUTPUT_SUBDIR=00_Inbox/competitor_analysis
FILTER_MODE=all
```

- [ ] **Step 4: Add OSS license**

Run: `test -f LICENSE`
Expected: `LICENSE` exists and contains MIT text

### Task 2: Implement article discovery script

**Files:**
- Create: `scripts/fetch_account_articles.py`

- [ ] **Step 1: Add CLI arguments and env resolution**

```python
parser.add_argument("--account", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--mode", choices=["all", "topic"], default="all")
```

- [ ] **Step 2: Implement API fetch for account and paginated articles**

```python
GET /api/public/v1/account?keyword=...
GET /api/public/v1/article?fakeid=...&begin=...&size=20
```

- [ ] **Step 3: Write output artifacts**

```python
urls_all.txt
articles-all-metadata.json
```

- [ ] **Step 4: Verify script output**

Run: `python3 scripts/fetch_account_articles.py --help`
Expected: exit 0 and argument help is printed

### Task 3: Implement downloader and classifier scripts

**Files:**
- Create: `scripts/download_articles.py`
- Create: `scripts/classify_titles.py`

- [ ] **Step 1: Implement batch downloader around opencli**

```python
subprocess.run([
  "opencli", "weixin", "download",
  "--url", url,
  "--output", out_dir,
  "--download-images", "true", "-f", "json"
])
```

- [ ] **Step 2: Implement title-based category rules**

```python
rules = [
  ("OpenClaw Ecosystem", r"openclaw|lobster|龙虾|clawbot"),
  ("Agent Use Cases", r"agent|workflow|automation"),
]
```

- [ ] **Step 3: Render markdown report**

```md
# Title Classification
- OpenClaw Ecosystem: N
```

- [ ] **Step 4: Verify scripts parse**

Run: `python3 -m py_compile scripts/*.py`
Expected: exit 0

### Task 4: Add orchestrator and end-to-end docs

**Files:**
- Create: `scripts/run.sh`
- Modify: `README.md`

- [ ] **Step 1: Implement .env loader and argument handling**

```bash
set -euo pipefail
[[ -f .env ]] && set -a && source .env && set +a
```

- [ ] **Step 2: Chain fetch -> download -> classify**

```bash
python3 scripts/fetch_account_articles.py ...
python3 scripts/download_articles.py ...
python3 scripts/classify_titles.py ...
```

- [ ] **Step 3: Add dry-run and logs**

Run: `./scripts/run.sh --help`
Expected: shows required args and exits 0

- [ ] **Step 4: Final verification**

Run: `python3 -m py_compile scripts/*.py && ./scripts/run.sh --help`
Expected: both commands exit 0
