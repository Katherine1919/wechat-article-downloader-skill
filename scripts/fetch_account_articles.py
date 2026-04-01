#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


def request_json(base: str, path: str, auth_key: str) -> dict:
    req = Request(f"{base}{path}")
    req.add_header("Cookie", f"auth-key={auth_key}")
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def safe_dirname(name: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]", "_", name).strip()
    return cleaned or "account"


def resolve_account(account_resp: dict, keyword: str):
    base_resp = account_resp.get("base_resp", {})
    ret = base_resp.get("ret", 0)
    if ret != 0:
        msg = base_resp.get("err_msg", "account query failed")
        raise RuntimeError(f"Account query failed: {msg} (ret={ret})")

    items = account_resp.get("list", [])
    if not items:
        raise RuntimeError(f"No account found for keyword: {keyword}")

    for item in items:
        name = str(item.get("nickname") or "")
        alias = str(item.get("alias") or "")
        if keyword.lower() in name.lower() or keyword.lower() in alias.lower():
            return item
    return items[0]


def main():
    parser = argparse.ArgumentParser(description="Fetch WeChat account article URLs")
    parser.add_argument("--account", required=True, help="Account keyword")
    parser.add_argument("--output-root", required=True, help="Root output directory")
    parser.add_argument("--mode", choices=["all", "topic"], default="all")
    parser.add_argument("--topic-regex", default=os.getenv("TOPIC_REGEX", "openclaw|lobster|agent|龙虾"))
    parser.add_argument("--base", default=os.getenv("WX_EXPORTER_BASE", "http://localhost:3101"))
    parser.add_argument("--auth-key", default=os.getenv("WX_AUTH_KEY", ""))
    args = parser.parse_args()

    if not args.auth_key:
        raise RuntimeError("Missing auth key. Set WX_AUTH_KEY or --auth-key")

    account_resp = request_json(
        args.base,
        f"/api/public/v1/account?keyword={quote(args.account)}&size=20",
        args.auth_key,
    )

    account = resolve_account(account_resp, args.account)
    fakeid = account.get("fakeid")
    if not fakeid:
        raise RuntimeError("Could not resolve account fakeid")

    account_name = str(account.get("nickname") or args.account)
    out_dir = Path(args.output_root) / safe_dirname(account_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_articles = []
    begin = 0
    size = 20
    while True:
        article_resp = request_json(
            args.base,
            f"/api/public/v1/article?fakeid={quote(str(fakeid))}&begin={begin}&size={size}",
            args.auth_key,
        )
        if article_resp.get("base_resp", {}).get("ret") != 0:
            break
        batch = article_resp.get("articles") or []
        if not batch:
            break
        all_articles.extend(batch)
        if len(batch) < size:
            break
        begin += size

    parsed = []
    for item in all_articles:
        title = str(item.get("title") or "")
        url = str(item.get("link") or item.get("url") or item.get("content_url") or "")
        if url.startswith("http"):
            parsed.append({"title": title, "url": url})

    dedup = {x["url"]: x for x in parsed}
    items = list(dedup.values())

    (out_dir / "urls_all.txt").write_text("\n".join(x["url"] for x in items) + "\n", encoding="utf-8")

    payload = {
        "account": {
            "nickname": account.get("nickname"),
            "alias": account.get("alias"),
            "fakeid": fakeid,
        },
        "totalFetched": len(all_articles),
        "all": len(items),
        "items": items,
    }
    (out_dir / "articles-all-metadata.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if args.mode == "topic":
        rx = re.compile(args.topic_regex, re.IGNORECASE)
        topic = [x for x in items if rx.search(x["title"] + " " + x["url"])]
        (out_dir / "urls_topic.txt").write_text(
            "\n".join(x["url"] for x in topic) + "\n",
            encoding="utf-8",
        )
        print(f"topic={len(topic)}")

    print(f"account_dir={out_dir}")
    print(f"total={len(all_articles)}")
    print(f"all_unique={len(items)}")


if __name__ == "__main__":
    main()
