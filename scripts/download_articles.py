#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def load_urls(path: Path):
    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("http"):
            urls.append(line)
    return urls


def main():
    parser = argparse.ArgumentParser(description="Download WeChat articles with images")
    parser.add_argument("--urls", required=True, help="Path to URL list file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--retries", type=int, default=1, help="Retry count per URL")
    parser.add_argument("--max-items", type=int, default=0, help="Max number of URLs to download (0 means all)")
    args = parser.parse_args()

    urls_file = Path(args.urls)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    urls = load_urls(urls_file)
    if args.max_items > 0:
        urls = urls[: args.max_items]
    success = 0
    failed = []

    for url in urls:
        ok = False
        for _ in range(args.retries + 1):
            cmd = [
                "opencli",
                "weixin",
                "download",
                "--url",
                url,
                "--output",
                str(out_dir),
                "--download-images",
                "true",
                "-f",
                "json",
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode == 0:
                ok = True
                break
        if ok:
            success += 1
        else:
            failed.append(url)

    summary = {
        "total": len(urls),
        "success": success,
        "failed": len(failed),
        "failed_urls": failed,
    }
    (out_dir / "download-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
