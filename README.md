# Meta Tag Auditor

A simple, free tool that checks a list of web pages for common on-page SEO problems and gives you a spreadsheet report.

Use it instead of opening pages one by one to check titles, descriptions and headings.

## What it checks

| Check | What gets flagged |
|---|---|
| Page status | 404s, errors and redirects |
| Title tag | Missing, too short (under 30 chars), too long (over 60), duplicated across pages |
| Meta description | Missing, too short (under 70 chars), too long (over 160), duplicated across pages |
| H1 heading | Missing, or more than one per page |
| Canonical tag | Missing |
| Indexability | Page set to `noindex` |
| Images | Images with no alt text |

## Example output

Each page gets one row in `report.csv`, with an **issues** column summarising what to fix. See [`example-report.csv`](example-report.csv).

| url | status_code | issues |
|---|---|---|
| https://example.com/blog/running-shoes | 200 | OK |
| https://example.com/old-page | 200 | Title too short; Missing meta description; Multiple H1s |
| https://example.com/deleted | 404 | Page returns 404 |

## How to use it

### Option 1: Run it on GitHub (no installation)

1. Click **Fork** at the top of this page to copy the repo to your account.
2. Open `urls.txt`, click the pencil icon, and replace the sample URLs with your own pages.
3. Go to the **Actions** tab, choose **Weekly meta tag audit**, and click **Run workflow**.
4. When it finishes, open the run and download **seo-report** at the bottom of the page.

It also runs automatically every Monday morning.

### Option 2: Run it on your computer

You need [Python](https://www.python.org/downloads/) installed.

```bash
pip install -r requirements.txt
python audit.py
```

Then open `report.csv` in Excel or Google Sheets.

To use a different list of URLs or report name:

```bash
python audit.py --input my_urls.txt --output my_report.csv
```

## Customising

The recommended character limits and other settings are at the top of `audit.py` under **Settings you can change**.

## Good practice

- Only audit sites you own or have permission to check.
- The tool waits one second between pages so it doesn't overload a website.

## License

MIT. Free to use, copy and change.
