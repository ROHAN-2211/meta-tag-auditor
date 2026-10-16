# Meta Tag Auditor

A simple, free tool that checks a list of web pages for common on-page SEO problems and gives you a spreadsheet report.

Use it instead of opening pages one by one to check titles, descriptions and headings.

**Three ways to use it:** run it on GitHub with no installation, run it on your computer, or add it to Claude as a skill.

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

### Option 3: Use it as a Claude skill

This repo also works as a [Claude skill](https://support.claude.com/en/articles/12512180-use-skills-in-claude). Once it's added, ask Claude something like *"audit these pages for SEO issues"* and Claude runs the audit, explains what's wrong, and suggests rewritten titles and meta descriptions.

1. Download **[meta-tag-auditor-skill.zip](../../releases/latest/download/meta-tag-auditor-skill.zip)**. Upload this file exactly as it is, without unzipping it.
2. In Claude, make sure **Code execution and file creation** is turned on under **Settings → Capabilities**.
3. Go to **Customize → Skills**, click **+**, then **Create skill → Upload a skill**, and choose the zip.
4. Switch the skill on, then ask Claude to audit your pages.

Claude needs web access from code execution to fetch the pages. If every URL comes back as `ERROR`, allow web access in your Claude settings, or use Option 1 instead.

> Use the zip above rather than GitHub's green **Code → Download ZIP** button. That button names the folder `meta-tag-auditor-main`, and Claude needs the folder name to match the skill name.

## Customising

The recommended character limits and other settings are at the top of `audit.py` under **Settings you can change**.

## Good practice

- Only audit sites you own or have permission to check.
- The tool waits one second between pages so it doesn't overload a website.

## License

MIT. Free to use, copy and change.
