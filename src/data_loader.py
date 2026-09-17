import pandas as pd

file_path = "data/PAIMANA_April_2026_Raw_Projects.csv"

df = pd.read_csv(file_path)

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))
print("\nColumns:")
print(df.columns.tolist())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nMissing values:")
print(df.isnull().sum())