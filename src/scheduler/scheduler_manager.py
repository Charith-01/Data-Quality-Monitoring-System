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
from src.history.history_manager import save_history


DEFAULT_DATASET_PATH = "data/raw/recruitment_data.csv"
DEFAULT_DATASET_TYPE = "Recruitment Dataset"


def run_scheduled_monitoring():
    """
    Run the complete data quality monitoring process automatically.
    """

    print("\n" + "=" * 60)
    print("AUTOMATED DATA QUALITY MONITORING STARTED")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        report = run_data_quality_checks(
            DEFAULT_DATASET_PATH,
            dataset_type=DEFAULT_DATASET_TYPE
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

        health = report["health_summary"]

        print(f"Dataset: {report['dataset_path']}")
        print(f"Dataset Type: {report['dataset_type']}")
        print(f"Health Score: {health['health_score']}%")
        print(f"Health Status: {health['health_status']}")
        print(f"Failed Checks: {health['failed_checks']}")
        print(f"Total Issues: {health['total_issues']}")
        print(f"Alerts Generated: {alert_result['alert_count']}")
        print(f"JSON Report: {saved_files['json_report']}")
        print(f"CSV Report: {saved_files['csv_summary']}")
        print(f"History File: {history_result['history_file']}")

        print("=" * 60)
        print("AUTOMATED MONITORING COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except FileNotFoundError as error:
        print(f"Dataset file error: {error}")

    except Exception as error:
        print(f"Scheduled monitoring failed: {error}")


def create_scheduler():
    """
    Create the scheduler.

    Current schedule:
    Every day at 9:00 AM.
    """

    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_scheduled_monitoring,
        trigger=CronTrigger(
            hour=9,
            minute=0
        ),
        id="daily_data_quality_monitoring",
        name="Daily Data Quality Monitoring",
        replace_existing=True
    )

    return scheduler


if __name__ == "__main__":

    scheduler = create_scheduler()

    print("Data Quality Scheduler Started")
    print("Schedule: Every day at 9:00 AM")
    print("Press Ctrl + C to stop the scheduler.")

    try:
        scheduler.start()

    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")

    except Exception as error:
        print(f"Scheduler error: {error}")