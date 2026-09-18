from data_loader import load_projects


def projects_by_agency():
    df = load_projects()

    agency_counts = df["agency"].value_counts()

    return agency_counts


if __name__ == "__main__":
    result = projects_by_agency()

    print("Projects by Agency:")
    print(result)