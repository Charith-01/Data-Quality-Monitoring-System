import os
import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


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
from src.utils.report_generator import save_reports
from src.alerts.alert_manager import save_alerts
from src.alerts.email_notifier import send_quality_alert_email
from src.history.history_manager import save_history


DEFAULT_DATASET_PATH = (
    "data/raw/recruitment_data.csv"
)

DEFAULT_DATASET_TYPE = (
    "Recruitment Dataset"
)

SCHEDULER_TIMEZONE = (
    "Asia/Colombo"
)


def run_scheduled_monitoring():
    """
    Run the complete automatic data quality monitoring process.

    Scheduled monitoring:
    - Runs quality checks
    - Saves JSON report
    - Saves CSV report
    - Saves alerts
    - Saves monitoring history
    - Sends email for serious issues
    """

    print("\n" + "=" * 60)

    print(
        "AUTOMATED DATA QUALITY MONITORING STARTED"
    )

    print(
        "Started at: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print("=" * 60)

    try:

        report = run_data_quality_checks(
            DEFAULT_DATASET_PATH,
            dataset_type=DEFAULT_DATASET_TYPE
        )

        # Automatically save scheduled reports
        saved_files = save_reports(
            report
        )

        alert_result = save_alerts(
            report
        )

        history_result = save_history(
            report
        )

        # Send email only when serious issues exist
        email_result = (
            send_quality_alert_email(
                report,
                alert_result,
                saved_files
            )
        )

        health = report[
            "health_summary"
        ]

        print(
            f"Dataset: "
            f"{report['dataset_path']}"
        )

        print(
            f"Dataset Type: "
            f"{report['dataset_type']}"
        )

        print(
            f"Health Score: "
            f"{health['health_score']}%"
        )

        print(
            f"Health Status: "
            f"{health['health_status']}"
        )

        print(
            f"Failed Checks: "
            f"{health['failed_checks']}"
        )

        print(
            f"Total Issues: "
            f"{health['total_issues']}"
        )

        print(
            f"Alerts Generated: "
            f"{alert_result['alert_count']}"
        )

        print(
            f"JSON Report: "
            f"{saved_files['json_report']}"
        )

        print(
            f"CSV Report: "
            f"{saved_files['csv_summary']}"
        )

        print(
            f"History File: "
            f"{history_result['history_file']}"
        )

        print(
            f"Email Status: "
            f"{email_result['status']}"
        )

        print(
            f"Email Message: "
            f"{email_result['message']}"
        )

        print("=" * 60)

        print(
            "AUTOMATED MONITORING COMPLETED SUCCESSFULLY"
        )

        print("=" * 60)

        return {
            "report": report,
            "saved_files": saved_files,
            "alert_result": alert_result,
            "history_result": history_result,
            "email_result": email_result
        }

    except FileNotFoundError as error:

        print(
            f"Dataset file error: {error}"
        )

        return {
            "status": "Failed",
            "message": str(
                error
            )
        }

    except Exception as error:

        print(
            f"Scheduled monitoring failed: {error}"
        )

        return {
            "status": "Failed",
            "message": str(
                error
            )
        }


def create_scheduler():
    """
    Create a scheduler that runs every day at 9:00 AM
    in Sri Lanka time.
    """

    scheduler = BlockingScheduler(
        timezone=SCHEDULER_TIMEZONE
    )

    scheduler.add_job(
        run_scheduled_monitoring,
        trigger=CronTrigger(
            hour=9,
            minute=0,
            timezone=SCHEDULER_TIMEZONE
        ),
        id="daily_data_quality_monitoring",
        name="Daily Data Quality Monitoring",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600
    )

    return scheduler


if __name__ == "__main__":

    scheduler = create_scheduler()

    print(
        "Data Quality Scheduler Started"
    )

    print(
        "Schedule: Every day at 9:00 AM"
    )

    print(
        "Timezone: Asia/Colombo"
    )

    print(
        "Scheduled reports will be saved "
        "inside the reports folder."
    )

    print(
        "Serious data quality issues will "
        "generate an email alert."
    )

    print(
        "Press Ctrl + C to stop the scheduler."
    )

    try:

        scheduler.start()

    except KeyboardInterrupt:

        print(
            "\nScheduler stopped by user."
        )

    except Exception as error:

        print(
            f"Scheduler error: {error}"
        )