#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path


def safe_name(name: str) -> str:
    return re.sub(r"[\\/:*?\"<>|]", "_", name).strip() or "account"


def export_markdown_files(source_dir: Path, target_root: Path, account_name: str, mode: str) -> dict:
    source_dir = Path(source_dir)
    target_root = Path(target_root)
    account_dir = target_root / safe_name(account_name) / mode
    account_dir.mkdir(parents=True, exist_ok=True)

    exported = 0
    collisions = 0
    for md in sorted(source_dir.rglob("*.md")):
        if not md.is_file():
            continue
        stem = safe_name(md.stem)
        rel_hint = safe_name(str(md.parent.relative_to(source_dir)))
        filename = f"{rel_hint}__{stem}.md"
        dst = account_dir / filename
        if dst.exists():
            collisions += 1
            dst = account_dir / f"{rel_hint}__{stem}__{collisions}.md"
        shutil.copy2(md, dst)
        exported += 1

    summary = {
        "source": str(source_dir),
        "target": str(account_dir),
        "mode": mode,
        "exported": exported,
        "collisions": collisions,
    }
    (account_dir / "export-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Export markdown files to local directory")
    parser.add_argument("--source", required=True, help="raw exports directory")
    parser.add_argument("--target", required=True, help="local markdown target root")
    parser.add_argument("--account", required=True, help="account name")
    parser.add_argument("--mode", choices=["all", "topic"], default="all")
    args = parser.parse_args()

    summary = export_markdown_files(
        source_dir=Path(args.source),
        target_root=Path(args.target),
        account_name=args.account,
        mode=args.mode,
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
