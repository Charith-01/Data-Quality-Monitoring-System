import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Allow Python to access project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.checks.data_quality_checker import run_data_quality_checks
from src.utils.report_generator import save_reports
from src.alerts.alert_manager import save_alerts


st.set_page_config(
    page_title="Data Quality Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)


def read_csv_with_fallback(file_path):
    """Read CSV using multiple possible encodings."""
    encodings = ["utf-8", "utf-8-sig", "latin1", "ISO-8859-1", "cp1252"]

    for encoding in encodings:
        try:
            return pd.read_csv(file_path, dtype=str, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise Exception("Unable to preview CSV file due to encoding issue.")


st.title("📊 Data Quality Monitoring Dashboard")
st.write("Automated system to monitor data integrity, reliability, and quality issues.")


# Sidebar
st.sidebar.header("Dataset Selection")

dataset_type = st.sidebar.selectbox(
    "Select Dataset Type",
    ["General Dataset", "Recruitment Dataset"],
    index=1
)

uploaded_file = st.sidebar.file_uploader("Upload Raw CSV Dataset", type=["csv"])

default_file_path = "data/raw/recruitment_data.csv"

st.sidebar.info(
    "Use General Dataset for any CSV file. "
    "Use Recruitment Dataset only for candidate/recruitment data."
)

if uploaded_file is not None:
    temp_file_path = "data/processed/uploaded_dataset.csv"

    os.makedirs("data/processed", exist_ok=True)

    with open(temp_file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    file_path = temp_file_path
    st.sidebar.success("Dataset uploaded successfully.")
else:
    file_path = default_file_path
    st.sidebar.info("Using default recruitment dataset.")


# Dataset preview before running checks
st.subheader("Selected Dataset Preview")

try:
    preview_df = read_csv_with_fallback(file_path)

    st.write(f"**Selected File:** `{file_path}`")
    st.write(f"**Selected Dataset Type:** `{dataset_type}`")
    st.write(f"**Rows:** {preview_df.shape[0]} | **Columns:** {preview_df.shape[1]}")

    st.write("**Detected Columns:**")
    st.write(list(preview_df.columns))

    st.dataframe(preview_df.head(10), use_container_width=True)

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
            col for col in expected_columns
            if col not in preview_df.columns
        ]

        if missing_preview_columns:
            st.warning(
                "This file does not fully match the recruitment dataset structure. "
                "Missing expected columns: "
                + ", ".join(missing_preview_columns)
            )

except Exception as e:
    st.error(f"Could not preview dataset: {e}")


if st.sidebar.button("Run Data Quality Checks"):
    try:
        report = run_data_quality_checks(file_path, dataset_type=dataset_type)
        saved_files = save_reports(report)
        alert_result = save_alerts(report)

        # Notification popup
        if alert_result["alert_count"] > 0:
            st.toast(
                f"⚠️ {alert_result['alert_count']} data quality alert(s) generated!",
                icon="⚠️"
            )
        else:
            st.toast(
                "✅ No data quality alerts generated.",
                icon="✅"
            )

        health = report["health_summary"]

        st.write("---")

        st.subheader("Overall Data Health Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Health Score", f"{health['health_score']}%")
        col2.metric("Health Status", health["health_status"])
        col3.metric("Failed Checks", health["failed_checks"])
        col4.metric("Total Issues", health["total_issues"])

        st.write("---")

        st.subheader("Dataset Information")

        col5, col6, col7 = st.columns(3)

        col5.metric("Total Rows", report["total_rows"])
        col6.metric("Total Columns", report["total_columns"])
        col7.metric("Total Checks", health["total_checks"])

        st.write(f"**Dataset Path:** {report['dataset_path']}")
        st.write(f"**Dataset Type:** {report['dataset_type']}")
        st.write(f"**Checked At:** {report['checked_at']}")

        st.write("---")

        st.subheader("Data Quality Alerts")

        if health["health_status"] == "Excellent":
            st.success("Excellent: Dataset quality is very good.")
        elif health["health_status"] == "Good":
            st.info("Good: Dataset has minor quality issues.")
        elif health["health_status"] == "Warning":
            st.warning("Warning: Dataset has several quality issues that need attention.")
        else:
            st.error("Poor: Dataset has serious data quality issues. Immediate review is recommended.")

        failed_checks = [
            result for result in report["check_results"]
            if result["status"] == "Failed"
        ]

        if failed_checks:
            for check in failed_checks:
                st.error(f"{check['check_name']} failed with {check['issue_count']} issue(s).")
        else:
            st.success("All checks passed successfully.")

        st.write("---")

        st.subheader("Check Results Summary")

        results_df = pd.DataFrame(report["check_results"])

        st.dataframe(
            results_df[["check_name", "status", "issue_count"]],
            use_container_width=True
        )

        st.write("---")

        st.subheader("Data Quality Visualizations")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            status_counts = results_df["status"].value_counts().reset_index()
            status_counts.columns = ["status", "count"]

            fig_status = px.pie(
                status_counts,
                names="status",
                values="count",
                title="Check Status Distribution"
            )

            st.plotly_chart(fig_status, use_container_width=True)

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

            fig_issues.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_issues, use_container_width=True)

        st.subheader("Overall Health Score Gauge")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health["health_score"],
            title={"text": "Data Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "white"},
                "steps": [
                    {"range": [0, 50], "color": "#ff4b4b"},
                    {"range": [50, 75], "color": "#ffa500"},
                    {"range": [75, 90], "color": "#f0e442"},
                    {"range": [90, 100], "color": "#00cc96"}
                ]
            }
        ))

        st.plotly_chart(fig_gauge, use_container_width=True)

        st.write("---")

        st.subheader("Detailed Issue Information")

        for result in report["check_results"]:
            with st.expander(result["check_name"]):
                st.write(f"**Status:** {result['status']}")
                st.write(f"**Issue Count:** {result['issue_count']}")
                st.write("**Details:**")
                st.write(result["details"])

        st.write("---")

        st.subheader("Generated Report Files")

        st.success(f"JSON Report saved: {saved_files['json_report']}")
        st.success(f"CSV Summary saved: {saved_files['csv_summary']}")

        st.write("---")

        st.subheader("Alert Log")

        if alert_result["alert_count"] > 0:
            st.warning(f"{alert_result['alert_count']} alert(s) generated.")
            st.write(f"**Alert file saved:** `{alert_result['alert_file']}`")

            alert_df = pd.DataFrame(alert_result["alerts"])
            st.dataframe(alert_df, use_container_width=True)

            st.info(
                "These alerts are also saved into the alert log file for future tracking."
            )
        else:
            st.success("No alerts generated. All checks passed.")

    except Exception as e:
        st.error(f"Error while running data quality checks: {e}")

else:
    st.info("Click **Run Data Quality Checks** from the sidebar to start monitoring.")