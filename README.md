# Philippines Tourism Analysis (2015–2023)

> **End-to-end data project** · SQL · Python · Power BI  
> Analyzing international visitor arrivals and regional tourism distribution in the Philippines, based on official government statistical reports.

---

## Project Background

This project was born from personal experience — I lived in Siargao, Philippines, and wanted to understand the country's tourism patterns through data. The source material consists of official PDF bulletins published by the **Philippine Statistics Authority (PSA)** and the **Department of Tourism (DOT)**, covering nearly a decade of visitor data — including the full impact of the COVID-19 pandemic.

The analysis covers two independent but complementary dimensions:

- **Visitor Arrivals** — international tourists by country of origin, monthly trends, COVID impact, and recovery
- **Regional Travelers** — where visitors actually go within the country (by region, province, and city), including domestic vs. foreign breakdown

---

## Key Insights

| Finding | Detail |
|---|---|
| **Total arrivals 2015–2023** | ~34 million international visitors |
| **Consistent #1 origin** | USA (every single year, 2015–2023) |
| **COVID collapse** | ~98% drop in arrivals in 2020 — the most severe in recorded history |
| **Recovery status** | Not fully recovered to 2019 levels by end of 2023 |
| **Peak month** | January (holiday season + ideal weather) |
| **Lowest month** | September (typhoon season) |
| **Top foreign destination** | NCR/Manila (Pasay & Parañaque — NAIA airport) |
| **Second hub** | Lapu-Lapu City, Cebu (Mactan-Cebu Airport) |
| **China pre-COVID** | Fastest growing market 2016–2019; slowest to recover post-pandemic |
| **Domestic tourism** | Represents ~80%+ of total tourist volume across all years |

---

## Dashboard Preview

| ![Total Arrivals](images/dashboard_total_arrivals.png) | ![Arrivals by Month](images/dashboard_arrivals_by_month.png) |
|---|---|
| Total Arrivals Overview | Seasonality — Monthly Patterns |

| ![Top Country](images/dashboard_top_country.png) | ![YoY / MoM](images/dashboard_yoy_mom.png) |
|---|---|
| Top Origin Country by Year | Year-over-Year & Month-over-Month |

| ![Foreign by City](images/dashboard_foreign_by_city.png) | ![Map — Region](images/dashboard_map_region.png) |
|---|---|
| Foreign Visitors by City | Regional Distribution Map |

---

## Dataset Description

All data originates from official Philippine government publications:

| Dataset | Source | Format | Coverage |
|---|---|---|---|
| Visitor Arrivals by Country | Philippine Statistics Authority (PSA) | Annual PDF bulletins | 2015–2023 |
| Regional Traveler Statistics | Department of Tourism (DOT) | Annual PDF bulletins | 2015–2023 |
| Tourism Satellite Account | PSA | PDF + Excel | Future phase |

**Key data variables:**
- `arrivals`: country of residence, monthly counts (Jan–Dec), annual total, year
- `regions`: region/province/city name, foreigner count, domestic count, OFW count, total, year

---

## Tools Used

| Tool | Purpose |
|---|---|
| **Python** | All extraction, cleaning, and transformation |
| **Pandas** | Data manipulation, merging, type handling |
| **Tabula-py** | Initial PDF table extraction |
| **pdfplumber** | Advanced coordinate-based extraction for complex PDFs |
| **openpyxl** | Excel output with color-coded geographic levels |
| **SQL (MySQL)** | Analytical queries — rankings, YoY growth, COVID recovery |
| **Power BI** | Final interactive dashboards (7 report pages) |

---

## Project Structure

```
Philippines-Tourism-Analysis/
│
├── data/
│   ├── sources/                   # Official PDF reports (originals, untouched)
│   │   ├── visitor_arrivals/      # PSA Annual Bulletins 2015–2023
│   │   ├── regional_travelers/    # DOT Regional Reports 2015–2023
│   │   └── satellite_account/    # Tourism Satellite Account (future)
│   ├── raw/                       # Data extracted directly from PDFs
│   │   ├── arrivals/              # CSVs from Tabula (unmodified output)
│   │   └── regions/               # Excel files extracted per year
│   └── processed/                 # Final cleaned datasets ready for analysis
│       ├── arrivals_master_2015_2023.csv
│       ├── regions_master_CLEAN.csv
│       └── region_coordinates.xlsx
│
├── Scripts/                     # Python cleaning & transformation scripts
│   ├── arrivals/
│   │   ├── 01_fix_2020.py         # Special handling for malformed 2020 PDF
│   │   ├── 02_clean_2015_2021.py  # Clean and standardize 2015–2021 data
│   │   ├── 03_clean_2022_2023.py  # Clean post-COVID column structure
│   │   └── 04_concatenate.py      # Merge all years into master dataset
│   └── regions/
│       ├── extract_pdf_to_excel.py  # Coordinate-based PDF extractor
│       ├── Regions_master_clean.py  # Standardize + classify geographic levels
│       ├── Clean_regions_master.py  # Additional cleaning pass
│       ├── Concatenate.py           # Merge all years into master dataset
│       └── create_region_coordinates.py  # Generate lat/lon lookup table
│
├── sql/
│   ├── Query_SQL_arrivals.sql     # 9 analytical queries — arrivals analysis
│   ├── Query_SQL_regions.sql      # 6 analytical queries — regional analysis
│   └── analysis_summary.md        # Full bilingual Q&A from the SQL analysis
│
├── powerbi/
│   └── PowerBI_ProjectPH.pbix    # Interactive dashboard (7 report pages)
│
├── images/                        # Dashboard screenshots
│   ├── dashboard_total_arrivals.png
│   ├── dashboard_arrivals_by_month.png
│   ├── dashboard_top_country.png
│   ├── dashboard_yoy_mom.png
│   ├── dashboard_foreign_by_city.png
│   ├── dashboard_map_city.png
│   └── dashboard_map_region.png
│
├── reports/                       # Analysis reports and summaries
│
└── _archive/                      # Deprecated scripts kept for reference
```

