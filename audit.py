"""
Meta Tag Auditor
----------------
Checks a list of web pages for common on-page SEO issues and saves a report
you can open in Excel or Google Sheets.

How to use:
    1. Put one URL per line in urls.txt
    2. Run:  python audit.py
    3. Open report.csv

Optional:
    python audit.py --input my_urls.txt --output my_report.csv
"""

import argparse
import csv
import sys
import time

import requests
from bs4 import BeautifulSoup

# ---- Settings you can change ------------------------------------------------
TITLE_MIN, TITLE_MAX = 30, 60          # recommended title length (characters)
DESC_MIN, DESC_MAX = 70, 160           # recommended meta description length
REQUEST_TIMEOUT = 15                   # seconds to wait for each page
DELAY_BETWEEN_PAGES = 1                # seconds, so we don't overload the site
USER_AGENT = "MetaTagAuditor/1.0 (+https://github.com)"
# -----------------------------------------------------------------------------


def read_urls(path):
    """Read URLs from a text file, skipping blank lines and # comments."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = [line.strip() for line in f]
    except FileNotFoundError:
        sys.exit(f"Could not find '{path}'. Create it and add one URL per line.")
    urls = [u for u in lines if u and not u.startswith("#")]
    if not urls:
        sys.exit(f"'{path}' has no URLs in it yet.")
    return urls


def get_meta(soup, name):
    tag = soup.find("meta", attrs={"name": name})
    return (tag.get("content") or "").strip() if tag else ""


def audit_page(url):
    """Fetch one page and return a dict of findings."""
    row = {"url": url}
    issues = []

    try:
        resp = requests.get(
            url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT}
        )
    except requests.RequestException as e:
        row.update(status_code="ERROR", issues=f"Could not load page: {e.__class__.__name__}")
        return row

    row["status_code"] = resp.status_code
    row["final_url"] = resp.url
    if resp.history:
        issues.append(f"Redirects ({len(resp.history)} hop)")
    if resp.status_code >= 400:
        issues.append(f"Page returns {resp.status_code}")
        row["issues"] = "; ".join(issues)
        return row

    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title = soup.title.get_text(strip=True) if soup.title else ""
    row["title"] = title
    row["title_length"] = len(title)
    if not title:
        issues.append("Missing title")
    elif len(title) < TITLE_MIN:
        issues.append("Title too short")
    elif len(title) > TITLE_MAX:
        issues.append("Title too long")

    # Meta description
    desc = get_meta(soup, "description")
    row["meta_description"] = desc
    row["description_length"] = len(desc)
    if not desc:
        issues.append("Missing meta description")
    elif len(desc) < DESC_MIN:
        issues.append("Meta description too short")
    elif len(desc) > DESC_MAX:
        issues.append("Meta description too long")

    # H1
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    row["h1"] = h1s[0] if h1s else ""
    row["h1_count"] = len(h1s)
    if not h1s:
        issues.append("Missing H1")
    elif len(h1s) > 1:
        issues.append("Multiple H1s")

    # Canonical
    canon = soup.find("link", rel="canonical")
    row["canonical"] = canon.get("href", "") if canon else ""
    if not canon:
        issues.append("Missing canonical")

    # Indexability
    robots = get_meta(soup, "robots").lower()
    row["robots"] = robots
    if "noindex" in robots:
        issues.append("Page is set to noindex")

    # Images without alt text
    missing_alt = [i for i in soup.find_all("img") if not i.get("alt")]
    row["images_missing_alt"] = len(missing_alt)
    if missing_alt:
        issues.append(f"{len(missing_alt)} image(s) missing alt text")

    row["issues"] = "; ".join(issues) if issues else "OK"
    return row


def flag_duplicates(rows):
    """Mark titles and descriptions that appear on more than one page."""
    for field, label in (("title", "Duplicate title"), ("meta_description", "Duplicate meta description")):
        seen = {}
        for r in rows:
            value = r.get(field)
            if value:
                seen.setdefault(value, []).append(r)
        for group in seen.values():
            if len(group) > 1:
                for r in group:
                    r["issues"] = label if r["issues"] == "OK" else f"{r['issues']}; {label}"


COLUMNS = [
    "url", "status_code", "issues", "title", "title_length", "meta_description",
    "description_length", "h1", "h1_count", "canonical", "robots",
    "images_missing_alt", "final_url",
]


def main():
    parser = argparse.ArgumentParser(description="Audit meta tags for a list of URLs.")
    parser.add_argument("--input", default="urls.txt", help="Text file with one URL per line")
    parser.add_argument("--output", default="report.csv", help="Where to save the report")
    args = parser.parse_args()

    urls = read_urls(args.input)
    print(f"Auditing {len(urls)} page(s)...\n")

    rows = []
    for i, url in enumerate(urls, 1):
        row = audit_page(url)
        rows.append(row)
        print(f"[{i}/{len(urls)}] {url}  ->  {row.get('issues')}")
        if i < len(urls):
            time.sleep(DELAY_BETWEEN_PAGES)

    flag_duplicates(rows)

    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    problem_pages = sum(1 for r in rows if r.get("issues") != "OK")
    print(f"\nDone. {problem_pages} of {len(rows)} page(s) have issues.")
    print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()
