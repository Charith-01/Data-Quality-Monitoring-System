import os
import sys
import tempfile

import pandas as pd


# Allow tests to access the project root
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from src.checks.data_quality_checker import (
    run_data_quality_checks
)


RECRUITMENT_COLUMNS = [
    "candidate_id",
    "candidate_name",
    "email",
    "phone",
    "job_id",
    "job_title",
    "application_date",
    "status",
    "experience_years",
    "expected_salary",
    "source"
]


def create_temp_csv(dataframe):
    """
    Save a DataFrame as a temporary CSV file.

    Returns the temporary file path.
    """

    temporary_file = tempfile.NamedTemporaryFile(
        suffix=".csv",
        delete=False
    )

    temporary_file.close()

    dataframe.to_csv(
        temporary_file.name,
        index=False
    )

    return temporary_file.name


def get_check_result(report, check_name):
    """
    Find one check result using its check name.
    """

    for result in report["check_results"]:

        if result["check_name"] == check_name:
            return result

    return None


def create_clean_recruitment_dataframe():
    """
    Create a clean recruitment dataset.
    """

    return pd.DataFrame([
        {
            "candidate_id": "CAND001",
            "candidate_name": "Nimal Perera",
            "email": "nimal@example.com",
            "phone": "0771234567",
            "job_id": "JOB001",
            "job_title": "Data Analyst",
            "application_date": "2026-07-01",
            "status": "Pending",
            "experience_years": 3,
            "expected_salary": 150000,
            "source": "LinkedIn"
        },
        {
            "candidate_id": "CAND002",
            "candidate_name": "Kamal Silva",
            "email": "kamal@example.com",
            "phone": "0719876543",
            "job_id": "JOB002",
            "job_title": "Software Engineer",
            "application_date": "2026-07-02",
            "status": "Shortlisted",
            "experience_years": 5,
            "expected_salary": 200000,
            "source": "Company Website"
        }
    ])


def test_clean_recruitment_dataset():
    """
    Clean recruitment dataset should have no failed
    recruitment-specific checks.
    """

    dataframe = create_clean_recruitment_dataframe()

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        failed_checks = [
            result
            for result in report["check_results"]
            if result["status"] == "Failed"
        ]

        assert len(failed_checks) == 0

        assert report[
            "health_summary"
        ]["health_score"] >= 90

        assert report[
            "health_summary"
        ]["health_status"] == "Excellent"

    finally:

        os.remove(
            file_path
        )


def test_dirty_recruitment_dataset():
    """
    Dirty recruitment data should produce failed checks.
    """

    dataframe = pd.DataFrame([
        {
            "candidate_id": "CAND001",
            "candidate_name": "",
            "email": "invalid-email",
            "phone": "12345",
            "job_id": "JOB001",
            "job_title": "Data Analyst",
            "application_date": "wrong-date",
            "status": "Selected",
            "experience_years": -3,
            "expected_salary": "unknown",
            "source": "UnknownSource"
        },
        {
            "candidate_id": "CAND001",
            "candidate_name": "",
            "email": "invalid-email",
            "phone": "12345",
            "job_id": "JOB001",
            "job_title": "Data Analyst",
            "application_date": "wrong-date",
            "status": "Selected",
            "experience_years": -3,
            "expected_salary": "unknown",
            "source": "UnknownSource"
        }
    ])

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        health = report[
            "health_summary"
        ]

        assert health["failed_checks"] > 0

        assert health["total_issues"] > 0

        assert health["health_score"] < 90

        failed_check_names = [
            result["check_name"]
            for result in report["check_results"]
            if result["status"] == "Failed"
        ]

        assert "Missing Values Check" in failed_check_names
        assert "Unique Columns Check" in failed_check_names
        assert "Email Format Check" in failed_check_names
        assert "Phone Format Check" in failed_check_names
        assert "Status Validation Check" in failed_check_names
        assert "Source Validation Check" in failed_check_names
        assert "Numeric Range Check" in failed_check_names

    finally:

        os.remove(
            file_path
        )