---

## Data Pipeline

### Phase 1 — Visitor Arrivals by Country

Annual PDF reports (each with a different layout) were extracted, cleaned, and merged:

```
Official PDFs (PSA, 2015–2023)
        │
        ▼
Tabula PDF extraction → data/raw/arrivals/  (unmodified CSVs)
        │
        ├── 01_fix_2020.py        ← 2020 PDF: split tables + swapped columns
        ├── 02_clean_2015_2021.py ← removes \xa0, \r, \n artifacts; numeric coercion
        ├── 03_clean_2022_2023.py ← handles new column layout post-COVID
        └── 04_concatenate.py     ← merges all years; adds YEAR column
                │
                ▼
        data/processed/arrivals_master_2015_2023.csv
```

### Phase 2 — Regional Travelers

Regional data required a custom coordinate-based extractor due to inconsistent PDF table boundaries:

```
Official PDFs (DOT, 2015–2023)
        │
        ▼
extract_pdf_to_excel.py → data/raw/regions/  (one Excel per year, color-coded)
        │
Regions_master_clean.py
        ├── Geographic level classification: Region / Province / City-Municipality
        ├── Coordinate mapping (lat/lon) for all 16 regions
        └── is_region_total flag for Power BI filtering
                │
                ▼
        data/processed/regions_master_CLEAN.csv
```

---

## SQL Analysis

15 analytical queries across 2 files answer the key business questions:

| File | Queries | Topics |
|---|---|---|
| `Query_SQL_arrivals.sql` | 9 | Rankings, YoY growth, seasonality, country comparison |
| `Query_SQL_regions.sql` | 6 | Regional distribution, COVID recovery, visitor type breakdown |

→ See [`sql/analysis_summary.md`](sql/analysis_summary.md) for all questions, queries, and findings (bilingual EN/ES).

---

## Dashboard Pages

| Page | Description |
|---|---|
| Total Arrivals | KPI overview — 34M total; bar chart by year; pie chart by country |
| Arrivals by Month | Seasonality view — January peak, September low; multi-year area chart |
| Top Country Year/Month | USA as top origin; monthly breakdown per country and year |
| YoY with MoM | COVID collapse visible in area chart; year-over-year and month-over-month % change |
| Foreign by City | Top cities by foreign visitor volume — Pasay, Parañaque, Lapu-Lapu lead |
| Map — City Level | Geographic bubble map of Philippines with city-level visitor distribution |
| Map — Region Level | Regional bubble map with bar chart by administrative region |

> Screenshots are available in the `05-images` folder.


## Data Challenges

This project required significantly more engineering effort than a standard CSV analysis:

- **PDF-only source data** — no APIs or structured downloads available
- **Encoding artifacts** — `\xa0`, `\r`, `\n` invisible characters causing silent type failures
- **OCR artifacts** — e.g., `"4 58,951"` parsed as string instead of `458,951`
- **Inconsistent table layouts** — especially the 2020 PDF (split tables, swapped columns)
- **Geographic classification inconsistency** — same cities classified as `Province` from 2018 onward in official sources; detected and corrected for 25+ locations
- **Duplicate records** — from overlapping row structures when concatenating 9 yearly files
- **Inconsistent naming** — same location spelled differently across years

---

## Roadmap

- [x] Visitor Arrivals pipeline (2015–2023)
- [x] Regional Travelers pipeline (2015–2023)
- [x] SQL analysis — 15 analytical queries
- [x] Power BI dashboard — 7 report pages
- [ ] Philippine Tourism Satellite Account integration (economic data layer)
- [ ] 2024–2025 data update

---

## Author

**Victor Toret Marin** — Data Analyst in training | Bootcamp Immune Technology Institute, Madrid  
Portfolio project — built end-to-end from raw PDFs to interactive SQL analysis and Power BI dashboard.

---

*Data sources: Philippine Statistics Authority (PSA) & Department of Tourism (DOT). All data is publicly available official government statistics.*
