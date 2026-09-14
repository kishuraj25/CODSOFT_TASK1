"""Clean the UCI Online Retail workbook for the CODSOFT Task 1 submission.

The pipeline is deliberately deterministic and preserves the raw workbook.
It creates both a general cleaned transaction file and a customer-ready sales
file for later internship tasks.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data/raw/Online Retail.xlsx")
DEFAULT_OUTPUT_DIR = Path("data/processed")
DEFAULT_REPORT_DIR = Path("reports")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    return parser.parse_args()


def normalize_text(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


def normalize_customer_ids(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    ids = numeric.round().astype("Int64").astype("string")
    return ids.fillna("UNKNOWN")


def collect_quality_metrics(
    df: pd.DataFrame, stage: str, duplicate_count: int | None = None
) -> list[dict[str, object]]:
    metrics: list[dict[str, object]] = [
        {"stage": stage, "metric": "row_count", "value": int(len(df))},
        {
            "stage": stage,
            "metric": "column_count",
            "value": int(len(df.columns)),
        },
    ]
    for column, count in df.isna().sum().items():
        metrics.append(
            {
                "stage": stage,
                "metric": f"missing_{column}",
                "value": int(count),
            }
        )
    if duplicate_count is not None:
        metrics.append(
            {
                "stage": stage,
                "metric": "duplicate_rows",
                "value": int(duplicate_count),
            }
        )
    return metrics


def clean_retail_data(
    raw: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, object]], dict[str, int]]:
    """Return cleaned general data, customer-ready data, metrics, and counts."""

    df = raw.copy()
    metrics = collect_quality_metrics(
        df, "raw", duplicate_count=int(df.duplicated().sum())
    )
    counts: dict[str, int] = {
        "raw_rows": len(df),
        "raw_duplicate_rows": int(df.duplicated().sum()),
        "raw_missing_descriptions": int(df["Description"].isna().sum()),
        "raw_missing_customer_ids": int(df["CustomerID"].isna().sum()),
        "raw_negative_quantities": int((df["Quantity"] < 0).sum()),
        "raw_zero_quantities": int((df["Quantity"] == 0).sum()),
        "raw_negative_prices": int((df["UnitPrice"] < 0).sum()),
        "raw_zero_prices": int((df["UnitPrice"] == 0).sum()),
    }

    df.columns = [re.sub(r"\s+", "", str(column).strip()) for column in df.columns]
    df["InvoiceNo"] = normalize_text(df["InvoiceNo"])
    df["StockCode"] = normalize_text(df["StockCode"]).str.upper()
    df["Description"] = normalize_text(df["Description"]).fillna("UNKNOWN PRODUCT")
    df["Country"] = normalize_text(df["Country"]).replace({"EIRE": "Ireland"})
    df["CustomerID"] = normalize_customer_ids(df["CustomerID"])
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Country",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
    ]
    malformed_required = int(df[required_columns].isna().any(axis=1).sum())
    counts["rows_with_malformed_required_fields"] = malformed_required
    df = df.dropna(subset=required_columns)

    before_deduplication = len(df)
    df = df.drop_duplicates().copy()
    counts["duplicate_rows_removed"] = before_deduplication - len(df)

    negative_price_rows = int((df["UnitPrice"] < 0).sum())
    counts["negative_price_rows_removed"] = negative_price_rows
    df = df[df["UnitPrice"] >= 0].copy()

    df["IsCancelled"] = df["InvoiceNo"].str.startswith("C", na=False)
    df["TransactionType"] = "SALE"
    df.loc[
        df["IsCancelled"] | (df["Quantity"] < 0), "TransactionType"
    ] = "RETURN_OR_CANCELLATION"
    df["PriceQualityFlag"] = "VALID"
    df.loc[df["UnitPrice"] == 0, "PriceQualityFlag"] = "ZERO_PRICE"
    df["LineTotal"] = (df["Quantity"] * df["UnitPrice"]).round(2)

    df = df.sort_values(["InvoiceDate", "InvoiceNo", "StockCode"]).reset_index(
        drop=True
    )
    df["InvoiceDate"] = df["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")

    customer_ready = df[
        (df["CustomerID"] != "UNKNOWN")
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
        & ~df["IsCancelled"]
    ].copy()

    metrics.extend(
        collect_quality_metrics(
            df, "cleaned_general", duplicate_count=int(df.duplicated().sum())
        )
    )
    metrics.extend(
        collect_quality_metrics(
            customer_ready,
            "customer_ready",
            duplicate_count=int(customer_ready.duplicated().sum()),
        )
    )
    counts["cleaned_general_rows"] = len(df)
    counts["customer_ready_rows"] = len(customer_ready)
    counts["unknown_customer_rows"] = int((df["CustomerID"] == "UNKNOWN").sum())
    counts["unknown_product_rows"] = int(
        (df["Description"] == "UNKNOWN PRODUCT").sum()
    )
    counts["return_or_cancellation_rows"] = int(
        (df["TransactionType"] == "RETURN_OR_CANCELLATION").sum()
    )
    counts["zero_price_rows_retained"] = int(
        (df["PriceQualityFlag"] == "ZERO_PRICE").sum()
    )
    return df, customer_ready, metrics, counts


def write_report(
    report_path: Path, counts: dict[str, int], input_path: Path
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = f"""# Task 1 — Data Cleaning & Preprocessing Report

