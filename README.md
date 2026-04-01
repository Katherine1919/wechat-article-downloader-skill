# wechat-article-downloader

中文 | [English](#english)

OpenClaw 可复用 Skill：按公众号名称批量下载文章（含图片）到 Obsidian，并自动生成标题分类报告。

## 功能特性
- 按关键词搜索公众号
- 拉取账号全部文章链接
- 使用 `opencli weixin download` 批量下载正文与图片
- 产出元数据文件（`articles-all-metadata.json`）
- 自动生成标题分类（`title-classification.md`）

## 环境要求
- Python 3.9+
- 系统可执行 `opencli`
- 可用的 `wechat-article-exporter` 服务（本地或远程）
- 有效的 `WX_AUTH_KEY`

## 配置
```bash
cp .env.example .env
```

至少填写：
- `WX_AUTH_KEY`
- `VAULT_PATH`

可选：
- `WX_EXPORTER_BASE`（默认 `http://localhost:3101`）
- `OUTPUT_SUBDIR`（默认 `00_Inbox/competitor_analysis`）
- `FILTER_MODE`（`all` 或 `topic`）
- `TOPIC_REGEX`（topic 模式下关键词）
- `MAX_DOWNLOAD`（限量下载，默认 `0` 表示全部）

## 使用方法
下载全部文章：
```bash
./scripts/run.sh --account "苍何" --mode all
```

只下载专题文章：
```bash
./scripts/run.sh --account "苍何" --mode topic
```

生产环境烟雾测试（限制下载 5 篇）：
```bash
MAX_DOWNLOAD=5 ./scripts/run.sh --account "苍何" --mode topic
```

## 输出目录结构
`$VAULT_PATH/$OUTPUT_SUBDIR/<account>/`

- `urls_all.txt`
- `articles-all-metadata.json`
- `raw_exports_all/`
- `title-classification.md`

若 `mode=topic`，还会额外生成：
- `urls_topic.txt`
- `raw_exports_topic/`

## 本地验证
```bash
python3 -m py_compile scripts/*.py
zsh -n scripts/run.sh
./scripts/run.sh --help
```

## License
MIT

---

## English

Reusable OpenClaw skill package to download WeChat public-account articles (with images) into Obsidian and generate title classification.

### Features
- Search account by keyword
- Extract all account article URLs
- Batch download article content + images via `opencli weixin download`
- Generate metadata (`articles-all-metadata.json`)
- Generate title classification (`title-classification.md`)

### Requirements
- Python 3.9+
- `opencli` available in PATH
- Running `wechat-article-exporter` service (local or hosted)
- Valid `WX_AUTH_KEY`

### Setup
```bash
cp .env.example .env
```

Required env values:
- `WX_AUTH_KEY`
- `VAULT_PATH`

### Usage
```bash
./scripts/run.sh --account "Canghe" --mode all
```

Topic-only mode:
```bash
./scripts/run.sh --account "Canghe" --mode topic
```

Production smoke test:
```bash
MAX_DOWNLOAD=5 ./scripts/run.sh --account "Canghe" --mode topic
```

### Verification
```bash
python3 -m py_compile scripts/*.py
zsh -n scripts/run.sh
./scripts/run.sh --help
```
