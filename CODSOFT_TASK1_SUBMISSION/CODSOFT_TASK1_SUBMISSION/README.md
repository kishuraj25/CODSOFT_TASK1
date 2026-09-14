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

## How to upload this to GitHub

1. Sign in to GitHub.
2. Create a new repository using the repository name required by CodSoft.
   If the email does not specify a different name, use the format
   `CODSOFT_TASKSNO` and replace `NO` with the required task number.
3. Open the new repository.
4. Select **Add file → Upload files**.
5. Upload the contents of this folder, including the README, Python file, and
   reports folder.
6. Click **Commit changes**.
7. Copy the repository URL. This is the link you will later paste into the
   CodSoft task submission form.

Do not upload passwords, GitHub tokens, or other private information.

## LinkedIn video checklist

Record a short screen video showing:

1. The GitHub repository and README
2. The Python cleaning file
3. The data-quality report
4. The final result counts:
   - 541,909 original rows
   - 5,268 duplicate rows removed
   - 536,639 cleaned rows

Add the GitHub repository link to the LinkedIn post and include:

`#codsoft #internship #dataanalytics`

## Suggested LinkedIn caption

> Completed Task 1 of my CodSoft Data Analytics Internship: Data Cleaning and
> Preprocessing using Python and Pandas. I inspected missing values, duplicate
> records, inconsistent data, data types, returns, and invalid prices, then
> created a cleaned dataset for further analysis.
>
> GitHub: [paste your repository link here]
>
> #codsoft #internship #dataanalytics