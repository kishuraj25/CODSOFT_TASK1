# CODSOFT Task 1 – Data Cleaning & Preprocessing

## 📌 Project Overview

This project is completed as part of the **CodSoft Data Analytics Internship – Task 1: Data Cleaning & Preprocessing**.

The objective of this task is to inspect a deliberately messy customer dataset, identify data-quality issues, clean and standardize the data using **Python and Pandas**, and export the cleaned dataset for further analysis.

---

## 🎯 Objectives

- Import and inspect the dataset
- Understand the dataset structure and data types
- Identify missing values
- Detect duplicate records
- Identify inconsistent categorical values
- Clean and standardize textual data
- Convert columns to appropriate data types
- Validate the cleaned dataset
- Export the cleaned dataset as a CSV file

---

## 📂 Dataset

The dataset contains customer-related information with the following columns:

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `full_name` | Customer's full name |
| `email` | Customer email address |
| `signup_date` | Customer registration date |
| `country` | Customer country |
| `spend` | Customer spending amount |
| `segment` | Customer business segment |
| `is_active` | Customer active status |

### Original Dataset

- **Rows:** 1000
- **Columns:** 8

---

## 🔍 Data Quality Issues Identified

The original dataset contained several data-quality problems.

### 1. Missing Values

Missing values were found in:

- `email`
- `signup_date`
- `spend`

**Total missing values identified initially:** 100

---

### 2. Duplicate Records

One duplicate record was identified and removed.

| Metric | Count |
|---|---:|
| Original Rows | 1000 |
| Duplicate Rows Removed | 1 |
| Final Rows | 999 |

---

### 3. Inconsistent Country Values

The `country` column contained multiple representations of the same country.

For example:

```text
US
usa
u.s.
United States
```

These representations were standardized to:

```text
United States
```

Similar standardization was performed for:

- United Kingdom
- Germany
- France
- Brazil

---

### 4. Inconsistent Customer Segments

Different representations were found in the `segment` column.

For example:

```text
SMB
smb
Small Business
```

These were standardized to:

```text
Small Business
```

The final standardized segments are:

- Enterprise
- Small Business
- Mid-Market
- Consumer

---

### 5. Inconsistent Active Status

The `is_active` column contained different representations such as:

```text
Y
yes
TRUE
1
N
no
FALSE
0
```

These values were converted into Boolean values:

```text
True
False
```

---

### 6. Inconsistent Spend Values

The `spend` column contained different representations such as:

```text
$100.66
USD 286.67
none
-
-999
```

Currency prefixes and invalid/missing representations were handled, and the column was converted to a numeric data type.

---

### 7. Inconsistent Date Formats

The `signup_date` column contained multiple date formats, including:

```text
2024-10-18
25 Jan 2025
Jun 26, 2024
02.09.2024
06/21/2023
```

These values were converted into a standard datetime format.

---

### 8. Invalid Email Values

Some email addresses contained invalid formatting, for example:

```text
Leilani@@example..com
Aisha@@example..com
ravi@@example..com
```

Recoverable formats such as:

```text
ravi[at]example.com
```

were corrected, while invalid/unrecoverable email values were treated as missing.

---

## 🧹 Data Cleaning Process

The following preprocessing steps were performed:

1. Loaded the CSV dataset using Pandas.
2. Inspected dataset shape, columns, data types, and sample records.
3. Checked for missing values.
4. Detected duplicate records.
5. Removed duplicate rows.
6. Removed unnecessary whitespace from text fields.
7. Standardized country names.
8. Standardized customer segments.
9. Converted active-status values to Boolean.
10. Cleaned currency and invalid values from the `spend` column.
11. Converted `spend` to numeric format.
12. Standardized multiple date formats.
13. Converted `signup_date` to datetime.
14. Validated email formats.
15. Converted invalid/unrecoverable email values to missing values.
16. Performed final data-type validation.
17. Performed final missing-value and duplicate checks.
18. Exported the cleaned dataset.

---

## 📊 Final Dataset

After preprocessing, the dataset contains:

| Metric | Result |
|---|---:|
| Original Rows | 1000 |
| Duplicate Rows Removed | 1 |
| Final Rows | 999 |
| Columns | 8 |
| Duplicate Rows Remaining | 0 |

### Final Data Types

```text
customer_id    string
full_name      string
email          string
signup_date    datetime
country        string
spend          Float64
segment        string
is_active      boolean
```

---

## 🔎 Remaining Missing Values

| Column | Missing Values |
|---|---:|
| `customer_id` | 0 |
| `full_name` | 0 |
| `email` | 45 |
| `signup_date` | 54 |
| `country` | 0 |
| `spend` | 73 |
| `segment` | 0 |
| `is_active` | 0 |

Unrecoverable missing information was retained as missing rather than assigning arbitrary values.

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**

---

## 📁 Project Structure

```text
CODSOFT_TASK1/
│
├── data/
│   └── dirty-customers.csv
│
├── cleaned_data/
│   └── cleaned_customers.csv
│
├── data_cleaning.py
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the Project Directory

```bash
cd CODSOFT_TASK1
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Data Cleaning Script

```bash
python data_cleaning.py
```

The cleaned dataset will be generated at:

```text
cleaned_data/cleaned_customers.csv
```

---

## 📤 Output

The final cleaned dataset is exported as:

```text
cleaned_data/cleaned_customers.csv
```

The cleaned dataset is ready for further data analysis and visualization.

---

## 📌 Internship Task

**Internship:** CodSoft Data Analytics Internship

**Task:** Task 1 – Data Cleaning & Preprocessing

**Tools:** Python, Pandas, NumPy, Matplotlib