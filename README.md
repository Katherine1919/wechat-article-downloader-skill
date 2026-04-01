# wechat-article-downloader

中文 | [English](#english)

OpenClaw 可复用 Skill：按公众号名称批量下载文章（含图片）到 Obsidian，并自动生成标题分类报告。

详细配置（中文）：`docs/CONFIGURATION_ZH.md`

## 给龙虾一句话（最简单）

如果你不想自己操作终端，直接把下面这句话发给 `@KK大总管`：

```text
安装并启用这个 skill： https://github.com/Katherine1919/wechat-article-downloader-skill 。配置 VAULT_PATH=/Users/KKClaw/openclaw-vault、WX_EXPORTER_BASE=http://localhost:3101；向我索取并写入 WX_AUTH_KEY；然后用账号“KK智能体实战笔记”先跑 MAX_DOWNLOAD=5 的烟雾测试并回报输出路径，最后再跑全量下载。
```

安装完成后，再发这句即可执行：

```text
用 wechat-article-downloader 下载“KK智能体实战笔记”全部文章，保存到 Obsidian，并把 markdown 同步到主笔 workspace。
```

如果出现审批提示，发送：`/approve <id> allow-once`。

---

## 文科生 3 步（手动版）

1) 打开终端并进入目录：

```bash
cd "/Users/KKClaw/Downloads/wechat-article-downloader-skill"
```

2) 初始化配置并填写两个值：

```bash
cp .env.example .env
open -e .env
```

在 `.env` 里至少填：

```env
WX_AUTH_KEY=你的auth-key
VAULT_PATH=/Users/KKClaw/openclaw-vault
```

3) 执行下载：

```bash
./scripts/run.sh --account "KK智能体实战笔记" --mode all
```

下载目录：

`/Users/KKClaw/openclaw-vault/00_Inbox/competitor_analysis/KK智能体实战笔记/`

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

> `LOCAL_MD_PATH` 为空时：只下载到 Obsidian。
> `LOCAL_MD_PATH` 有值时：会额外导出 markdown 到本地/workspace。

可选：
- `WX_EXPORTER_BASE`（默认 `http://localhost:3101`）
- `OUTPUT_SUBDIR`（默认 `00_Inbox/competitor_analysis`）
- `FILTER_MODE`（`all` 或 `topic`）
- `TOPIC_REGEX`（topic 模式下关键词）
- `MAX_DOWNLOAD`（限量下载，默认 `0` 表示全部）
- `LOCAL_MD_PATH`（可选：把 Markdown 额外导出到本地目录或龙虾 workspace）

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

导出到龙虾 workspace（示例）：
```bash
LOCAL_MD_PATH="/Users/KKClaw/.openclaw/agents/KK公众号主笔/workspace/inbox_md" \
./scripts/run.sh --account "苍何" --mode all
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

若设置了 `LOCAL_MD_PATH`，还会额外导出：
- `$LOCAL_MD_PATH/<account>/<mode>/*.md`
- `$LOCAL_MD_PATH/<account>/<mode>/export-summary.json`

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

Export markdown to a local/workspace path:
```bash
LOCAL_MD_PATH="/Users/KKClaw/.openclaw/agents/KK公众号主笔/workspace/inbox_md" \
./scripts/run.sh --account "Canghe" --mode all
```

### Verification
```bash
python3 -m py_compile scripts/*.py
zsh -n scripts/run.sh
./scripts/run.sh --help
```
