import pandas as pd

from data_loader import load_projects


def calculate_risk(df):
    # ---------------------------------------------------------
    # 1. Cost Escalation
    # ---------------------------------------------------------
    df["cost_escalation_pct"] = (
        (df["revised_cost_crore"] - df["original_cost_crore"])
        / df["original_cost_crore"]
    ) * 100

    # Avoid invalid values caused by zero original cost
    df["cost_escalation_pct"] = df["cost_escalation_pct"].replace(
        [float("inf"), -float("inf")], 0
    )

    # ---------------------------------------------------------
    # 2. Expenditure Percentage
    # ---------------------------------------------------------
    df["expenditure_pct"] = (
        df["cumulative_expenditure_crore"]
        / df["revised_cost_crore"]
    ) * 100

    df["expenditure_pct"] = df["expenditure_pct"].replace(
        [float("inf"), -float("inf")], 0
    )

    # ---------------------------------------------------------
    # 3. Cost Risk Score
    # ---------------------------------------------------------
    df["cost_risk_score"] = 0

    df.loc[df["cost_escalation_pct"] > 5, "cost_risk_score"] = 10
    df.loc[df["cost_escalation_pct"] > 15, "cost_risk_score"] = 20
    df.loc[df["cost_escalation_pct"] > 30, "cost_risk_score"] = 30

    # ---------------------------------------------------------
    # 4. Physical Progress Risk Score
    # ---------------------------------------------------------
    df["progress_risk_score"] = 0

    df.loc[df["physical_progress_pct"] < 75, "progress_risk_score"] = 10
    df.loc[df["physical_progress_pct"] < 50, "progress_risk_score"] = 20
    df.loc[df["physical_progress_pct"] < 25, "progress_risk_score"] = 30

    # ---------------------------------------------------------
    # 5. Expenditure vs Physical Progress Risk
    # ---------------------------------------------------------
    #
    # If expenditure is significantly ahead of physical progress,
    # the project may require attention.
    #
    # Difference:
    # expenditure percentage - physical progress percentage
    #
    df["expenditure_progress_gap"] = (
        df["expenditure_pct"] - df["physical_progress_pct"]
    )

    df["expenditure_risk_score"] = 0

    df.loc[
        df["expenditure_progress_gap"] > 20,
        "expenditure_risk_score"
    ] = 10

    df.loc[
        df["expenditure_progress_gap"] > 40,
        "expenditure_risk_score"
    ] = 20

    # ---------------------------------------------------------
    # 6. Schedule Risk Score
    # ---------------------------------------------------------
    df["revised_target_completion_date"] = pd.to_datetime(
        df["revised_target_completion_date"],
        errors="coerce",
        format="mixed"
    )

    report_date = pd.Timestamp("2026-04-30")

    df["schedule_risk_score"] = 0

    df.loc[
        df["revised_target_completion_date"] < report_date,
        "schedule_risk_score"
    ] = 10

    # ---------------------------------------------------------
    # 7. Total Risk Score
    # ---------------------------------------------------------
    #
    # Maximum:
    # Cost       = 30
    # Progress   = 30
    # Expenditure= 20
    # Schedule   = 10
    #
    # Maximum total = 90
    #
    df["raw_risk_score"] = (
        df["cost_risk_score"]
        + df["progress_risk_score"]
        + df["expenditure_risk_score"]
        + df["schedule_risk_score"]
    )

    # Convert to 0-100 scale
    df["risk_score"] = (
        df["raw_risk_score"] / 90
    ) * 100

    df["risk_score"] = df["risk_score"].round(2)

    # ---------------------------------------------------------
    # 8. Risk Level
    # ---------------------------------------------------------
    df["risk_level"] = "Low"

    df.loc[df["risk_score"] >= 30, "risk_level"] = "Medium"
    df.loc[df["risk_score"] >= 60, "risk_level"] = "High"

    # ---------------------------------------------------------
    # 9. Early Warning Flags
    # ---------------------------------------------------------
    warnings = []

    for _, row in df.iterrows():

        project_warnings = []

        if row["cost_escalation_pct"] > 15:
            project_warnings.append("High Cost Escalation")

        if row["physical_progress_pct"] < 25:
            project_warnings.append("Low Physical Progress")

        if row["expenditure_progress_gap"] > 40:
            project_warnings.append(
                "Expenditure Significantly Ahead of Progress"
            )

        if (
            pd.notna(row["revised_target_completion_date"])
            and row["revised_target_completion_date"] < report_date
        ):
            project_warnings.append("Target Date Passed")

        warnings.append(" | ".join(project_warnings))

    df["early_warning"] = warnings

    return df


def main():

    # Load project data
    df = load_projects()

    # Calculate risk
    df = calculate_risk(df)

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------
    print("\n===== APRIL 2026 PROJECT RISK SUMMARY =====")

    print("\nTotal Projects:")
    print(len(df))

    print("\nRisk Level:")
    print(df["risk_level"].value_counts())

    print("\nAverage Risk Score:")
    print(round(df["risk_score"].mean(), 2))

    print("\nProjects with Early Warnings:")
    print((df["early_warning"] != "").sum())

    # ---------------------------------------------------------
    # Top 10 Highest Risk Projects
    # ---------------------------------------------------------
    print("\nTop 10 Highest Risk Projects:")

    top_projects = df.sort_values(
        by="risk_score",
        ascending=False
    ).head(10)

    print(
        top_projects[
            [
                "project_name",
                "risk_score",
                "risk_level",
                "cost_escalation_pct",
                "physical_progress_pct",
                "expenditure_pct",
                "expenditure_progress_gap",
                "early_warning"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()