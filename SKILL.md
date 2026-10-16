---
name: meta-tag-auditor
description: Audit web pages for on-page SEO issues (titles, meta descriptions, H1s, canonicals, noindex, alt text, 404s) and suggest fixes. Use when asked to check pages or a site for SEO problems.
---

# Meta Tag Auditor

Checks a list of URLs for common on-page SEO problems using `audit.py` in this skill's folder, then explains the results and suggests fixes.

## Steps

1. **Get the URLs.** Ask the user for the pages to check if they haven't given any. Accept a pasted list, a sitemap URL, or a file. If they give only a homepage, suggest adding a few key pages (pricing, product, top blog posts) for a more useful audit.

2. **Install requirements** (once per session):
   ```bash
   pip install -r <skill-folder>/requirements.txt
   ```
   Add `--break-system-packages` if pip refuses to install.

3. **Write the URLs** to a text file, one per line, with no duplicates. Listing the same URL twice causes a false "Duplicate title" result.

4. **Run the audit:**
   ```bash
   python <skill-folder>/audit.py --input urls.txt --output report.csv
   ```

5. **Read `report.csv`** and reply with:
   - A one-line summary: how many pages were checked and how many have issues.
   - The problems grouped by type and ordered by impact: 404s and `noindex` first, then missing titles, descriptions and H1s, then length and duplicate issues, then alt text.
   - For each page with a missing, too-long or too-short title or meta description, a suggested rewrite within the limits (titles 30–60 characters, descriptions 70–160), based on the page's current H1 and content.

6. **Give the user `report.csv`** so they have the full table.

## Notes

- If every URL comes back as `ERROR`, this environment probably can't reach those sites. Tell the user to allow web access for code execution in their Claude settings, or to run the tool from GitHub instead.
- Only audit sites the user owns or has permission to check.
- The tool pauses one second between pages, so long lists take a while. Warn the user before running more than about 50 URLs.
