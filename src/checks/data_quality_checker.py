import pandas as pd  # read and check CSV data
from datetime import datetime  # save checked date and time
import sys  # help Python find files from other folders
import os  # help Python find files from other folders


# Allow Python to import project folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

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
    """Load CSV dataset."""
    try:
        return pd.read_csv(
            file_path,
            dtype={
                "phone": str,
                "candidate_id": str,
                "job_id": str
            }
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading file: {e}")


def check_required_columns(df):
    """Check whether all required columns exist."""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    return {
        "check_name": "Required Columns Check",
        "status": "Failed" if missing_columns else "Passed",
        "issue_count": len(missing_columns),
        "details": missing_columns
    }


def check_missing_values(df):
    """Check missing values in mandatory fields."""
    issues = {}

    for col in MANDATORY_FIELDS:
        if col in df.columns:
            missing_count = (
                df[col].isna().sum()
                + (df[col].astype(str).str.strip() == "").sum()
            )

            if missing_count > 0:
                issues[col] = int(missing_count)

    return {
        "check_name": "Missing Values Check",
        "status": "Failed" if issues else "Passed",
        "issue_count": sum(issues.values()),
        "details": issues
    }


def check_duplicate_rows(df):
    """Check duplicate rows."""
    duplicate_count = df.duplicated().sum()

    return {
        "check_name": "Duplicate Rows Check",
        "status": "Failed" if duplicate_count > 0 else "Passed",
        "issue_count": int(duplicate_count),
        "details": f"{duplicate_count} duplicate rows found"
    }


def check_unique_columns(df):
    """Check uniqueness for key columns like candidate_id."""
    issues = {}

    for col in UNIQUE_COLUMNS:
        if col in df.columns:
            duplicate_count = df[col].duplicated().sum()

            if duplicate_count > 0:
                issues[col] = int(duplicate_count)

    return {
        "check_name": "Unique Columns Check",
        "status": "Failed" if issues else "Passed",
        "issue_count": sum(issues.values()),
        "details": issues
    }


def check_email_format(df):
    """Check email format."""
    if "email" not in df.columns:
        return {
            "check_name": "Email Format Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "email column not found"
        }

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    invalid_emails = df[~df["email"].astype(str).str.match(email_pattern, na=False)]

    return {
        "check_name": "Email Format Check",
        "status": "Failed" if len(invalid_emails) > 0 else "Passed",
        "issue_count": len(invalid_emails),
        "details": invalid_emails[["candidate_id", "email"]].to_dict(orient="records")
        if "candidate_id" in df.columns else invalid_emails["email"].tolist()
    }


def check_phone_format(df):
    """Check Sri Lankan phone number format."""
    if "phone" not in df.columns:
        return {
            "check_name": "Phone Format Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "phone column not found"
        }

    phone_pattern = r"^0\d{9}$"
    invalid_phones = df[~df["phone"].astype(str).str.match(phone_pattern, na=False)]

    return {
        "check_name": "Phone Format Check",
        "status": "Failed" if len(invalid_phones) > 0 else "Passed",
        "issue_count": len(invalid_phones),
        "details": invalid_phones[["candidate_id", "phone"]].to_dict(orient="records")
        if "candidate_id" in df.columns else invalid_phones["phone"].tolist()
    }


def check_valid_status(df):
    """Check allowed application status values."""
    if "status" not in df.columns:
        return {
            "check_name": "Status Validation Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "status column not found"
        }

    invalid_status = df[~df["status"].isin(VALID_STATUS_VALUES)]

    return {
        "check_name": "Status Validation Check",
        "status": "Failed" if len(invalid_status) > 0 else "Passed",
        "issue_count": len(invalid_status),
        "details": invalid_status[["candidate_id", "status"]].to_dict(orient="records")
        if "candidate_id" in df.columns else invalid_status["status"].tolist()
    }


def check_valid_source(df):
    """Check allowed recruitment source values."""
    if "source" not in df.columns:
        return {
            "check_name": "Source Validation Check",
            "status": "Skipped",
            "issue_count": 0,
            "details": "source column not found"
        }

    invalid_sources = df[~df["source"].isin(VALID_SOURCES)]

    return {
        "check_name": "Source Validation Check",
        "status": "Failed" if len(invalid_sources) > 0 else "Passed",
        "issue_count": len(invalid_sources),
        "details": invalid_sources[["candidate_id", "source"]].to_dict(orient="records")
        if "candidate_id" in df.columns else invalid_sources["source"].tolist()
    }


def check_numeric_ranges(df):
    """Check numeric columns are inside allowed ranges."""
    issues = {}

    for col, rules in NUMERIC_RULES.items():
        if col in df.columns:
            numeric_col = pd.to_numeric(df[col], errors="coerce")

            invalid_rows = df[
                (numeric_col < rules["min"])
                | (numeric_col > rules["max"])
                | (numeric_col.isna())
            ]

            if len(invalid_rows) > 0:
                issues[col] = {
                    "issue_count": len(invalid_rows),
                    "invalid_values": invalid_rows[[col]].to_dict(orient="records")
                }

    total_issues = sum(item["issue_count"] for item in issues.values())

    return {
        "check_name": "Numeric Range Check",
        "status": "Failed" if total_issues > 0 else "Passed",
        "issue_count": total_issues,
        "details": issues
    }


def calculate_health_score(results):
    """Calculate data health score out of 100."""
    total_checks = len(results)
    failed_checks = sum(1 for result in results if result["status"] == "Failed")
    total_issues = sum(result["issue_count"] for result in results)

    score = 100 - (failed_checks * 10) - min(total_issues, 30)
    score = max(score, 0)

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
    """Run recruitment-specific quality checks."""
    recruitment_results = [
        check_required_columns(df),
        check_missing_values(df),
        check_duplicate_rows(df),
        check_unique_columns(df),
        check_email_format(df),
        check_phone_format(df),
        check_valid_status(df),
        check_valid_source(df),
        check_numeric_ranges(df)
    ]

    return recruitment_results


def run_data_quality_checks(file_path):
    """Run general and recruitment-specific data quality checks."""
    df = load_data(file_path)

    # General checks work for any dataset structure
    general_results = run_general_quality_checks(df)

    # Recruitment-specific checks work best for recruitment dataset structure
    recruitment_results = run_recruitment_quality_checks(df)

    # Combine both result groups
    results = general_results + recruitment_results

    health_summary = calculate_health_score(results)

    return {
        "dataset_path": file_path,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "health_summary": health_summary,
        "check_results": results
    }


if __name__ == "__main__":
    file_path = "data/raw/recruitment_data.csv"
    report = run_data_quality_checks(file_path)

    saved_files = save_reports(report)

    print("\nDATA QUALITY CHECK REPORT")
    print("=" * 40)
    print(f"Dataset: {report['dataset_path']}")
    print(f"Checked At: {report['checked_at']}")
    print(f"Rows: {report['total_rows']}")
    print(f"Columns: {report['total_columns']}")
    print(f"Health Score: {report['health_summary']['health_score']}%")
    print(f"Health Status: {report['health_summary']['health_status']}")
    print("=" * 40)

    for result in report["check_results"]:
        print(f"\n{result['check_name']}")
        print(f"Status: {result['status']}")
        print(f"Issues: {result['issue_count']}")
        print(f"Details: {result['details']}")

    print("\nREPORT FILES GENERATED")
    print("=" * 40)
    print(f"JSON Report: {saved_files['json_report']}")
    print(f"CSV Summary: {saved_files['csv_summary']}")