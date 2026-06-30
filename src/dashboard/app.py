import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os


# Allow Python to access project root
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)


from src.checks.data_quality_checker import run_data_quality_checks
from src.checks.data_profiler import generate_data_profile
from src.utils.report_generator import save_reports
from src.alerts.alert_manager import save_alerts
from src.history.history_manager import save_history, load_history


st.set_page_config(
    page_title="Data Quality Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)


def read_csv_with_fallback(file_path):
    """
    Read a CSV file using multiple possible encodings.
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
                dtype=str,
                encoding=encoding
            )

        except UnicodeDecodeError:
            continue

    raise Exception(
        "Unable to read the CSV file due to an encoding issue."
    )


def read_file_bytes(file_path):
    """
    Read a generated file as bytes for download buttons.
    """

    if not file_path:
        return None

    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as file:
        return file.read()


st.title("📊 Data Quality Monitoring Dashboard")

st.write(
    "Automated system to monitor data integrity, "
    "reliability, and quality issues."
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.header("Dataset Selection")


dataset_type = st.sidebar.selectbox(
    "Select Dataset Type",
    [
        "General Dataset",
        "Recruitment Dataset"
    ],
    index=1
)


uploaded_file = st.sidebar.file_uploader(
    "Upload Raw CSV Dataset",
    type=["csv"]
)


default_file_path = "data/raw/recruitment_data.csv"


st.sidebar.info(
    "Use General Dataset for any CSV file. "
    "Use Recruitment Dataset only for candidate or recruitment data."
)


if uploaded_file is not None:

    temp_file_path = "data/processed/uploaded_dataset.csv"

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    with open(temp_file_path, "wb") as file:
        file.write(
            uploaded_file.getbuffer()
        )

    file_path = temp_file_path

    st.sidebar.success(
        "Dataset uploaded successfully."
    )

else:

    file_path = default_file_path

    st.sidebar.info(
        "Using default recruitment dataset."
    )


# ---------------------------------------------------------
# Dataset Preview
# ---------------------------------------------------------

st.subheader("Selected Dataset Preview")


preview_df = None


try:

    preview_df = read_csv_with_fallback(
        file_path
    )

    st.write(
        f"**Selected File:** `{file_path}`"
    )

    st.write(
        f"**Selected Dataset Type:** `{dataset_type}`"
    )

    st.write(
        f"**Rows:** {preview_df.shape[0]} | "
        f"**Columns:** {preview_df.shape[1]}"
    )

    st.write("**Detected Columns:**")

    st.write(
        list(preview_df.columns)
    )

    st.dataframe(
        preview_df.head(10),
        use_container_width=True
    )

    if dataset_type == "Recruitment Dataset":

        expected_columns = [
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

        missing_preview_columns = [
            column
            for column in expected_columns
            if column not in preview_df.columns
        ]

        if missing_preview_columns:

            st.warning(
                "This file does not fully match the recruitment "
                "dataset structure. Missing expected columns: "
                + ", ".join(missing_preview_columns)
            )

except Exception as error:

    st.error(
        f"Could not preview dataset: {error}"
    )


# ---------------------------------------------------------
# Run Checks
# ---------------------------------------------------------

if st.sidebar.button("Run Data Quality Checks"):

    try:

        if preview_df is None:
            preview_df = read_csv_with_fallback(
                file_path
            )

        report = run_data_quality_checks(
            file_path,
            dataset_type=dataset_type
        )

        profile = generate_data_profile(
            preview_df
        )

        saved_files = save_reports(
            report
        )

        alert_result = save_alerts(
            report
        )

        history_result = save_history(
            report
        )

        if alert_result["alert_count"] > 0:

            st.toast(
                f"{alert_result['alert_count']} "
                "data quality alert(s) generated!",
                icon="⚠️"
            )

        else:

            st.toast(
                "No data quality alerts generated.",
                icon="✅"
            )

        health = report["health_summary"]

        st.write("---")


        # -------------------------------------------------
        # Health Summary
        # -------------------------------------------------

        st.subheader("Overall Data Health Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Health Score",
            f"{health['health_score']}%"
        )

        col2.metric(
            "Health Status",
            health["health_status"]
        )

        col3.metric(
            "Failed Checks",
            health["failed_checks"]
        )

        col4.metric(
            "Total Issues",
            health["total_issues"]
        )

        st.write("---")


        # -------------------------------------------------
        # Dataset Information
        # -------------------------------------------------

        st.subheader("Dataset Information")

        col5, col6, col7 = st.columns(3)

        col5.metric(
            "Total Rows",
            report["total_rows"]
        )

        col6.metric(
            "Total Columns",
            report["total_columns"]
        )

        col7.metric(
            "Total Checks",
            health["total_checks"]
        )

        st.write(
            f"**Dataset Path:** {report['dataset_path']}"
        )

        st.write(
            f"**Dataset Type:** {report['dataset_type']}"
        )

        st.write(
            f"**Checked At:** {report['checked_at']}"
        )

        st.write("---")


        # -------------------------------------------------
        # Dataset Profiling
        # -------------------------------------------------

        st.subheader("Dataset Profiling Summary")

        profile_summary = profile["dataset_summary"]

        profile_col1, profile_col2, profile_col3 = st.columns(3)

        profile_col1.metric(
            "Duplicate Rows",
            profile_summary["duplicate_rows"]
        )

        profile_col2.metric(
            "Duplicate Percentage",
            f"{profile_summary['duplicate_percentage']}%"
        )

        profile_col3.metric(
            "Total Missing Values",
            profile_summary["total_missing_values"]
        )

        profile_col4, profile_col5, profile_col6 = st.columns(3)

        profile_col4.metric(
            "Overall Missing Percentage",
            f"{profile_summary['overall_missing_percentage']}%"
        )

        profile_col5.metric(
            "Profiled Columns",
            profile_summary["total_columns"]
        )

        profile_col6.metric(
            "Profiled Rows",
            profile_summary["total_rows"]
        )

        st.write("---")

        st.subheader("Column-Level Data Profile")

        column_profile_df = pd.DataFrame(
            profile["column_profiles"]
        )

        st.dataframe(
            column_profile_df,
            use_container_width=True
        )

        st.caption(
            "The profile shows detected types, missing values, "
            "unique values, common values, and numeric statistics."
        )

        st.write("---")


        # -------------------------------------------------
        # Alerts
        # -------------------------------------------------

        st.subheader("Data Quality Alerts")

        if health["health_status"] == "Excellent":

            st.success(
                "Excellent: Dataset quality is very good."
            )

        elif health["health_status"] == "Good":

            st.info(
                "Good: Dataset has minor quality issues."
            )

        elif health["health_status"] == "Warning":

            st.warning(
                "Warning: Dataset has several quality issues "
                "that need attention."
            )

        else:

            st.error(
                "Poor: Dataset has serious data quality issues. "
                "Immediate review is recommended."
            )

        failed_checks = [
            result
            for result in report["check_results"]
            if result["status"] == "Failed"
        ]

        if failed_checks:

            for check in failed_checks:

                st.error(
                    f"{check['check_name']} failed with "
                    f"{check['issue_count']} issue(s)."
                )

        else:

            st.success(
                "All checks passed successfully."
            )

        st.write("---")


        # -------------------------------------------------
        # Check Results
        # -------------------------------------------------

        st.subheader("Check Results Summary")

        results_df = pd.DataFrame(
            report["check_results"]
        )

        st.dataframe(
            results_df[
                [
                    "check_name",
                    "status",
                    "issue_count"
                ]
            ],
            use_container_width=True
        )

        st.write("---")


        # -------------------------------------------------
        # Charts
        # -------------------------------------------------

        st.subheader("Data Quality Visualizations")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            status_counts = (
                results_df["status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "status",
                "count"
            ]

            fig_status = px.pie(
                status_counts,
                names="status",
                values="count",
                title="Check Status Distribution"
            )

            st.plotly_chart(
                fig_status,
                use_container_width=True
            )

        with chart_col2:

            fig_issues = px.bar(
                results_df,
                x="check_name",
                y="issue_count",
                title="Issue Count by Check Type",
                labels={
                    "check_name": "Check Type",
                    "issue_count": "Issue Count"
                }
            )

            fig_issues.update_layout(
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig_issues,
                use_container_width=True
            )

        st.subheader("Overall Health Score Gauge")

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=health["health_score"],
                title={
                    "text": "Data Health Score"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "white"
                    },
                    "steps": [
                        {
                            "range": [0, 50],
                            "color": "#ff4b4b"
                        },
                        {
                            "range": [50, 75],
                            "color": "#ffa500"
                        },
                        {
                            "range": [75, 90],
                            "color": "#f0e442"
                        },
                        {
                            "range": [90, 100],
                            "color": "#00cc96"
                        }
                    ]
                }
            )
        )

        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )

        st.write("---")


        # -------------------------------------------------
        # Detailed Issues
        # -------------------------------------------------

        st.subheader("Detailed Issue Information")

        for result in report["check_results"]:

            with st.expander(
                result["check_name"]
            ):

                st.write(
                    f"**Status:** {result['status']}"
                )

                st.write(
                    f"**Issue Count:** {result['issue_count']}"
                )

                st.write("**Details:**")

                st.write(
                    result["details"]
                )

        st.write("---")


        # -------------------------------------------------
        # Reports
        # -------------------------------------------------

        st.subheader("Generated Report Files")

        json_report_path = saved_files["json_report"]
        csv_summary_path = saved_files["csv_summary"]

        st.success(
            f"JSON Report saved: {json_report_path}"
        )

        st.success(
            f"CSV Summary saved: {csv_summary_path}"
        )

        json_report_data = read_file_bytes(
            json_report_path
        )

        csv_summary_data = read_file_bytes(
            csv_summary_path
        )

        download_col1, download_col2 = st.columns(2)

        with download_col1:

            if json_report_data is not None:

                st.download_button(
                    label="⬇ Download JSON Report",
                    data=json_report_data,
                    file_name=os.path.basename(
                        json_report_path
                    ),
                    mime="application/json",
                    use_container_width=True
                )

        with download_col2:

            if csv_summary_data is not None:

                st.download_button(
                    label="⬇ Download CSV Summary",
                    data=csv_summary_data,
                    file_name=os.path.basename(
                        csv_summary_path
                    ),
                    mime="text/csv",
                    use_container_width=True
                )

        st.write("---")


        # -------------------------------------------------
        # Monitoring History and Trend Charts
        # -------------------------------------------------

        st.subheader("Monitoring History")

        history_df = load_history()

        if not history_df.empty:

            st.write(
                f"**Total monitoring runs:** "
                f"{history_result['total_history_records']}"
            )

            st.dataframe(
                history_df,
                use_container_width=True
            )

            st.info(
                f"Monitoring history saved to: "
                f"`{history_result['history_file']}`"
            )

            st.subheader("Data Quality Score Trend")

            if len(history_df) >= 2:

                trend_df = history_df.copy()

                trend_df["checked_at"] = pd.to_datetime(
                    trend_df["checked_at"],
                    errors="coerce"
                )

                trend_df["health_score"] = pd.to_numeric(
                    trend_df["health_score"],
                    errors="coerce"
                )

                trend_df["total_issues"] = pd.to_numeric(
                    trend_df["total_issues"],
                    errors="coerce"
                )

                trend_df = trend_df.dropna(
                    subset=[
                        "checked_at",
                        "health_score",
                        "total_issues"
                    ]
                )

                trend_df = trend_df.sort_values(
                    by="checked_at"
                )

                if len(trend_df) >= 2:

                    fig_trend = px.line(
                        trend_df,
                        x="checked_at",
                        y="health_score",
                        markers=True,
                        title="Data Health Score Over Time",
                        labels={
                            "checked_at": "Monitoring Time",
                            "health_score": "Health Score"
                        }
                    )

                    fig_trend.update_yaxes(
                        range=[0, 100]
                    )

                    st.plotly_chart(
                        fig_trend,
                        use_container_width=True
                    )

                    st.subheader("Data Quality Issue Trend")

                    fig_issue_trend = px.line(
                        trend_df,
                        x="checked_at",
                        y="total_issues",
                        markers=True,
                        title="Total Data Quality Issues Over Time",
                        labels={
                            "checked_at": "Monitoring Time",
                            "total_issues": "Total Issues"
                        }
                    )

                    st.plotly_chart(
                        fig_issue_trend,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "The history records do not contain enough "
                        "valid values to create trend charts."
                    )

            else:

                st.info(
                    "Run the monitoring system at least twice "
                    "to display trend charts."
                )

        else:

            st.info(
                "No monitoring history is available yet."
            )

        st.write("---")


        # -------------------------------------------------
        # Alert Log
        # -------------------------------------------------

        st.subheader("Alert Log")

        if alert_result["alert_count"] > 0:

            st.warning(
                f"{alert_result['alert_count']} alert(s) generated."
            )

            st.write(
                f"**Alert file saved:** "
                f"`{alert_result['alert_file']}`"
            )

            alert_df = pd.DataFrame(
                alert_result["alerts"]
            )

            st.dataframe(
                alert_df,
                use_container_width=True
            )

            alert_file_path = alert_result["alert_file"]

            alert_file_data = read_file_bytes(
                alert_file_path
            )

            if alert_file_data is not None:

                st.download_button(
                    label="⬇ Download Alert Log",
                    data=alert_file_data,
                    file_name=os.path.basename(
                        alert_file_path
                    ),
                    mime="text/csv"
                )

            st.info(
                "These alerts are saved for future tracking."
            )

        else:

            st.success(
                "No alerts generated. All checks passed."
            )

    except Exception as error:

        st.error(
            "Error while running data quality checks: "
            f"{error}"
        )

else:

    st.info(
        "Click **Run Data Quality Checks** "
        "from the sidebar to start monitoring."
    )