## Dataset

- Source file: `{input_path}`
- Source: UCI Machine Learning Repository, Online Retail
- Original rows: **{counts["raw_rows"]:,}**
- Original columns: **8**

## Data-quality findings

| Issue | Rows |
| --- | ---: |
| Exact duplicate rows detected | {counts["raw_duplicate_rows"]:,} |
| Missing descriptions | {counts["raw_missing_descriptions"]:,} |
| Missing customer IDs | {counts["raw_missing_customer_ids"]:,} |
| Negative quantities (returns/cancellations) | {counts["raw_negative_quantities"]:,} |
| Zero quantities | {counts["raw_zero_quantities"]:,} |
| Negative unit prices | {counts["raw_negative_prices"]:,} |
| Zero unit prices | {counts["raw_zero_prices"]:,} |

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
| General cleaned transaction file | {counts["cleaned_general_rows"]:,} |
| Customer-ready positive-sales file | {counts["customer_ready_rows"]:,} |
| Duplicate rows removed | {counts["duplicate_rows_removed"]:,} |
| Malformed required-field rows removed | {counts["rows_with_malformed_required_fields"]:,} |
| Negative-price rows removed | {counts["negative_price_rows_removed"]:,} |
| Unknown-customer rows retained in general file | {counts["unknown_customer_rows"]:,} |
| Unknown-product rows retained in general file | {counts["unknown_product_rows"]:,} |
| Returns/cancellations retained and classified | {counts["return_or_cancellation_rows"]:,} |
| Zero-price rows retained and flagged | {counts["zero_price_rows_retained"]:,} |

## Limitations

The dataset does not contain customer age, so later customer segmentation will
use recency, purchase frequency, monetary value, geography, and product
behavior rather than age-based segments.
"""
    report_path.write_text(report, encoding="utf-8")


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {args.input}. "
            "Download the UCI Online Retail workbook first."
        )

    raw = pd.read_excel(args.input, engine="openpyxl")
    cleaned, customer_ready, metrics, counts = clean_retail_data(raw)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.report_dir.mkdir(parents=True, exist_ok=True)
    cleaned_path = args.output_dir / "online_retail_cleaned.csv"
    customer_path = args.output_dir / "online_retail_customer_ready.csv"
    metrics_path = args.report_dir / "task_1_data_quality_summary.csv"
    cleaned.to_csv(cleaned_path, index=False)
    customer_ready.to_csv(customer_path, index=False)
    pd.DataFrame(metrics).to_csv(metrics_path, index=False)
    write_report(
        args.report_dir / "task_1_data_quality_report.md", counts, args.input
    )
    (args.report_dir / "task_1_counts.json").write_text(
        json.dumps(counts, indent=2), encoding="utf-8"
    )

    print(json.dumps(counts, indent=2))
    print(f"Wrote {cleaned_path}")
    print(f"Wrote {customer_path}")
    print(f"Wrote {metrics_path}")


if __name__ == "__main__":
    main()