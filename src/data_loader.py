import pandas as pd


def load_projects():
    file_path = "data/PAIMANA_April_2026_Raw_Projects.csv"

    df = pd.read_csv(file_path)

    return df


if __name__ == "__main__":
    df = load_projects()

    print("Number of rows:", len(df))
    print("Number of columns:", len(df.columns))
    print("Duplicate rows:", df.duplicated().sum())
    print("\nMissing values:")
    print(df.isnull().sum())