# 配置说明（中文）

本文档说明：如何配置下载目标为「本地目录」或「小龙虾 workspace」。

## 1. 基础配置

先复制环境变量模板：

```bash
cp .env.example .env
```

必填项：
- `WX_AUTH_KEY`：`wechat-article-exporter` 登录态 key
- `VAULT_PATH`：你的 Obsidian Vault 根目录

常用可选项：
- `WX_EXPORTER_BASE`：默认 `http://localhost:3101`
- `OUTPUT_SUBDIR`：默认 `00_Inbox/competitor_analysis`
- `FILTER_MODE`：`all` 或 `topic`
- `TOPIC_REGEX`：专题过滤关键词
- `MAX_DOWNLOAD`：限制下载数量，`0` 表示不限制

## 2. 下载到 Obsidian（默认）

只要设置好 `VAULT_PATH`，运行后会写入：

`$VAULT_PATH/$OUTPUT_SUBDIR/<账号名>/`

示例：

```bash
./scripts/run.sh --account "苍何" --mode all
```

## 3. 额外导出到本地目录（Markdown）

设置 `LOCAL_MD_PATH` 为本地目录：

```bash
LOCAL_MD_PATH="/Users/KKClaw/Downloads/wx_md_exports" \
./scripts/run.sh --account "苍何" --mode all
```

导出目录：

`$LOCAL_MD_PATH/<账号名>/<mode>/`

包含：
- `*.md`
- `export-summary.json`

## 4. 额外导出到小龙虾 workspace（Markdown）

设置 `LOCAL_MD_PATH` 为 agent workspace 目录：

```bash
LOCAL_MD_PATH="/Users/KKClaw/.openclaw/agents/KK公众号主笔/workspace/inbox_md" \
./scripts/run.sh --account "苍何" --mode all
```

这样主笔/增长官可以直接读取导出的 md 内容进行学习与改写。

## 5. 生产环境建议

1. 首次上线先用 `MAX_DOWNLOAD=2` 做烟雾测试
2. 确认 `download-summary.json` 与 `export-summary.json` 正常
3. 再把 `MAX_DOWNLOAD` 调回 `0` 做全量下载
4. 如果报 `认证信息无效`，重新登录 exporter 并更新 `WX_AUTH_KEY`
