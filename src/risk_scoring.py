import pandas as pd
from data_loader import load_projects


def calculate_risk(df):
    """
    Calculate current risk score for April 2026 projects.

    Risk factors:
    1. Cost escalation
    2. Physical progress
    3. Expenditure level
    4. Schedule status
    """

    df = df.copy()

    # ---------------------------------------------------------
    # 1. COST ESCALATION
    # ---------------------------------------------------------

    df["cost_escalation_pct"] = (
        (df["revised_cost_crore"] - df["original_cost_crore"])
        / df["original_cost_crore"]
    ) * 100

    df["cost_escalation_pct"] = (
        df["cost_escalation_pct"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    # Cost risk score: maximum 30 points
    df["cost_risk_score"] = (
        df["cost_escalation_pct"]
        .apply(
            lambda x:
                30 if x > 30
                else 20 if x > 15
                else 10 if x > 5
                else 0
        )
    )

    # ---------------------------------------------------------
    # 2. PHYSICAL PROGRESS
    # ---------------------------------------------------------

    # Lower progress = higher current risk
    df["progress_risk_score"] = (
        df["physical_progress_pct"]
        .apply(
            lambda x:
                30 if x < 25
                else 20 if x < 50
                else 10 if x < 75
                else 0
        )
    )

    # ---------------------------------------------------------
    # 3. EXPENDITURE
    # ---------------------------------------------------------

    df["expenditure_pct"] = (
        df["cumulative_expenditure_crore"]
        / df["revised_cost_crore"]
    ) * 100

    df["expenditure_pct"] = (
        df["expenditure_pct"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    # ---------------------------------------------------------
    # 4. SCHEDULE STATUS
    # ---------------------------------------------------------

    today = pd.Timestamp("2026-04-30")

    df["revised_target_completion_date"] = pd.to_datetime(
        df["revised_target_completion_date"],
        errors="coerce"
    )

    df["schedule_risk_score"] = (
        df["revised_target_completion_date"]
        .apply(
            lambda date:
                10
                if pd.notna(date) and date < today
                else 0
        )
    )

    # ---------------------------------------------------------
    # 5. TOTAL RISK SCORE
    # ---------------------------------------------------------

    df["risk_score"] = (
        df["cost_risk_score"]
        + df["progress_risk_score"]
        + df["schedule_risk_score"]
    )

    # Maximum = 70 points
    # Convert to 100-point scale
    df["risk_score"] = (
        df["risk_score"] / 70
    ) * 100

    # ---------------------------------------------------------
    # 6. RISK LEVEL
    # ---------------------------------------------------------

    df["risk_level"] = df["risk_score"].apply(
        lambda x:
            "High" if x >= 60
            else "Medium" if x >= 30
            else "Low"
    )

    # ---------------------------------------------------------
    # 7. EARLY WARNING FLAGS
    # ---------------------------------------------------------

    def generate_warning(row):

        warnings = []

        if row["cost_escalation_pct"] > 15:
            warnings.append("High Cost Escalation")

        if row["physical_progress_pct"] < 25:
            warnings.append("Low Physical Progress")

        if (
            row["revised_target_completion_date"] < today
        ):
            warnings.append("Target Date Passed")

        if (
            row["expenditure_pct"] > 80
            and row["physical_progress_pct"] < 50
        ):
            warnings.append("High Expenditure with Low Progress")

        if not warnings:
            return "No Immediate Warning"

        return " | ".join(warnings)

    df["early_warning"] = df.apply(
        generate_warning,
        axis=1
    )

    return df


if __name__ == "__main__":

    # Load April 2026 project data
    projects = load_projects()

    # Calculate risk
    risk_data = calculate_risk(projects)

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n===== APRIL 2026 PROJECT RISK SUMMARY =====")

    print("\nTotal Projects:")
    print(len(risk_data))

    print("\nRisk Level:")
    print(risk_data["risk_level"].value_counts())

    print("\nAverage Risk Score:")
    print(round(risk_data["risk_score"].mean(), 2))

    print("\nProjects with Early Warnings:")
    warning_projects = (
        risk_data["early_warning"]
        != "No Immediate Warning"
    ).sum()

    print(warning_projects)

    print("\nTop 10 Highest Risk Projects:")

    top_risk = risk_data.sort_values(
        "risk_score",
        ascending=False
    ).head(10)

    print(
        top_risk[
            [
                "project_name",
                "risk_score",
                "risk_level",
                "early_warning"
            ]
        ].to_string(index=False)
    )