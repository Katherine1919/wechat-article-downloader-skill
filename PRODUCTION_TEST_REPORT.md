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

---

## Additional Production Validation (local/workspace export)

Date: 2026-04-02

### Scope
- Verify markdown can be exported to local filesystem path
- Verify markdown can be exported to Lobster workspace path
- Verify artifacts are generated for both paths

### Commands executed

1) Build smoke input (2 URLs) from existing account list

2) Download smoke data:

```bash
python3 scripts/download_articles.py \
  --urls "/Users/KKClaw/openclaw-vault/00_Inbox/prod_validation/KK智能体实战笔记/urls_smoke_2.txt" \
  --output "/Users/KKClaw/openclaw-vault/00_Inbox/prod_release_test/KK智能体实战笔记/raw_exports_all" \
  --retries 1
```

Result: `{"total": 2, "success": 2, "failed": 0}`

3) Export markdown to local path:

```bash
python3 scripts/export_markdown.py \
  --source "/Users/KKClaw/openclaw-vault/00_Inbox/prod_release_test/KK智能体实战笔记/raw_exports_all" \
  --target "/Users/KKClaw/Downloads/wx_md_local_test" \
  --account "KK智能体实战笔记" \
  --mode all
```

4) Export markdown to Lobster workspace path:

```bash
python3 scripts/export_markdown.py \
  --source "/Users/KKClaw/openclaw-vault/00_Inbox/prod_release_test/KK智能体实战笔记/raw_exports_all" \
  --target "/Users/KKClaw/.openclaw/agents/KK公众号主笔/workspace/inbox_md_prod" \
  --account "KK智能体实战笔记" \
  --mode all
```

### Artifact verification
- Obsidian smoke output: `raw_exports_all/download-summary.json` exists
- Local export: `.../wx_md_local_test/KK智能体实战笔记/all/export-summary.json` exists
- Workspace export: `.../workspace/inbox_md_prod/KK智能体实战笔记/all/export-summary.json` exists
- Classification output exists in smoke folder

### Notes
- During one end-to-end run with old auth key, exporter returned `认证信息无效 (ret=-1)` as expected.
- Error handling now reports this clearly.
