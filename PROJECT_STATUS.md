# Project Status

## Completed on September 19, 2026

- Research period fixed at January 1, 2016 through September 18, 2026.
- Exact SEC census completed: 618,291 unique Form 424B2 filing events.
- Issuer-year probability sample completed: 23,941 filings in 252 strata.
- Primary-document audit map completed: 97.58% direct primary-document coverage.
- Document collection completed: 23,941 successful downloads (100.0%).
- Classification and term extraction completed: 17,947 sampled filings classified as structured products.
- Case-level exploratory file built: 16,977 deduplicated sampled offerings.
- Weighted annual, quarterly, issuer, product, underlying, term, concentration, retail-proxy, and buyer-observability analyses completed.
- Twelve representative filings selected; original SEC HTML examples are included.
- A 100-row manual-validation worksheet was created. Human labels remain intentionally blank.
- Full Markdown report, 15-page PDF report, formatted Excel workbook, figures, processed tables, source code, tests, and beginner documentation completed.

## Verification

- All seven automated parser, classifier, extractor, normalization, and SEC-index tests pass.
- Python source compiles successfully.
- Census, sample, classified, and validation row counts match their expected unique-accession counts.
- Excel workbook recalculation and formula-error scan found no spreadsheet errors.
- Every workbook sheet and every PDF page was rendered and visually inspected.
- The PDF contains 15 readable pages and the Excel file passes ZIP-container integrity testing.

## Interpretation limits

- Exact counts describe Form 424B2 filing events, not unique deals or outstanding securities.
- Structured-product, snowball, product, underlying, and term statistics are weighted sample estimates.
- Confidence intervals cover sampling uncertainty, not classification or extraction error.
- Aggregate principal is a low-coverage sensitivity measure, not issuance AUM.
- Beneficial-owner identity and purchaser count are not observable in Form 424B2.
- The manual-validation template must be completed before claiming classifier accuracy in publication.
- 2026 is year-to-date through September 18.
