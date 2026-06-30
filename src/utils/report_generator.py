import json
import os
from datetime import datetime

import pandas as pd


REPORTS_FOLDER = "reports"


def ensure_reports_folder():
    """
    Create the reports folder if it does not exist.
    """

    os.makedirs(
        REPORTS_FOLDER,
        exist_ok=True
    )


def create_summary_dataframe(report):
    """
    Convert data quality check results into a summary DataFrame.

    This DataFrame can be used for:
    - CSV file saving
    - Manual dashboard downloads
    """

    rows = []

    for result in report["check_results"]:

        rows.append({
            "checked_at": report["checked_at"],
            "dataset_path": report["dataset_path"],
            "dataset_type": report.get(
                "dataset_type",
                "Unknown"
            ),
            "total_rows": report["total_rows"],
            "total_columns": report["total_columns"],
            "health_score": report[
                "health_summary"
            ]["health_score"],
            "health_status": report[
                "health_summary"
            ]["health_status"],
            "total_checks": report[
                "health_summary"
            ]["total_checks"],
            "failed_checks": report[
                "health_summary"
            ]["failed_checks"],
            "total_issues": report[
                "health_summary"
            ]["total_issues"],
            "check_name": result["check_name"],
            "status": result["status"],
            "issue_count": result["issue_count"],
            "details": str(
                result["details"]
            )
        })

    return pd.DataFrame(
        rows
    )


def create_json_download_data(report):
    """
    Create JSON report content in memory.

    This does not save a file inside the reports folder.
    It returns bytes for Streamlit download_button.
    """

    json_text = json.dumps(
        report,
        indent=4,
        ensure_ascii=False,
        default=str
    )

    return json_text.encode(
        "utf-8"
    )


def create_csv_download_data(report):
    """
    Create CSV summary content in memory.

    This does not save a file inside the reports folder.
    It returns bytes for Streamlit download_button.
    """

    summary_df = create_summary_dataframe(
        report
    )

    csv_text = summary_df.to_csv(
        index=False
    )

    return csv_text.encode(
        "utf-8-sig"
    )


def save_json_report(report):
    """
    Save the full JSON report inside the reports folder.

    This function is intended for scheduled monitoring.
    """

    ensure_reports_folder()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = os.path.join(
        REPORTS_FOLDER,
        f"data_quality_report_{timestamp}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    return file_path


def save_csv_summary(report):
    """
    Save the CSV summary inside the reports folder.

    This function is intended for scheduled monitoring.
    """

    ensure_reports_folder()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = os.path.join(
        REPORTS_FOLDER,
        f"data_quality_summary_{timestamp}.csv"
    )

    summary_df = create_summary_dataframe(
        report
    )

    summary_df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    return file_path


def save_reports(report):
    """
    Save both JSON and CSV reports.

    Use this function only when reports must be
    automatically stored, such as scheduled monitoring.
    """

    json_path = save_json_report(
        report
    )

    csv_path = save_csv_summary(
        report
    )

    return {
        "json_report": json_path,
        "csv_summary": csv_path
    }