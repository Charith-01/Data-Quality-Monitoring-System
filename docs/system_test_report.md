# Data Quality Monitoring System Test Report

## 1. Document Information

| Item | Details |
|---|---|
| Project Name | Data Quality Monitoring System |
| Test Type | Functional, Integration, and Manual Testing |
| Test Environment | Local Development Environment |
| Dashboard Framework | Streamlit |
| Programming Language | Python |
| Test Framework | Pytest |
| Scheduler | APScheduler |
| Report Formats | JSON and CSV |

---

## 2. Testing Objective

The purpose of system testing is to confirm that the Data Quality Monitoring System correctly:

- Loads CSV datasets.
- Runs general data quality checks.
- Runs recruitment-specific checks.
- Detects missing, invalid, duplicate, and out-of-range values.
- Calculates the health score.
- Generates alerts.
- Stores monitoring history.
- Displays trend charts.
- Supports manual report downloads.
- Generates scheduled reports.
- Sends email alerts for serious issues.
- Handles invalid and incomplete datasets without crashing.

---

## 3. Test Scope

The testing process covers:

- Dataset loading.
- Encoding fallback.
- General data checks.
- Recruitment checks.
- Health score calculation.
- Data profiling.
- Dashboard visualisations.
- Manual report downloads.
- Scheduled report generation.
- Alert logging.
- Monitoring history.
- Email notifications.
- Error handling.

---

## 4. Automated Test Cases

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| AT-01 | Clean recruitment dataset | All checks pass and health score is Excellent | All checks passed successfully | Passed |
| AT-02 | Dirty recruitment dataset | Multiple checks fail and score decreases | Multiple invalid values were detected | Passed |
| AT-03 | General dataset | Only general checks run | Recruitment-specific checks were excluded | Passed |
| AT-04 | Missing recruitment columns | Required Columns Check fails | Missing columns were detected correctly | Passed |
| AT-05 | Duplicate rows | Duplicate check fails once | Duplicate row was detected once | Passed |
| AT-06 | Invalid numeric values | Numeric Range Check fails | Invalid numeric values were detected | Passed |
| AT-07 | Header-only dataset | System handles zero rows without crashing | System handled zero rows safely | Passed |
| AT-08 | Report metadata | Report contains all required fields | All required report fields were present | Passed |

Automated test result:

```text
8 passed
0 failed
```

---

## 5. Manual Dashboard Test Cases

| Test ID | Test Case                    | Test Steps                              | Expected Result                           | Status  |
| ------- | ---------------------------- | --------------------------------------- | ----------------------------------------- | ------- |
| MT-01   | Dashboard startup            | Run Streamlit dashboard                 | Dashboard opens successfully              | Pending |
| MT-02   | Default dataset preview      | Open dashboard without upload           | Default recruitment data appears          | Pending |
| MT-03   | CSV upload                   | Upload a valid CSV                      | Uploaded dataset appears in preview       | Pending |
| MT-04   | Run manual checks            | Click Run Data Quality Checks           | Results, score, alerts, and charts appear | Pending |
| MT-05   | JSON download                | Click Download JSON Report              | Browser downloads JSON file               | Pending |
| MT-06   | CSV download                 | Click Download CSV Summary              | Browser downloads CSV file                | Pending |
| MT-07   | Manual file-saving behaviour | Run checks without downloading          | No new file is created in reports folder  | Pending |
| MT-08   | Monitoring history           | Run checks multiple times               | New history rows appear                   | Pending |
| MT-09   | Health-score trend           | Run checks at least twice               | Health score trend chart appears          | Pending |
| MT-10   | Issue trend                  | Run checks at least twice               | Issue trend chart appears                 | Pending |
| MT-11   | General dataset mode         | Select General Dataset and upload a CSV | Recruitment checks are excluded           | Pending |
| MT-12   | Missing columns warning      | Upload incomplete recruitment CSV       | Missing-column warning appears            | Pending |

---

## 6. Scheduled Monitoring Test Cases

