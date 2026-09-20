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


def cost_increase_analysis():
    df = load_projects()

    cost_increased = df[
        df["revised_cost_crore"] > df["original_cost_crore"]
    ]

    number_of_projects = len(cost_increased)

    total_cost_increase = (
        cost_increased["revised_cost_crore"]
        - cost_increased["original_cost_crore"]
    ).sum()

    percentage_of_projects = (
        number_of_projects / len(df)
    ) * 100

    return {
        "number_of_projects": number_of_projects,
        "total_cost_increase": total_cost_increase,
        "percentage_of_projects": percentage_of_projects
    }


def progress_category_analysis():
    df = load_projects()

    def categorize_progress(progress):
        if progress <= 25:
            return "Low"
        elif progress <= 50:
            return "Moderate"
        elif progress <= 75:
            return "Good"
        else:
            return "High"

    df["progress_category"] = df["physical_progress_pct"].apply(
        categorize_progress
    )

    progress_counts = df["progress_category"].value_counts()

    return progress_counts



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

    cost_increase_result = cost_increase_analysis()

    print("\nCost Increase Analysis:")
    print(
        "Projects with increased cost:",
        cost_increase_result["number_of_projects"]
    )

    print(
        "Total cost increase:",
        cost_increase_result["total_cost_increase"],
        "crore"
    )

    print(
        "Percentage of projects with increased cost:",
        cost_increase_result["percentage_of_projects"],
        "%"
    )


    progress_result = progress_category_analysis()
    print("\nProjects by Progress Category:")
    print(progress_result)