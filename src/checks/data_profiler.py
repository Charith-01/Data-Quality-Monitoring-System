import pandas as pd


def calculate_dataset_summary(df):
    """
    Calculate overall dataset-level information.
    """

    total_rows = len(df)
    total_columns = len(df.columns)
    duplicate_rows = int(df.duplicated().sum())

    if total_rows > 0:
        duplicate_percentage = round(
            (duplicate_rows / total_rows) * 100,
            2
        )
    else:
        duplicate_percentage = 0.0

    total_cells = total_rows * total_columns
    total_missing_values = int(df.isna().sum().sum())

    if total_cells > 0:
        overall_missing_percentage = round(
            (total_missing_values / total_cells) * 100,
            2
        )
    else:
        overall_missing_percentage = 0.0

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": duplicate_percentage,
        "total_missing_values": total_missing_values,
        "overall_missing_percentage": overall_missing_percentage
    }


def detect_column_type(series, column_name=""):
    """
    Detect a user-friendly column type.
    """

    non_null_series = series.dropna()

    if non_null_series.empty:
        return "Empty"

    column_name_lower = column_name.lower()

    identifier_keywords = [
        "id",
        "phone",
        "mobile",
        "telephone",
        "postal",
        "zip",
        "code"
    ]

    if any(
        keyword in column_name_lower
        for keyword in identifier_keywords
    ):
        return "Identifier"

    if pd.api.types.is_bool_dtype(series):
        return "Boolean"

    if pd.api.types.is_integer_dtype(series):
        return "Integer"

    if pd.api.types.is_float_dtype(series):
        return "Decimal"

    if pd.api.types.is_numeric_dtype(series):
        return "Numeric"

    converted_numeric = pd.to_numeric(
        non_null_series,
        errors="coerce"
    )

    numeric_percentage = (
        converted_numeric.notna().mean() * 100
    )

    if numeric_percentage >= 90:
        return "Numeric Text"

    date_keywords = [
        "date",
        "time",
        "created",
        "updated",
        "timestamp"
    ]

    if any(
        keyword in column_name_lower
        for keyword in date_keywords
    ):
        converted_dates = pd.to_datetime(
            non_null_series,
            errors="coerce",
            format="mixed"
        )

        date_percentage = (
            converted_dates.notna().mean() * 100
        )

        if date_percentage >= 90:
            return "Date/Time Text"

    unique_count = non_null_series.nunique()

    if unique_count <= 20:
        return "Categorical"

    return "Text"


def calculate_numeric_statistics(series):
    """
    Calculate statistics for numeric columns.
    """

    numeric_series = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if numeric_series.empty:
        return {
            "minimum": None,
            "maximum": None,
            "average": None,
            "median": None
        }

    return {
        "minimum": round(float(numeric_series.min()), 2),
        "maximum": round(float(numeric_series.max()), 2),
        "average": round(float(numeric_series.mean()), 2),
        "median": round(float(numeric_series.median()), 2)
    }


def calculate_column_profile(df):
    """
    Create profiling information for every dataset column.
    """

    profiles = []
    total_rows = len(df)

    for column in df.columns:
        series = df[column]

        missing_count = int(
            series.isna().sum()
        )

        if total_rows > 0:
            missing_percentage = round(
                (missing_count / total_rows) * 100,
                2
            )
        else:
            missing_percentage = 0.0

        unique_values = int(
            series.nunique(dropna=True)
        )

        detected_type = detect_column_type(
            series,
            column
        )

        if detected_type in [
            "Integer",
            "Decimal",
            "Numeric",
            "Numeric Text"
        ]:
            statistics = calculate_numeric_statistics(
                series
            )
        else:
            statistics = {
                "minimum": None,
                "maximum": None,
                "average": None,
                "median": None
            }

        most_common_value = None
        most_common_count = 0

        non_null_series = series.dropna()

        if not non_null_series.empty:
            value_counts = (
                non_null_series
                .astype(str)
                .value_counts()
            )

            most_common_value = str(
                value_counts.index[0]
            )

            most_common_count = int(
                value_counts.iloc[0]
            )

        profiles.append({
            "column_name": column,
            "detected_type": detected_type,
            "pandas_data_type": str(series.dtype),
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
            "unique_values": unique_values,
            "most_common_value": most_common_value,
            "most_common_count": most_common_count,
            "minimum": statistics["minimum"],
            "maximum": statistics["maximum"],
            "average": statistics["average"],
            "median": statistics["median"]
        })

    return profiles


def generate_data_profile(df):
    """
    Generate complete dataset profile.
    """

    dataset_summary = calculate_dataset_summary(
        df
    )

    column_profiles = calculate_column_profile(
        df
    )

    return {
        "dataset_summary": dataset_summary,
        "column_profiles": column_profiles
    }


def load_csv_with_fallback(file_path):
    """
    Load CSV using multiple possible encodings.
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
                f"Error loading CSV file: {error}"
            )

    raise Exception(
        "Unable to read CSV file. "
        "Please check the file encoding."
    )


if __name__ == "__main__":

    file_path = "data/raw/recruitment_data.csv"

    try:
        dataframe = load_csv_with_fallback(
            file_path
        )

        profile = generate_data_profile(
            dataframe
        )

        print("\nDATASET SUMMARY")
        print("=" * 40)

        for key, value in profile["dataset_summary"].items():
            print(f"{key}: {value}")

        print("\nCOLUMN PROFILES")
        print("=" * 40)

        profile_df = pd.DataFrame(
            profile["column_profiles"]
        )

        print(
            profile_df.to_string(index=False)
        )

    except FileNotFoundError as error:
        print(error)

    except Exception as error:
        print(
            f"Error generating data profile: {error}"
        )