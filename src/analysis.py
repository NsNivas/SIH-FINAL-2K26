from data_loader import load_projects


def projects_by_agency():
    df = load_projects()

    agency_counts = df["agency"].value_counts()

    return agency_counts


def projects_by_state():
    df = load_projects()

    state_counts = df["state"].value_counts()

    return state_counts

def project_cost_analysis():
    df = load_projects()

    total_original_cost = df["original_cost_crore"].sum()
    total_revised_cost = df["revised_cost_crore"].sum()
    total_cost_increase = total_revised_cost - total_original_cost

    return {
        "total_original_cost": total_original_cost,
        "total_revised_cost": total_revised_cost,
        "total_cost_increase": total_cost_increase
    }

def expenditure_analysis():
    df = load_projects()

    total_expenditure = df["cumulative_expenditure_crore"].sum()

    return total_expenditure


if __name__ == "__main__":
    agency_result = projects_by_agency()

    print("Projects by Agency:")
    print(agency_result)

    state_result = projects_by_state()

    print("\nProjects by State:")
    print(state_result)

    cost_result = project_cost_analysis()

    print("\nProject Cost Analysis:")
    print("Total Original Cost:",
          cost_result["total_original_cost"], "crore")

    print("Total Revised Cost:",
          cost_result["total_revised_cost"], "crore")

    print("Total Cost Increase:",
          cost_result["total_cost_increase"], "crore")


    expenditure_result = expenditure_analysis()

    print("\nExpenditure Analysis:")
    print("Total Cumulative Expenditure:",
          expenditure_result, "crore")