| Test ID | Test Case               | Test Steps                                 | Expected Result                        | Status  |
| ------- | ----------------------- | ------------------------------------------ | -------------------------------------- | ------- |
| ST-01   | Immediate scheduled run | Call `run_scheduled_monitoring()` manually | Monitoring completes successfully      | Pending |
| ST-02   | Scheduled JSON report   | Run scheduled monitoring                   | JSON report is saved in reports folder | Pending |
| ST-03   | Scheduled CSV report    | Run scheduled monitoring                   | CSV report is saved in reports folder  | Pending |
| ST-04   | History update          | Run scheduled monitoring                   | Monitoring history gains a new row     | Pending |
| ST-05   | Alert-log update        | Run with dirty dataset                     | Failed checks are written to alert log | Pending |
| ST-06   | Scheduler startup       | Start `scheduler_manager.py`               | Scheduler waits for daily 9:00 AM run  | Pending |
| ST-07   | Scheduler timezone      | Review startup message                     | Asia/Colombo timezone is shown         | Pending |

---

## 7. Email Alert Test Cases

| Test ID | Test Case                  | Test Steps                         | Expected Result                          | Status  |
| ------- | -------------------------- | ---------------------------------- | ---------------------------------------- | ------- |
| ET-01   | Email disabled             | Set `EMAIL_ALERTS_ENABLED=false`   | Email sending is skipped safely          | Pending |
| ET-02   | Poor-health email          | Enable email and use dirty dataset | Alert email is received                  | Pending |
| ET-03   | Email subject              | Review received email              | Subject includes health status and score | Pending |
| ET-04   | Email body                 | Review received email              | Health and alert details are included    | Pending |
| ET-05   | JSON attachment            | Review received email              | JSON report is attached                  | Pending |
| ET-06   | CSV attachment             | Review received email              | CSV report is attached                   | Pending |
| ET-07   | Clean-data email behaviour | Run with clean data                | No serious alert email is sent           | Pending |
| ET-08   | Invalid credentials        | Use incorrect SMTP password        | Authentication error is handled safely   | Pending |

---

## 8. Security Test Cases

| Test ID | Test Case                             | Expected Result                         | Status  |
| ------- | ------------------------------------- | --------------------------------------- | ------- |
| SEC-01  | `.env` file ignored by Git            | `.env` does not appear in Git staging   | Pending |
| SEC-02  | Credentials absent from source code   | No passwords are hard-coded             | Pending |
| SEC-03  | Generated reports ignored if required | Generated reports are not committed     | Pending |
| SEC-04  | Alert logs ignored if required        | Generated alert logs are not committed  | Pending |
| SEC-05  | Temporary uploaded data ignored       | Uploaded temporary CSV is not committed | Pending |

---

## 9. Error-Handling Test Cases

| Test ID | Test Case                   | Expected Result                      | Status  |
| ------- | --------------------------- | ------------------------------------ | ------- |
| ER-01   | Missing dataset file        | Clear file-not-found message appears | Pending |
| ER-02   | Invalid CSV encoding        | Encoding fallback is attempted       | Pending |
| ER-03   | Header-only CSV             | System does not crash                | Passed  |
| ER-04   | Invalid numeric text        | Numeric issue is detected            | Passed  |
| ER-05   | Missing recruitment columns | Checks fail safely without crashing  | Passed  |
| ER-06   | Invalid SMTP configuration  | Configuration error is returned      | Pending |

---

## 10. Test Execution Commands

Run automated tests:
```bash
pytest -v
```

Run the dashboard:
```bash
streamlit run "src/dashboard/app.py"
```

Run scheduled monitoring immediately:
```bash
python -c "from src.scheduler.scheduler_manager import run_scheduled_monitoring; run_scheduled_monitoring()"
```

Start the daily scheduler:
```bash
python src/scheduler/scheduler_manager.py
```

---

## 11. Final Test Summary

| Item                     | Result                                           |
| ------------------------ | ------------------------------------------------ |
| Total Automated Tests    | 8                                                |
| Automated Tests Passed   | 8                                                |
| Automated Tests Failed   | 0                                                |
| Automated Test Pass Rate | 100%                                             |
| Manual Tests Passed      | Pending                                          |
| Manual Tests Failed      | Pending                                          |
| Scheduled Tests          | Pending                                          |
| Email Tests              | Pending                                          |
| Security Tests           | Pending                                          |
| Critical Defects         | 0                                                |
| Overall System Status    | Automated Testing Passed; Manual Testing Pending |

---

## 12. Conclusion

The automated testing stage was completed successfully.

All eight automated tests passed, confirming that the system correctly handles:

 - Clean recruitment datasets.
 - Dirty recruitment datasets.
 - General datasets.
 - Missing required columns.
 - Duplicate rows.
 - Invalid numeric values.
 - Header-only datasets.
 - Report metadata.

The remaining work is to complete manual dashboard testing, scheduled monitoring testing, email alert testing, and security verification.