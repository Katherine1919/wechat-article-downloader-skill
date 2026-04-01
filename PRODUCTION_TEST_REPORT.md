# Production Validation Report

Date: 2026-04-02

## Scope
- Static checks (Python + shell syntax)
- CLI contract checks (`--help`)
- Negative-path checks (invalid auth)
- End-to-end bounded run with real provider session

## Results

### 1) Static checks
- `python3 -m py_compile scripts/*.py` -> PASS
- `zsh -n scripts/run.sh` -> PASS

### 2) CLI contract
- `scripts/run.sh --help` -> PASS
- `scripts/fetch_account_articles.py --help` -> PASS
- `scripts/download_articles.py --help` -> PASS
- `scripts/classify_titles.py --help` -> PASS

### 3) Negative-path
- Invalid auth key on fetch returns explicit provider error:
  - `RuntimeError: Account query failed: 认证信息无效 (ret=-1)`

### 4) End-to-end smoke (production-like)
Command:

```bash
WX_AUTH_KEY="***" \
VAULT_PATH="/Users/KKClaw/openclaw-vault" \
OUTPUT_SUBDIR="00_Inbox/prod_validation" \
MAX_DOWNLOAD=3 \
FILTER_MODE=topic \
./scripts/run.sh --account "苍何" --mode topic
```

Observed:
- account fetch: `total=654`, `all_unique=654`, `topic=37`
- bounded download summary:
  - `total=3`, `success=3`, `failed=0`
- classification generated successfully

Output path:
- `/Users/KKClaw/openclaw-vault/00_Inbox/prod_validation/苍何`

Artifacts present:
- `urls_all.txt`
- `urls_topic.txt`
- `articles-all-metadata.json`
- `raw_exports_topic/download-summary.json`
- `title-classification.md`

Note:
- Bounded download may produce fewer unique folders than requested URLs when source URLs are duplicates or map to same article content.

## Readiness
Current package is ready for GitHub publication and production pilot runs.
