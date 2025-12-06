# ACL Paper Scraper

This directory contains scripts to scrape ACL conference papers (2023-2025) from various sources.

## Scripts

### 1. `acl_scraper.py` - ACL Anthology Scraper

Scrapes **accepted papers** from [ACL Anthology](https://aclanthology.org/), the official repository for ACL publications.

**Features:**
- Scrapes ACL, NAACL, EMNLP, EACL, TACL papers
- Extracts: title, authors, abstract, PDF URL, DOI
- Supports years 2023-2025

**Usage:**
```bash
# Basic usage - scrape main venues
python acl_scraper.py

# Specify venues and years
python acl_scraper.py --venues acl emnlp --years 2023 2024

# Include detailed info (abstract, PDF URL)
python acl_scraper.py --details

# Custom output
python acl_scraper.py --output ./results --filename my_papers
```

### 2. `openreview_scraper.py` - OpenReview Scraper

Scrapes papers from [OpenReview](https://openreview.net/), which hosts ACL Rolling Review (ARR) submissions. This may include both **accepted and rejected** papers (if publicly visible).

**Features:**
- Scrapes ACL Rolling Review cycles
- May include rejected papers (if publicly available)
- Extracts paper decision/status information

**Usage:**
```bash
# Scrape all ARR cycles and direct venue submissions
python openreview_scraper.py

# Scrape only ARR cycles
python openreview_scraper.py --mode arr

# Specify years
python openreview_scraper.py --years 2023 2024 2025
```

### 3. `run_all.py` - Combined Scraper

Runs both scrapers and combines results.

**Usage:**
```bash
python run_all.py
```

## Output

All results are saved to the `data/` directory:

- `acl_papers.csv` / `acl_papers.json` - Papers from ACL Anthology
- `openreview_papers.csv` / `openreview_papers.json` - Papers from OpenReview
- `all_papers.csv` / `all_papers.json` - Combined results
- `*_summary.json` - Statistics about scraped papers

## Data Fields

| Field | Description |
|-------|-------------|
| `paper_id` | Unique identifier |
| `title` | Paper title |
| `authors` | List of authors |
| `authors_str` | Authors as comma-separated string |
| `abstract` | Paper abstract (if fetched) |
| `venue` | Conference venue (ACL, EMNLP, etc.) |
| `year` | Publication year |
| `status` | Paper status: accepted, rejected, submitted |
| `url` | URL to paper page |
| `pdf_url` | Direct link to PDF |
| `doi` | Digital Object Identifier |
| `scraped_at` | Timestamp of scraping |

## Installation

```bash
pip install -r requirements.txt
```

## Notes

### About Rejected Papers

- **ACL Anthology** only contains accepted papers
- **OpenReview/ARR** may contain rejected papers if:
  - The venue makes decisions public
  - Authors chose to make their submission visible
- Most rejected papers are not publicly available

### Rate Limiting

The scripts include built-in delays to be respectful to the servers. Please don't modify these to avoid getting blocked.

### Data Quality

- Paper metadata is extracted automatically and may have occasional errors
- Abstract extraction may fail for some older papers
- Author name formatting may vary

## Example Output

```
Scraping complete!
Total papers: 10565

Papers by venue:
EMNLP    4726
ACL      4262
NAACL    1577

Papers by year:
2025    4970
2024    3154
2023    2441
```

## Current Data (As of Dec 2024)

| Source | Papers | Description |
|--------|--------|-------------|
| ACL Anthology | 10,565 | Accepted papers from ACL, NAACL, EMNLP (2023-2025) |
| OpenReview ARR | 2,166+ | Submitted papers to ACL Rolling Review |