def test_general_dataset_only_runs_general_checks():
    """
    General dataset should not run recruitment-specific checks.
    """

    dataframe = pd.DataFrame([
        {
            "product_id": "P001",
            "product_name": "Laptop",
            "price": 250000
        },
        {
            "product_id": "P002",
            "product_name": "Monitor",
            "price": 80000
        }
    ])

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="General Dataset"
        )

        check_names = [
            result["check_name"]
            for result in report["check_results"]
        ]

        assert "Email Format Check" not in check_names
        assert "Phone Format Check" not in check_names
        assert "Status Validation Check" not in check_names
        assert "Source Validation Check" not in check_names
        assert "Numeric Range Check" not in check_names

    finally:

        os.remove(
            file_path
        )


def test_missing_required_columns():
    """
    Recruitment dataset with missing columns should fail
    the required columns check without crashing.
    """

    dataframe = pd.DataFrame([
        {
            "candidate_id": "CAND001",
            "candidate_name": "Nimal Perera",
            "job_id": "JOB001"
        }
    ])

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        required_check = get_check_result(
            report,
            "Required Columns Check"
        )

        assert required_check is not None

        assert required_check[
            "status"
        ] == "Failed"

        assert required_check[
            "issue_count"
        ] > 0

        assert "email" in required_check[
            "details"
        ]

        assert "phone" in required_check[
            "details"
        ]

        assert "status" in required_check[
            "details"
        ]

    finally:

        os.remove(
            file_path
        )


def test_duplicate_rows_counted_once():
    """
    Duplicate rows should be checked only once.
    """

    clean_row = {
        "candidate_id": "CAND001",
        "candidate_name": "Nimal Perera",
        "email": "nimal@example.com",
        "phone": "0771234567",
        "job_id": "JOB001",
        "job_title": "Data Analyst",
        "application_date": "2026-07-01",
        "status": "Pending",
        "experience_years": 3,
        "expected_salary": 150000,
        "source": "LinkedIn"
    }

    dataframe = pd.DataFrame([
        clean_row,
        clean_row
    ])

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        duplicate_checks = [
            result
            for result in report["check_results"]
            if "Duplicate Rows" in result["check_name"]
        ]

        assert len(
            duplicate_checks
        ) == 1

        assert duplicate_checks[
            0
        ]["status"] == "Failed"

        assert duplicate_checks[
            0
        ]["issue_count"] == 1

    finally:

        os.remove(
            file_path
        )

def test_invalid_numeric_values():
    """
    Invalid numeric values should fail the numeric range check.
    """

    dataframe = create_clean_recruitment_dataframe()

    # Convert numeric columns to object type so invalid text
    # values can be inserted for testing.
    dataframe["experience_years"] = (
        dataframe["experience_years"]
        .astype(object)
    )

    dataframe["expected_salary"] = (
        dataframe["expected_salary"]
        .astype(object)
    )

    dataframe.loc[
        0,
        "experience_years"
    ] = "abc"

    dataframe.loc[
        1,
        "expected_salary"
    ] = "unknown"

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        numeric_check = get_check_result(
            report,
            "Numeric Range Check"
        )

        assert numeric_check is not None

        assert numeric_check[
            "status"
        ] == "Failed"

        assert numeric_check[
            "issue_count"
        ] >= 2

    finally:

        os.remove(
            file_path
        )


def test_empty_dataset_with_headers():
    """
    Header-only CSV should not crash the monitoring system.
    """

    dataframe = pd.DataFrame(
        columns=RECRUITMENT_COLUMNS
    )

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        assert report[
            "total_rows"
        ] == 0

        assert report[
            "total_columns"
        ] == len(
            RECRUITMENT_COLUMNS
        )

        assert "health_summary" in report
        assert "check_results" in report

    finally:

        os.remove(
            file_path
        )


def test_report_contains_required_metadata():
    """
    Generated report should contain all required metadata.
    """

    dataframe = create_clean_recruitment_dataframe()

    file_path = create_temp_csv(
        dataframe
    )

    try:

        report = run_data_quality_checks(
            file_path,
            dataset_type="Recruitment Dataset"
        )

        assert "dataset_path" in report
        assert "dataset_type" in report
        assert "checked_at" in report
        assert "total_rows" in report
        assert "total_columns" in report
        assert "health_summary" in report
        assert "check_results" in report

    finally:

        os.remove(
            file_path
        )