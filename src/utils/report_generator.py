import json
import os
import pandas as pd
from datetime import datetime


def ensure_reports_folder():
    """Create reports folder if it does not exist."""
    os.makedirs("reports", exist_ok=True)


def save_json_report(report):
    """Save full data quality report as JSON."""
    ensure_reports_folder()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reports/data_quality_report_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return file_path


def save_csv_summary(report):
    """Save check result summary as CSV."""
    ensure_reports_folder()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reports/data_quality_summary_{timestamp}.csv"

    rows = []

    for result in report["check_results"]:
        rows.append({
            "checked_at": report["checked_at"],
            "dataset_path": report["dataset_path"],
            "total_rows": report["total_rows"],
            "total_columns": report["total_columns"],
            "health_score": report["health_summary"]["health_score"],
            "health_status": report["health_summary"]["health_status"],
            "check_name": result["check_name"],
            "status": result["status"],
            "issue_count": result["issue_count"],
            "details": str(result["details"])
        })

    df = pd.DataFrame(rows)
    df.to_csv(file_path, index=False)

    return file_path


def save_reports(report):
    """Save both JSON and CSV reports."""
    json_path = save_json_report(report)
    csv_path = save_csv_summary(report)

    return {
        "json_report": json_path,
        "csv_summary": csv_path
    }