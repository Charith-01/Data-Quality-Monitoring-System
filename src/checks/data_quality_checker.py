import pandas as pd
from datetime import datetime
import sys
import os


# Allow Python to import project folders
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)


from config.data_quality_rules import (
    REQUIRED_COLUMNS,
    MANDATORY_FIELDS,
    VALID_STATUS_VALUES,
    VALID_SOURCES,
    UNIQUE_COLUMNS,
    NUMERIC_RULES
)

from src.checks.general_quality_checker import run_general_quality_checks
from src.utils.report_generator import save_reports


def load_data(file_path):
    """
    Load a CSV dataset using multiple encoding options.
    """

    encodings = [
        "utf-8",
        "utf-8-sig",
        "latin1",
        "ISO-8859-1",
        "cp1252"
    ]

    for encoding in encodings:

        try:

            return pd.read_csv(
                file_path,
                dtype={
                    "phone": str,
                    "candidate_id": str,
                    "job_id": str
                },
                encoding=encoding
            )

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        except Exception as error:
            raise Exception(
                f"Error loading file: {error}"
            )

    raise Exception(
        "Unable to read CSV file. "
        "Please check the file encoding."
    )


def check_required_columns(df):
    """
    Check whether all required recruitment columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return {
        "check_name": "Required Columns Check",
        "status": "Failed" if missing_columns else "Passed",
        "issue_count": len(missing_columns),
        "details": missing_columns
    }


def check_missing_values(df):
    """
    Check missing values in mandatory recruitment fields.
    """

    issues = {}

    for column in MANDATORY_FIELDS:

        if column in df.columns:

            missing_count = (
                df[column].isna().sum()
                + (
                    df[column]
                    .astype(str)
                    .str.strip()
                    == ""
                ).sum()
            )

            if missing_count > 0:

                issues[column] = int(
                    missing_count
                )

    return {
        "check_name": "Missing Values Check",
        "status": "Failed" if issues else "Passed",
        "issue_count": sum(issues.values()),
        "details": issues
    }


def check_duplicate_rows(df):
    """
    Check duplicate rows.

    This function is kept for possible independent use.
    General checks already perform duplicate-row validation.
    """

    duplicate_count = int(
        df.duplicated().sum()
    )

    return {
        "check_name": "Duplicate Rows Check",
        "status": (
            "Failed"
            if duplicate_count > 0
            else "Passed"
        ),
        "issue_count": duplicate_count,
        "details": (
            f"{duplicate_count} duplicate rows found"
        )
    }


def check_unique_columns(df):
    """
    Check uniqueness of key columns such as candidate_id.
    """

    issues = {}

    for column in UNIQUE_COLUMNS:

        if column in df.columns:

            duplicate_count = int(
                df[column]
                .duplicated()
                .sum()
            )

            if duplicate_count > 0:

                issues[column] = duplicate_count

    return {
        "check_name": "Unique Columns Check",
        "status": "Failed" if issues else "Passed",
        "issue_count": sum(issues.values()),
        "details": issues
    }


def check_email_format(df):
    """
    Check recruitment email format.
    """

    if "email" not in df.columns:

        return {
            "check_name": "Email Format Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "email column not found"
        }

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    invalid_emails = df[
        ~df["email"]
        .astype(str)
        .str.match(
            email_pattern,
            na=False
        )
    ]

    if "candidate_id" in df.columns:

        details = invalid_emails[
            [
                "candidate_id",
                "email"
            ]
        ].to_dict(
            orient="records"
        )

    else:

        details = invalid_emails[
            "email"
        ].tolist()

    return {
        "check_name": "Email Format Check",
        "status": (
            "Failed"
            if len(invalid_emails) > 0
            else "Passed"
        ),
        "issue_count": len(invalid_emails),
        "details": details
    }


def check_phone_format(df):
    """
    Check Sri Lankan phone number format.
    """

    if "phone" not in df.columns:

        return {
            "check_name": "Phone Format Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "phone column not found"
        }

    phone_pattern = r"^0\d{9}$"

    invalid_phones = df[
        ~df["phone"]
        .astype(str)
        .str.match(
            phone_pattern,
            na=False
        )
    ]

    if "candidate_id" in df.columns:

        details = invalid_phones[
            [
                "candidate_id",
                "phone"
            ]
        ].to_dict(
            orient="records"
        )

    else:

        details = invalid_phones[
            "phone"
        ].tolist()

    return {
        "check_name": "Phone Format Check",
        "status": (
            "Failed"
            if len(invalid_phones) > 0
            else "Passed"
        ),
        "issue_count": len(invalid_phones),
        "details": details
    }


def check_valid_status(df):
    """
    Check allowed recruitment application status values.
    """

    if "status" not in df.columns:

        return {
            "check_name": "Status Validation Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "status column not found"
        }

    invalid_status = df[
        ~df["status"].isin(
            VALID_STATUS_VALUES
        )
    ]

    if "candidate_id" in df.columns:

        details = invalid_status[
            [
                "candidate_id",
                "status"
            ]
        ].to_dict(
            orient="records"
        )

    else:

        details = invalid_status[
            "status"
        ].tolist()

    return {
        "check_name": "Status Validation Check",
        "status": (
            "Failed"
            if len(invalid_status) > 0
            else "Passed"
        ),
        "issue_count": len(invalid_status),
        "details": details
    }


def check_valid_source(df):
    """
    Check allowed recruitment source values.
    """

    if "source" not in df.columns:

        return {
            "check_name": "Source Validation Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "source column not found"
        }

    invalid_sources = df[
        ~df["source"].isin(
            VALID_SOURCES
        )
    ]

    if "candidate_id" in df.columns:

        details = invalid_sources[
            [
                "candidate_id",
                "source"
            ]
        ].to_dict(
            orient="records"
        )

    else:

        details = invalid_sources[
            "source"
        ].tolist()

    return {
        "check_name": "Source Validation Check",
        "status": (
            "Failed"
            if len(invalid_sources) > 0
            else "Passed"
        ),
        "issue_count": len(invalid_sources),
        "details": details
    }


def check_numeric_ranges(df):
    """
    Check recruitment numeric values against configured ranges.
    """

    issues = {}

    for column, rules in NUMERIC_RULES.items():

        if column in df.columns:

            numeric_column = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            invalid_rows = df[
                (
                    numeric_column
                    < rules["min"]
                )
                |
                (
                    numeric_column
                    > rules["max"]
                )
                |
                numeric_column.isna()
            ]

            if len(invalid_rows) > 0:

                issues[column] = {
                    "issue_count": len(
                        invalid_rows
                    ),
                    "invalid_values": (
                        invalid_rows[
                            [column]
                        ]
                        .to_dict(
                            orient="records"
                        )
                    )
                }

    total_issues = sum(
        item["issue_count"]
        for item in issues.values()
    )

    return {
        "check_name": "Numeric Range Check",
        "status": (
            "Failed"
            if total_issues > 0
            else "Passed"
        ),
        "issue_count": total_issues,
        "details": issues
    }


def calculate_health_score(results):
    """
    Calculate an overall data health score out of 100.
    """

    total_checks = len(results)

    failed_checks = sum(
        1
        for result in results
        if result["status"] == "Failed"
    )

    total_issues = sum(
        result["issue_count"]
        for result in results
    )

    score = (
        100
        - (failed_checks * 10)
        - min(total_issues, 30)
    )

    score = max(
        score,
        0
    )

    if score >= 90:

        status = "Excellent"

    elif score >= 75:

        status = "Good"

    elif score >= 50:

        status = "Warning"

    else:

        status = "Poor"

    return {
        "health_score": score,
        "health_status": status,
        "total_checks": total_checks,
        "failed_checks": failed_checks,
        "total_issues": total_issues
    }


def run_recruitment_quality_checks(df):
    """
    Run recruitment-specific checks.

    Duplicate rows are excluded here because the general
    quality checker already checks duplicate rows.
    """

    recruitment_results = [
        check_required_columns(df),
        check_missing_values(df),
        check_unique_columns(df),
        check_email_format(df),
        check_phone_format(df),
        check_valid_status(df),
        check_valid_source(df),
        check_numeric_ranges(df)
    ]

    return recruitment_results


def run_data_quality_checks(
    file_path,
    dataset_type="Recruitment Dataset"
):
    """
    Run quality checks based on the selected dataset type.

    General Dataset:
        Run only general checks.

    Recruitment Dataset:
        Run general and recruitment-specific checks.
    """

    dataframe = load_data(
        file_path
    )

    general_results = run_general_quality_checks(
        dataframe
    )

    if dataset_type == "General Dataset":

        results = general_results

    elif dataset_type == "Recruitment Dataset":

        recruitment_results = (
            run_recruitment_quality_checks(
                dataframe
            )
        )

        results = (
            general_results
            + recruitment_results
        )

    else:

        results = general_results

    health_summary = calculate_health_score(
        results
    )

    return {
        "dataset_path": file_path,
        "dataset_type": dataset_type,
        "checked_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "total_rows": len(dataframe),
        "total_columns": len(
            dataframe.columns
        ),
        "health_summary": health_summary,
        "check_results": results
    }


if __name__ == "__main__":

    file_path = (
        "data/raw/recruitment_data.csv"
    )

    report = run_data_quality_checks(
        file_path,
        dataset_type="Recruitment Dataset"
    )

    saved_files = save_reports(
        report
    )

    print("\nDATA QUALITY CHECK REPORT")
    print("=" * 40)

    print(
        f"Dataset: "
        f"{report['dataset_path']}"
    )

    print(
        f"Dataset Type: "
        f"{report['dataset_type']}"
    )

    print(
        f"Checked At: "
        f"{report['checked_at']}"
    )

    print(
        f"Rows: "
        f"{report['total_rows']}"
    )

    print(
        f"Columns: "
        f"{report['total_columns']}"
    )

    print(
        f"Health Score: "
        f"{report['health_summary']['health_score']}%"
    )

    print(
        f"Health Status: "
        f"{report['health_summary']['health_status']}"
    )

    print("=" * 40)

    for result in report["check_results"]:

        print(
            f"\n{result['check_name']}"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )

        print(
            f"Issues: "
            f"{result['issue_count']}"
        )

        print(
            f"Details: "
            f"{result['details']}"
        )

    print("\nREPORT FILES GENERATED")
    print("=" * 40)

    print(
        f"JSON Report: "
        f"{saved_files['json_report']}"
    )

    print(
        f"CSV Summary: "
        f"{saved_files['csv_summary']}"
    )