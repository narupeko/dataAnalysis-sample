# 文献リスト(bibliography.csv)にあるオープンアクセス論文をまとめてダウンロードする
#
# 使い方（インターネットに接続できる手元のPCで実行）:
#   pip install requests
#   python fetch_papers.py --email you@example.com
#
# 処理の流れ:
#   1. bibliography.csv の oa_url があればそのURLから取得
#   2. なければ DOI を Unpaywall API で照会し、OA版PDFのURLを探して取得
#   3. 取得結果を download_log.csv に記録（失敗・有料論文も記録）
import argparse
import csv
import re
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
HEADERS = {"User-Agent": "Mozilla/5.0 (dropout-research literature fetcher)"}


def safe_name(row):
    first_author = re.split(r"[,&; ]", row["authors"].strip())[0] or "anon"
    title = re.sub(r"[^\w\-]+", "_", row["title"])[:60]
    return f'{row["id"]}_{first_author}_{row["year"]}_{title}.pdf'


def unpaywall_pdf(doi, email):
    if not doi:
        return None
    r = requests.get(f"https://api.unpaywall.org/v2/{doi}", params={"email": email}, timeout=30)
    if r.status_code != 200:
        return None
    loc = r.json().get("best_oa_location") or {}
    return loc.get("url_for_pdf") or loc.get("url")


def download(url, dest):
    r = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
    r.raise_for_status()
    if not r.content.startswith(b"%PDF"):
        # PDFではなくHTML（ランディングページ）が返ってきた場合
        return "not_pdf"
    dest.write_bytes(r.content)
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True, help="Unpaywall API に渡す連絡先メール")
    ap.add_argument("--csv", default=HERE / "bibliography.csv")
    ap.add_argument("--out", default=HERE / "papers")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(exist_ok=True)
    log = []
    with open(args.csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        dest = out / safe_name(row)
        if dest.exists():
            log.append({**row, "result": "exists", "file": dest.name})
            continue
        url = row.get("oa_url") or unpaywall_pdf(row.get("doi", "").strip(), args.email)
        if not url:
            log.append({**row, "result": "no_oa", "file": ""})
            continue
        try:
            result = download(url, dest)
        except Exception as e:  # noqa: BLE001
            result = f"error: {e}"
        log.append({**row, "result": result, "file": dest.name if result == "ok" else "", "used_url": url})
        print(f'[{result}] {row["id"]} {row["title"][:70]}')
        time.sleep(1)

    fields = list(rows[0].keys()) + ["result", "file", "used_url"]
    with open(out / "download_log.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(log)
    ok = sum(1 for x in log if x["result"] in ("ok", "exists"))
    print(f"取得 {ok} / {len(log)} 件  → {out}")


if __name__ == "__main__":
    main()
