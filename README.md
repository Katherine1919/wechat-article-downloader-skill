# wechat-article-downloader

GitHub-ready OpenClaw skill package for downloading WeChat public-account articles (including images) into an Obsidian vault.

## Features
- Account search by keyword
- Full article link extraction
- Batch article + image download using `opencli weixin download`
- Metadata output (`articles-all-metadata.json`)
- Title classification report (`title-classification.md`)

## Requirements
- Python 3.9+
- `opencli` available in PATH
- Local or hosted `wechat-article-exporter` service
- Valid auth cookie key (`WX_AUTH_KEY`)

## Setup
```bash
cp .env.example .env
```

Edit `.env`:
- `WX_AUTH_KEY`: required
- `VAULT_PATH`: required
- `WX_EXPORTER_BASE`: default `http://localhost:3101`

## Usage
```bash
./scripts/run.sh --account "Draco正在VibeCoding"
```

Optional:
```bash
./scripts/run.sh --account "Draco正在VibeCoding" --mode topic
```

For production smoke/limit tests:
```bash
MAX_DOWNLOAD=5 ./scripts/run.sh --account "Draco正在VibeCoding" --mode topic
```

## Output layout
`$VAULT_PATH/$OUTPUT_SUBDIR/<account>/`

- `urls_all.txt`
- `articles-all-metadata.json`
- `raw_exports_all/`
- `title-classification.md`

If `--mode topic`, also creates:
- `urls_topic.txt`
- `raw_exports_topic/`

## Verification
```bash
python3 -m py_compile scripts/*.py
./scripts/run.sh --help
```

## License
MIT
