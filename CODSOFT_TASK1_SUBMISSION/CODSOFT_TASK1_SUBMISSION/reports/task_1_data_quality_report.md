# Task 1 — Data Cleaning & Preprocessing Report

## Dataset

- Source file: `data/raw/Online Retail.xlsx`
- Source: UCI Machine Learning Repository, Online Retail
- Original rows: **541,909**
- Original columns: **8**

## Data-quality findings

| Issue | Rows |
| --- | ---: |
| Exact duplicate rows detected | 5,268 |
| Missing descriptions | 1,454 |
| Missing customer IDs | 135,080 |
| Negative quantities (returns/cancellations) | 10,624 |
| Zero quantities | 0 |
| Negative unit prices | 2 |
| Zero unit prices | 2,515 |

## Cleaning actions

1. Standardized column names and trimmed repeated whitespace in text fields.
2. Normalized stock codes and invoice numbers to uppercase text.
3. Converted `InvoiceDate`, `Quantity`, `UnitPrice`, and `CustomerID` to
   analysis-ready types, with invalid values measured before removal.
4. Replaced missing descriptions with `UNKNOWN PRODUCT`.
5. Replaced missing customer IDs with `UNKNOWN` in the general cleaned file.
   These rows are excluded from the customer-ready file because they cannot be
   assigned to a customer.
6. Normalized the country label `EIRE` to `Ireland`.
7. Removed exact duplicates.
8. Removed rows with negative unit prices. Zero-price rows were retained and
   flagged because they may represent free samples or special transactions.
9. Classified negative-quantity or `C`-prefixed invoices as
   `RETURN_OR_CANCELLATION` instead of silently treating them as sales.
10. Added `LineTotal = Quantity * UnitPrice`.

## Output summary

| Output | Rows |
| --- | ---: |
| General cleaned transaction file | 536,639 |
| Customer-ready positive-sales file | 392,692 |
| Duplicate rows removed | 5,268 |
| Malformed required-field rows removed | 0 |
| Negative-price rows removed | 2 |
| Unknown-customer rows retained in general file | 135,035 |
| Unknown-product rows retained in general file | 1,454 |
| Returns/cancellations retained and classified | 10,587 |
| Zero-price rows retained and flagged | 2,510 |

## Limitations

The dataset does not contain customer age, so later customer segmentation will
use recency, purchase frequency, monetary value, geography, and product
behavior rather than age-based segments.
