import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(
    os.getenv("SMTP_PORT", "587")
)

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME",
    ""
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD",
    ""
)

ALERT_RECIPIENT = os.getenv(
    "ALERT_RECIPIENT",
    ""
)

EMAIL_ALERTS_ENABLED = (
    os.getenv(
        "EMAIL_ALERTS_ENABLED",
        "false"
    )
    .strip()
    .lower()
    == "true"
)


def validate_email_configuration():
    """
    Validate required email configuration values.
    """

    missing_values = []

    if not SMTP_HOST:
        missing_values.append(
            "SMTP_HOST"
        )

    if not SMTP_USERNAME:
        missing_values.append(
            "SMTP_USERNAME"
        )

    if not SMTP_PASSWORD:
        missing_values.append(
            "SMTP_PASSWORD"
        )

    if not ALERT_RECIPIENT:
        missing_values.append(
            "ALERT_RECIPIENT"
        )

    if missing_values:

        return {
            "valid": False,
            "message": (
                "Missing email configuration: "
                + ", ".join(
                    missing_values
                )
            )
        }

    return {
        "valid": True,
        "message": (
            "Email configuration is valid."
        )
    }


def get_serious_alerts(
    alert_result
):
    """
    Return only High and Critical alerts.
    """

    serious_alerts = []

    alerts = alert_result.get(
        "alerts",
        []
    )

    for alert in alerts:

        severity = str(
            alert.get(
                "severity",
                ""
            )
        ).strip().lower()

        if severity in [
            "high",
            "critical"
        ]:

            serious_alerts.append(
                alert
            )

    return serious_alerts


def should_send_email(
    report,
    alert_result
):
    """
    Decide whether an email should be sent.

    Email is sent when:
    - Health status is Poor
    - At least one High or Critical alert exists
    """

    health_status = (
        report
        .get(
            "health_summary",
            {}
        )
        .get(
            "health_status",
            ""
        )
    )

    serious_alerts = get_serious_alerts(
        alert_result
    )

    return (
        health_status == "Poor"
        or len(serious_alerts) > 0
    )


def build_alert_details(
    alert_result
):
    """
    Build readable alert details for the email body.
    """

    alerts = alert_result.get(
        "alerts",
        []
    )

    if not alerts:

        return (
            "No individual alert records "
            "were generated."
        )

    alert_lines = []

    for index, alert in enumerate(
        alerts,
        start=1
    ):

        check_name = alert.get(
            "check_name",
            "Unknown Check"
        )

        severity = alert.get(
            "severity",
            "Unknown"
        )

        issue_count = alert.get(
            "issue_count",
            0
        )

        alert_lines.append(
            f"{index}. {check_name}\n"
            f"   Severity: {severity}\n"
            f"   Issues: {issue_count}"
        )

    return "\n\n".join(
        alert_lines
    )


def create_email_message(
    report,
    alert_result
):
    """
    Create the email subject and body.
    """

    health = report[
        "health_summary"
    ]

    serious_alerts = get_serious_alerts(
        alert_result
    )

    subject = (
        "[Data Quality Alert] "
        f"{health['health_status']} "
        f"- Score {health['health_score']}%"
    )

    alert_details = build_alert_details(
        alert_result
    )

    body = f"""
Automated Data Quality Monitoring Alert

A serious data quality issue was detected during the scheduled monitoring run.

MONITORING INFORMATION
----------------------
Dataset: {report['dataset_path']}
Dataset Type: {report['dataset_type']}
Checked At: {report['checked_at']}
Total Rows: {report['total_rows']}
Total Columns: {report['total_columns']}

HEALTH SUMMARY
--------------
Health Score: {health['health_score']}%
Health Status: {health['health_status']}
Total Checks: {health['total_checks']}
Failed Checks: {health['failed_checks']}
Total Issues: {health['total_issues']}
High/Critical Alerts: {len(serious_alerts)}

ALERT DETAILS
-------------
{alert_details}

The generated JSON and CSV reports are attached to this email.

This is an automated message from the Data Quality Monitoring System.
""".strip()

    message = EmailMessage()

    message[
        "Subject"
    ] = subject

    message[
        "From"
    ] = SMTP_USERNAME

    message[
        "To"
    ] = ALERT_RECIPIENT

    message.set_content(
        body
    )

    return message


def attach_file(
    message,
    file_path
):
    """
    Attach one report file to the email.
    """

    if not file_path:
        return

    path = Path(
        file_path
    )

    if not path.exists():
        return

    file_data = path.read_bytes()

    file_extension = (
        path.suffix
        .lower()
    )

    if file_extension == ".json":

        main_type = "application"
        sub_type = "json"

    elif file_extension == ".csv":

        main_type = "text"
        sub_type = "csv"

    else:

        main_type = "application"
        sub_type = "octet-stream"

    message.add_attachment(
        file_data,
        maintype=main_type,
        subtype=sub_type,
        filename=path.name
    )


def send_quality_alert_email(
    report,
    alert_result,
    saved_files
):
    """
    Send a serious data quality alert email.

    Returns a result dictionary whether the email
    was sent, skipped, or failed.
    """

    if not EMAIL_ALERTS_ENABLED:

        return {
            "email_sent": False,
            "status": "Disabled",
            "message": (
                "Email alerts are disabled "
                "in the .env file."
            )
        }

    configuration = (
        validate_email_configuration()
    )

    if not configuration[
        "valid"
    ]:

        return {
            "email_sent": False,
            "status": "Configuration Error",
            "message": configuration[
                "message"
            ]
        }

    if not should_send_email(
        report,
        alert_result
    ):

        return {
            "email_sent": False,
            "status": "Skipped",
            "message": (
                "No Poor health status or "
                "High/Critical alerts were found."
            )
        }

    try:

        message = create_email_message(
            report,
            alert_result
        )

        attach_file(
            message,
            saved_files.get(
                "json_report"
            )
        )

        attach_file(
            message,
            saved_files.get(
                "csv_summary"
            )
        )

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=30
        ) as smtp_server:

            smtp_server.ehlo()

            smtp_server.starttls()

            smtp_server.ehlo()

            smtp_server.login(
                SMTP_USERNAME,
                SMTP_PASSWORD
            )

            smtp_server.send_message(
                message
            )

        return {
            "email_sent": True,
            "status": "Sent",
            "message": (
                "Data quality alert email "
                "sent successfully."
            )
        }

    except smtplib.SMTPAuthenticationError:

        return {
            "email_sent": False,
            "status": (
                "Authentication Error"
            ),
            "message": (
                "SMTP authentication failed. "
                "Check the email address and "
                "App Password."
            )
        }

    except smtplib.SMTPException as error:

        return {
            "email_sent": False,
            "status": "SMTP Error",
            "message": str(
                error
            )
        }

    except Exception as error:

        return {
            "email_sent": False,
            "status": "Failed",
            "message": str(
                error
            )
        }