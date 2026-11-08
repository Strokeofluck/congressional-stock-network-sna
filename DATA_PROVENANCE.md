# Data provenance

## Original source

[U.S. House Clerk financial disclosures](https://disclosures-clerk.house.gov/) provide the original Periodic Transaction Reports. Each extract row retains its original PDF URL, filing ID, and page where available.

## Frozen extract

This repository copies the analysis input from [Sean Ryan's original congressional stock-network project](https://github.com/Strokeofluck/congressional-stock-network-2025), as available locally on November 8, 2026. That project's provenance identifies the V8.2 House PTR output source blob as `418f6b6e46674ef944b617f24f7890803c0e7bdc`.

The extract has 3,179 accepted public-stock purchase records dated in 2025. This repository recalculates network metrics against that fixed extract. It does not assert that the scrape is current or exhaustive.

## Fields

| Field | Meaning |
|---|---|
| filing_id | Source PTR filing identifier |
| politician | Filer display name |
| asset_v8_2_cleaned | Cleaned asset label |
| ticker_v8_2_cleaned | Resolved ticker used for network ties |
| asset_type | Source asset classification, ST in this extract |
| transaction_type | Purchase classification, P in this extract |
| transaction_date | Reported transaction date |
| amount_min, amount_max, amount_category | Disclosed amount range |
| location, page | Source location metadata |
| original_pdf_url | Link to original House disclosure |
| ticker_parse_status | Parser acceptance status |

Repeated records collapse to unique filer–ticker ties for the reported degree and projection metrics. All 3,179 rows remain available for inspection. See [methods](METHODS.md) for graph filters and limitations.

The input lives in `data/`; the website also provides a downloadable copy in `site/purchase-data.csv`. The build copies from the canonical input, keeping these identical.
