#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


RULES = [
    ("OpenClaw Ecosystem", r"openclaw|lobster|龙虾|clawbot|skills?"),
    ("Agent Use Cases", r"agent|智能体|workflow|automation|一人公司"),
    ("Tutorials and Deployment", r"教程|部署|安装|guide|入门|手把手|setup"),
    ("Model and Product Releases", r"发布|上线|版本|更新|beta|new"),
    ("Industry Commentary", r"复盘|对比|评测|为什么|受害者|再见"),
    ("AIGC Creation", r"出图|视频|电影|漫剧|数字人|创作"),
    ("Growth and Monetization", r"增长|赚钱|变现|转化|流量|电商"),
    ("Other AI Topics", r".*"),
]


def main():
    parser = argparse.ArgumentParser(description="Classify article titles into categories")
    parser.add_argument("--metadata", required=True, help="Path to articles-all-metadata.json")
    parser.add_argument("--output", required=True, help="Path to markdown output")
    args = parser.parse_args()

    data = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
    items = data.get("items", [])

    grouped = defaultdict(list)
    for item in items:
        title = str(item.get("title") or "")
        for name, pat in RULES:
            if re.search(pat, title, re.IGNORECASE):
                grouped[name].append(title)
                break

    lines = [
        "# Title Classification",
        "",
        f"Total Articles: {len(items)}",
        "",
        "## Counts",
    ]
    for name, _ in RULES:
        lines.append(f"- {name}: {len(grouped[name])}")

    for name, _ in RULES:
        lines.append("")
        lines.append(f"## {name}")
        samples = grouped[name][:10]
        if not samples:
            lines.append("- (none)")
        else:
            for title in samples:
                lines.append(f"- {title}")

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
