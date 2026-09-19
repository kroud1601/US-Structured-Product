# U.S. Structured Products Research Project

This beginner-friendly Python project studies U.S. SEC Form 424B2 filings from **January 1, 2016 through September 18, 2026**. It combines:

- an exact census of all Form 424B2 filing metadata;
- a reproducible issuer-year probability sample for document-text analysis;
- structured-product, autocallable, and snowball classification;
- extraction of payoff, underlying, maturity, coupon, barrier, principal, value, and retail-distribution fields;
- weighted annual, quarterly, issuer, product, underlying, risk, and data-quality statistics.

The project does not claim that every Form 424B2 filing is a structured product. It also does not treat principal amounts as AUM or note units as investor counts.

## One-time setup

Install Python 3.10 or newer, open a terminal in this folder, and run:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

For the exact package versions used for the final build, install `requirements-lock.txt` instead.

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Your SEC identity is stored in `config/config.yaml`. Check the setup with:

```bash
python run_project.py doctor
python -m unittest discover -s tests -v
```

## Recommended research workflow

Run each command in order:

```bash
python run_project.py metadata
python run_project.py sample-plan
python run_project.py primary-map
python run_project.py collect --research-sample
python run_project.py build
python run_project.py analyze
python run_project.py validation-sample --size 500
```

What each command does:

1. `metadata` builds the exact SEC Form 424B2 census.
2. `sample-plan` selects the documented issuer-year probability sample and assigns weights.
3. `primary-map` maps sampled accessions to direct SEC pricing-supplement documents.
4. `collect --research-sample` downloads, classifies, and extracts the sample. It saves every 25 results and can be restarted.
5. `build` creates a case-level deduplicated offering file for exploration.
6. `analyze` creates weighted CSV tables, figures, source examples, and the full report.
7. `validation-sample` creates a 500-row classification review template. Manually audit extracted fields for at least 200 confirmed structured notes.

After `analyze`, rebuild the Excel workbook and PDF with:

```bash
python scripts/build_analysis_workbook.py
python scripts/build_report_pdf.py
```

To reproduce the expanded statistical analysis and its supporting CSV tables,
run:

```bash
python scripts/run_expanded_analysis.py
```

See `docs/EXPANDED_ANALYSIS_GUIDE.md` for detailed Windows, macOS, and Linux
instructions. The finished expanded workbook is included at
`output/US_Structured_Products_Expanded_Analysis.xlsx`.

The formatted Excel workbook is included in `output/`. The beginner-friendly renderer uses Python and OpenPyXL. The earlier JavaScript renderer is retained as an optional reference, but it is not required.

For a detailed explanation of every stage, formula, command, and quality-control step, read `docs/COMPLETE_REPRODUCTION_GUIDE.md`.

If collection stops, run the same command again. Successful accession numbers are skipped. Failed accessions are retried.

## Small practice run

Use the synthetic offline demonstration to learn the folders without downloading SEC data:

```bash
python run_project.py demo
```

For a live diagnostic subset:

```bash
python run_project.py collect --limit 100
```

The final study uses `--research-sample`, not `--full`. Downloading all 618,291 filing documents adds large cost with little benefit after an exact metadata census and a properly weighted term sample.

## Main outputs

| File or folder | Purpose |
|---|---|
| `data/interim/filing_universe.csv` | Exact Form 424B2 metadata census |
| `data/interim/research_sample.csv` | Selected accessions, strata, population sizes, and weights |
| `data/interim/primary_document_map.csv` | Accession-to-primary-document audit map |
| `data/interim/classified_filings.csv` | Download status, labels, extracted terms, and evidence fields |
| `data/processed/offerings_master.csv` | Deduplicated sampled offering records for case analysis |
| `data/processed/universe_annual.csv` | Exact annual Form 424B2 filing counts |
| `data/processed/structured_annual.csv` | Weighted annual structured-product and snowball estimates |
| `data/processed/product_summary.csv` | Weighted product distribution |
| `data/processed/issuer_structured.csv` | Weighted structured-product issuer distribution |
| `data/processed/term_summary.csv` | Coverage and weighted economic-term statistics |
| `data/processed/principal_summary.csv` | Disclosed-principal sensitivity table, explicitly not AUM |
| `data/processed/buyer_observability.csv` | What buyer questions can and cannot be answered |
| `data/examples/` | Curated original SEC HTML examples |
| `data/validation/validation_sample.csv` | Manual classification/extraction review sheet |
| `figures/` | Report-ready PNG figures |
| `report/FULL_REPORT.md` | Full results, method, interpretation, limitations, and references |
| `output/US_Structured_Products_Analysis.xlsx` | Formatted analysis workbook with formulas and charts |
| `output/pdf/US_Structured_Products_Market_Report.pdf` | Professor-ready PDF report |

## Interpretation rules

- Exact census tables support statements about all Form 424B2 filings.
- Structured-product, snowball, product, underlying, and term results are weighted sample estimates.
- A filing is the population unit. The deduplicated offering file is exploratory because amendments and final supplements do not always share a universal deal identifier.
- The principal sensitivity table keeps only conservative aggregate amounts of at least $100,000; smaller per-note denominations are excluded. Even retained amounts may be stated, expected, approximate, or maximum principal and are not outstanding AUM.
- Form 424B2 generally does not disclose beneficial-owner identity or the number of purchasers.
- 2026 includes filings only through September 18.
- Automated classification and extraction require manual validation before publication.

Read `docs/BEGINNER_GUIDE.md`, `docs/METHODOLOGY.md`, `docs/DATA_DICTIONARY.md`, and `docs/VALIDATION_GUIDE.md` before changing the rules.
