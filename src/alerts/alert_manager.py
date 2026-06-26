import os
import pandas as pd
from datetime import datetime


def ensure_alerts_folder():
    """Create alerts folder if it does not exist."""
    os.makedirs("alerts", exist_ok=True)


def get_severity(issue_count):
    """Assign severity level based on issue count."""
    if issue_count >= 10:
        return "Critical"
    elif issue_count >= 5:
        return "High"
    elif issue_count >= 1:
        return "Medium"
    else:
        return "Low"


def generate_alerts(report):
    """Generate alert records for failed data quality checks."""
    alerts = []

    for result in report["check_results"]:
        if result["status"] == "Failed":
            issue_count = result["issue_count"]
            severity = get_severity(issue_count)

            alerts.append({
                "alert_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "dataset_path": report["dataset_path"],
                "dataset_type": report.get("dataset_type", "Unknown"),
                "check_name": result["check_name"],
                "issue_count": issue_count,
                "severity": severity,
                "message": f"{result['check_name']} failed with {issue_count} issue(s)."
            })

    return alerts


def save_alerts(report):
    """Save alert records to CSV file."""
    ensure_alerts_folder()

    alerts = generate_alerts(report)

    if not alerts:
        return {
            "alert_file": None,
            "alert_count": 0,
            "alerts": []
        }

    alert_file_path = "alerts/data_quality_alerts.csv"

    new_alerts_df = pd.DataFrame(alerts)

    if os.path.exists(alert_file_path):
        existing_alerts_df = pd.read_csv(alert_file_path)
        final_alerts_df = pd.concat(
            [existing_alerts_df, new_alerts_df],
            ignore_index=True
        )
    else:
        final_alerts_df = new_alerts_df

    final_alerts_df.to_csv(alert_file_path, index=False)

    return {
        "alert_file": alert_file_path,
        "alert_count": len(alerts),
        "alerts": alerts
    }