import pandas as pd
import numpy as np

df = pd.read_csv("data/dirty-customers.csv")

print("Dataset Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# ==========================================
# STEP 2: MISSING VALUES ANALYSIS
# ==========================================

print("\n" + "=" * 50)
print("MISSING VALUES ANALYSIS")
print("=" * 50)

missing = df.isnull().sum()

print("\nMissing values in each column:")
print(missing)

print("\nTotal missing values:", missing.sum())

print("\nMissing value percentage:")
missing_percentage = (df.isnull().sum() / len(df)) * 100
print(missing_percentage.round(2))

# ==========================================
# STEP 3: DUPLICATE RECORD ANALYSIS
# ==========================================

print("\n" + "=" * 50)
print("DUPLICATE RECORD ANALYSIS")
print("=" * 50)

duplicate_count = df.duplicated().sum()

print("\nTotal duplicate rows:", duplicate_count)

if duplicate_count > 0:
    print("\nDuplicate records:")
    print(df[df.duplicated(keep=False)])
else:
    print("\nNo duplicate records found.")

# ==========================================
# STEP 4: INCONSISTENT DATA ANALYSIS
# ==========================================

print("\n" + "=" * 50)
print("INCONSISTENT DATA ANALYSIS")
print("=" * 50)

# Country values
print("\n--- COUNTRY VALUES ---")
print(df["country"].value_counts(dropna=False))

# Segment values
print("\n--- SEGMENT VALUES ---")
print(df["segment"].value_counts(dropna=False))

# Active status values
print("\n--- IS_ACTIVE VALUES ---")
print(df["is_active"].value_counts(dropna=False))

# Spend values
print("\n--- SPEND SAMPLE ---")
print(df["spend"].value_counts(dropna=False).head(20))

# Signup date values
print("\n--- SIGNUP DATE SAMPLE ---")
print(df["signup_date"].value_counts(dropna=False).head(20))


# ==========================================
# STEP 5: DATA CLEANING
# ==========================================

print("\n" + "=" * 50)
print("DATA CLEANING")
print("=" * 50)

# Make a copy of the original dataset
cleaned_df = df.copy()

# ------------------------------------------
# 5.1 Remove duplicate records
# ------------------------------------------

before_duplicates = len(cleaned_df)

cleaned_df = cleaned_df.drop_duplicates()

after_duplicates = len(cleaned_df)

print("\nDuplicate rows removed:",
      before_duplicates - after_duplicates)


# ------------------------------------------
# 5.2 Clean text columns
# ------------------------------------------

text_columns = [
    "customer_id",
    "full_name",
    "email",
    "country",
    "segment"
]

for column in text_columns:
    cleaned_df[column] = cleaned_df[column].astype("string").str.strip()


# Clean customer names
cleaned_df["full_name"] = cleaned_df["full_name"].str.title()


# ------------------------------------------
# 5.3 Standardize Country
# ------------------------------------------

country_mapping = {
    "us": "United States",
    "usa": "United States",
    "u.s.": "United States",
    "united states": "United States",

    "uk": "United Kingdom",
    "gb": "United Kingdom",
    "united kingdom": "United Kingdom",

    "de": "Germany",
    "germany": "Germany",

    "fr": "France",
    "france": "France",

    "br": "Brazil",
    "brazil": "Brazil"
}

cleaned_df["country"] = (
    cleaned_df["country"]
    .str.lower()
    .replace(country_mapping)
)

print("\nCountry values after cleaning:")
print(cleaned_df["country"].value_counts())


# ------------------------------------------
# 5.4 Standardize Customer Segment
# ------------------------------------------

segment_mapping = {
    "smb": "Small Business",
    "small business": "Small Business",

    "ent": "Enterprise",
    "enterprise": "Enterprise",

    "midmarket": "Mid-Market",
    "mid-market": "Mid-Market",
    "mid market": "Mid-Market",

    "consumer": "Consumer"
}

cleaned_df["segment"] = (
    cleaned_df["segment"]
    .str.lower()
    .replace(segment_mapping)
)

print("\nSegment values after cleaning:")
print(cleaned_df["segment"].value_counts())


# ------------------------------------------
# 5.5 Standardize Active Status
# ------------------------------------------

active_mapping = {
    "y": True,
    "yes": True,
    "true": True,
    "1": True,

    "n": False,
    "no": False,
    "false": False,
    "0": False
}

cleaned_df["is_active"] = (
    cleaned_df["is_active"]
    .str.lower()
    .replace(active_mapping)
)

cleaned_df["is_active"] = cleaned_df["is_active"].astype("boolean")

print("\nActive status after cleaning:")
print(cleaned_df["is_active"].value_counts(dropna=False))

# ==========================================
# STEP 6: CLEAN SPEND COLUMN
# ==========================================

print("\n" + "=" * 50)
print("SPEND COLUMN CLEANING")
print("=" * 50)

# Convert special missing-value representations to NaN
cleaned_df["spend"] = (
    cleaned_df["spend"]
    .astype("string")
    .str.strip()
    .replace({
        "-": np.nan,
        "none": np.nan,
        "-999": np.nan
    })
)

# Remove currency symbols and text
cleaned_df["spend"] = (
    cleaned_df["spend"]
    .str.replace("$", "", regex=False)
    .str.replace("USD", "", regex=False)
    .str.strip()
)

# Convert to numeric
cleaned_df["spend"] = pd.to_numeric(
    cleaned_df["spend"],
    errors="coerce"
)

print("\nSpend data type after cleaning:")
print(cleaned_df["spend"].dtype)

print("\nMissing values in spend after cleaning:")
print(cleaned_df["spend"].isnull().sum())

print("\nSample cleaned spend values:")
print(cleaned_df["spend"].head(20))


# ==========================================
# STEP 7: CLEAN SIGNUP DATE
# ==========================================

print("\n" + "=" * 50)
print("SIGNUP DATE CLEANING")
print("=" * 50)

# Make a clean copy of the original date column
date_series = (
    cleaned_df["signup_date"]
    .astype("string")
    .str.strip()
)

# Convert known invalid values to missing
date_series = date_series.replace({
    "": pd.NA,
    "none": pd.NA,
    "-": pd.NA,
    "-999": pd.NA
})

# Parse mixed date formats
cleaned_df["signup_date"] = pd.to_datetime(
    date_series,
    format="mixed",
    errors="coerce"
)

print("\nSignup date data type:")
print(cleaned_df["signup_date"].dtype)

print("\nMissing signup dates:")
print(cleaned_df["signup_date"].isna().sum())

print("\nSample cleaned dates:")
print(cleaned_df["signup_date"].head(20))


# ==========================================
# STEP 8: EMAIL CLEANING & VALIDATION
# ==========================================

print("\n" + "=" * 50)
print("EMAIL CLEANING & VALIDATION")
print("=" * 50)

# Convert to string and remove extra spaces
cleaned_df["email"] = (
    cleaned_df["email"]
    .astype("string")
    .str.strip()
)

# Handle common missing representations
cleaned_df["email"] = cleaned_df["email"].replace({
    "": pd.NA,
    "none": pd.NA,
    "-": pd.NA
})

# Convert [at] / [AT] to @
cleaned_df["email"] = (
    cleaned_df["email"]
    .str.replace(r"\[at\]", "@", regex=True, case=False)
)

# Extract email from formats such as:
# Yuki <Yuki@example.com>
cleaned_df["email"] = (
    cleaned_df["email"]
    .str.extract(r"<([^<>@\s]+@[^<>@\s]+\.[^<>@\s]+)>", expand=False)
    .fillna(cleaned_df["email"])
)

# Validate email format
email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

invalid_email_mask = (
    cleaned_df["email"].notna()
    & ~cleaned_df["email"].str.match(email_pattern, na=False)
)

print("\nInvalid email count:", invalid_email_mask.sum())

print("\nInvalid email examples:")
print(cleaned_df.loc[invalid_email_mask, "email"].head(20))

# Mark genuinely invalid emails as missing
cleaned_df.loc[invalid_email_mask, "email"] = pd.NA

print("\nFinal missing emails:",
      cleaned_df["email"].isna().sum())

# ==========================================
# STEP 9: FINAL DATA TYPE CONVERSION
# ==========================================

print("\n" + "=" * 50)
print("FINAL DATA TYPE CONVERSION")
print("=" * 50)

# Convert customer_id and full_name to string
cleaned_df["customer_id"] = cleaned_df["customer_id"].astype("string")
cleaned_df["full_name"] = cleaned_df["full_name"].astype("string")

# Email remains string
cleaned_df["email"] = cleaned_df["email"].astype("string")

# Country and segment remain categorical text
cleaned_df["country"] = cleaned_df["country"].astype("string")
cleaned_df["segment"] = cleaned_df["segment"].astype("string")

# Spend is already numeric
cleaned_df["spend"] = pd.to_numeric(
    cleaned_df["spend"],
    errors="coerce"
)

# Signup date is already datetime
cleaned_df["signup_date"] = pd.to_datetime(
    cleaned_df["signup_date"],
    errors="coerce"
)

# Active status as boolean
cleaned_df["is_active"] = cleaned_df["is_active"].astype("boolean")


print("\nFinal Data Types:")
print(cleaned_df.dtypes)

print("\n" + "=" * 50)
print("FINAL MISSING VALUE CHECK")
print("=" * 50)

print(cleaned_df.isnull().sum())

print("\n" + "=" * 50)
print("FINAL DUPLICATE CHECK")
print("=" * 50)

print("Duplicate rows remaining:", cleaned_df.duplicated().sum())

print("\nFinal Dataset Shape:", cleaned_df.shape)

# ==========================================
# STEP 10: SAVE CLEANED DATASET
# ==========================================

import os

os.makedirs("cleaned_data", exist_ok=True)

output_path = "cleaned_data/cleaned_customers.csv"

cleaned_df.to_csv(output_path, index=False)

print("\n" + "=" * 50)
print("DATASET EXPORT")
print("=" * 50)
print("Cleaned dataset saved successfully!")
print("File:", output_path)
