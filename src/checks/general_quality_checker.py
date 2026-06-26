import pandas as pd


def check_general_missing_values(df):
    """Check missing values for all columns."""
    missing_counts = df.isna().sum()
    missing_percentages = (df.isna().mean() * 100).round(2)

    issues = {}

    for col in df.columns:
        if missing_counts[col] > 0:
            issues[col] = {
                "missing_count": int(missing_counts[col]),
                "missing_percentage": float(missing_percentages[col])
            }

    return {
        "check_name": "General Missing Values Check",
        "status": "Failed" if issues else "Passed",
        "issue_count": int(missing_counts.sum()),
        "details": issues
    }


def check_empty_columns(df):
    """Check columns that are fully empty."""
    empty_columns = []

    for col in df.columns:
        if df[col].isna().all():
            empty_columns.append(col)

    return {
        "check_name": "Empty Columns Check",
        "status": "Failed" if empty_columns else "Passed",
        "issue_count": len(empty_columns),
        "details": empty_columns
    }


def check_duplicate_rows_general(df):
    """Check duplicate rows for any dataset."""
    duplicate_count = df.duplicated().sum()

    return {
        "check_name": "General Duplicate Rows Check",
        "status": "Failed" if duplicate_count > 0 else "Passed",
        "issue_count": int(duplicate_count),
        "details": f"{duplicate_count} duplicate row(s) found"
    }


def check_column_data_types(df):
    """Show detected data types for all columns."""
    data_types = {
        col: str(dtype)
        for col, dtype in df.dtypes.items()
    }

    return {
        "check_name": "Column Data Types Check",
        "status": "Passed",
        "issue_count": 0,
        "details": data_types
    }


def check_high_missing_columns(df, threshold=50):
    """Check columns with missing percentage higher than threshold."""
    missing_percentages = df.isna().mean() * 100

    high_missing_columns = {}

    for col in df.columns:
        if missing_percentages[col] > threshold:
            high_missing_columns[col] = round(float(missing_percentages[col]), 2)

    return {
        "check_name": "High Missing Percentage Check",
        "status": "Failed" if high_missing_columns else "Passed",
        "issue_count": len(high_missing_columns),
        "details": high_missing_columns
    }


def check_negative_numeric_values(df):
    """Check negative values in numeric columns."""
    issues = {}

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for col in numeric_columns:
        negative_count = (df[col] < 0).sum()
        if negative_count > 0:
            issues[col] = int(negative_count)

    return {
        "check_name": "Negative Numeric Values Check",
        "status": "Failed" if issues else "Passed",
        "issue_count": sum(issues.values()),
        "details": issues
    }


def run_general_quality_checks(df):
    """Run general data quality checks for any dataset."""
    results = [
        check_general_missing_values(df),
        check_empty_columns(df),
        check_duplicate_rows_general(df),
        check_column_data_types(df),
        check_high_missing_columns(df),
        check_negative_numeric_values(df)
    ]

    return results