from data_loader import load_projects


def calculate_risk():
    df = load_projects()

    return df


if __name__ == "__main__":
    df = calculate_risk()

    print("Total projects:", len(df))