from data_loader import load_projects


def projects_by_agency():
    df = load_projects()

    agency_counts = df["agency"].value_counts()

    return agency_counts


def projects_by_state():
    df = load_projects()

    state_counts = df["state"].value_counts()

    return state_counts


if __name__ == "__main__":
    agency_result = projects_by_agency()

    print("Projects by Agency:")
    print(agency_result)

    state_result = projects_by_state()

    print("\nProjects by State:")
    print(state_result)