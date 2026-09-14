# CODSOFT Data Analytics Internship — Task 1

## Data Cleaning & Preprocessing

This project imports the UCI Online Retail dataset, checks its quality, cleans
the data with Pandas, and exports a cleaned CSV file.

## What this project completed

- Inspected the dataset structure
- Checked missing values
- Detected duplicate records
- Checked inconsistent values and data types
- Removed exact duplicates
- Handled missing descriptions and customer IDs
- Corrected date, numeric, and text fields
- Identified returns and cancellations
- Removed invalid negative prices
- Calculated total value for each transaction
- Exported a cleaned dataset

## Files

- `task_1_data_cleaning.py` — the Python cleaning program
- `reports/task_1_data_quality_report.md` — explanation of findings and cleaning decisions
- `reports/task_1_data_quality_summary.csv` — quality metrics
- `data/cleaned_sample_100.csv` — small preview that opens easily

The complete cleaned dataset is available in the project workspace at:

`data/processed/online_retail_cleaned.csv`

It is large, so it is better to download it rather than preview it in a
browser. The report and Python program contain the complete results.

## How to run the program

From the project root:

```bash
python task_1_data_cleaning.py
```

The program reads the original UCI Online Retail workbook and creates the
cleaned files in the output folders.


> Preprocessing using Python and Pandas. I inspected missing values, duplicate
> records, inconsistent data, data types, returns, and invalid prices, then
> created a cleaned dataset for further analysis.
>
> GitHub: [paste your repository link here]
>
> #codsoft #internship #dataanalytics
