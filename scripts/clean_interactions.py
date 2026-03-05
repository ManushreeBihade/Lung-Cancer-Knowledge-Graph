import pandas as pd

INPUT_FILE = "data/interactions.csv"
OUTPUT_FILE = "data/interactions_cleaned.csv"

# Load
df = pd.read_csv(INPUT_FILE)

print("Original rows:", len(df))

# ----------------------------
# Basic Cleaning
# ----------------------------

# Strip whitespace
df["gene_1"] = df["gene_1"].astype(str).str.strip()
df["gene_2"] = df["gene_2"].astype(str).str.strip()
df["relation"] = df["relation"].astype(str).str.strip()
df["PMID"] = df["PMID"].astype(str).str.strip()

# Remove null or empty values
df = df.dropna()
df = df[(df["gene_1"] != "") & (df["gene_2"] != "") & (df["relation"] != "")]

# ----------------------------
# Remove Self-Loops
# ----------------------------

df = df[df["gene_1"] != df["gene_2"]]

# ----------------------------
# Remove '+' entities (e.g., CD133+)
# ----------------------------

df = df[~df["gene_1"].str.contains(r"\+", regex=True)]
df = df[~df["gene_2"].str.contains(r"\+", regex=True)]

# ----------------------------
# Remove very short meaningless relations
# (e.g., single-word fragments like "inhibition")
# ----------------------------

df = df[df["relation"].str.len() > 3]

# ----------------------------
# Drop exact duplicate rows
# ----------------------------

df = df.drop_duplicates()

print("Rows after cleaning:", len(df))

# Save cleaned file
df.to_csv(OUTPUT_FILE, index=False)

print("Cleaned file saved as:", OUTPUT_FILE)