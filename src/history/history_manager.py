import os
import pandas as pd


HISTORY_FOLDER = "history"

HISTORY_FILE = os.path.join(
    HISTORY_FOLDER,
    "data_quality_history.csv"
)


HISTORY_COLUMNS = [
    "checked_at",
    "dataset_path",
    "dataset_type",
    "total_rows",
    "total_columns",
    "health_score",
    "health_status",
    "total_checks",
    "failed_checks",
    "total_issues"
]


def ensure_history_folder():
    """
    Create the history folder if it does not exist.
    """

    os.makedirs(
        HISTORY_FOLDER,
        exist_ok=True
    )


def create_history_record(report):
    """
    Create one monitoring-history record from a quality report.
    """

    health = report[
        "health_summary"
    ]

    return {
        "checked_at": report[
            "checked_at"
        ],
        "dataset_path": report[
            "dataset_path"
        ],
        "dataset_type": report.get(
            "dataset_type",
            "Unknown"
        ),
        "total_rows": report[
            "total_rows"
        ],
        "total_columns": report[
            "total_columns"
        ],
        "health_score": health[
            "health_score"
        ],
        "health_status": health[
            "health_status"
        ],
        "total_checks": health[
            "total_checks"
        ],
        "failed_checks": health[
            "failed_checks"
        ],
        "total_issues": health[
            "total_issues"
        ]
    }


def save_history(report):
    """
    Append the current monitoring run to the history CSV.
    """

    ensure_history_folder()

    history_record = (
        create_history_record(
            report
        )
    )

    new_history_df = pd.DataFrame(
        [history_record]
    )

    if os.path.exists(
        HISTORY_FILE
    ):

        try:

            existing_history_df = (
                pd.read_csv(
                    HISTORY_FILE
                )
            )

        except pd.errors.EmptyDataError:

            existing_history_df = (
                pd.DataFrame(
                    columns=HISTORY_COLUMNS
                )
            )

        history_df = pd.concat(
            [
                existing_history_df,
                new_history_df
            ],
            ignore_index=True
        )

    else:

        history_df = new_history_df

    history_df.to_csv(
        HISTORY_FILE,
        index=False
    )

    return {
        "history_file": HISTORY_FILE,
        "history_record": history_record,
        "total_history_records": len(
            history_df
        )
    }


def load_history():
    """
    Load all previous monitoring records.
    """

    if not os.path.exists(
        HISTORY_FILE
    ):

        return pd.DataFrame(
            columns=HISTORY_COLUMNS
        )

    try:

        history_df = pd.read_csv(
            HISTORY_FILE
        )

    except pd.errors.EmptyDataError:

        return pd.DataFrame(
            columns=HISTORY_COLUMNS
        )

    if "checked_at" in history_df.columns:

        history_df["checked_at"] = (
            pd.to_datetime(
                history_df[
                    "checked_at"
                ],
                errors="coerce"
            )
        )

        history_df = (
            history_df
            .sort_values(
                by="checked_at"
            )
            .reset_index(
                drop=True
            )
        )

    return history_df