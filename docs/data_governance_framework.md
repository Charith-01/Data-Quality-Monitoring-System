# Data Governance Framework

## 1. Introduction

The Data Quality Monitoring System is designed to identify, monitor, report, and manage data quality issues within organisational datasets. A data governance framework is required to ensure that data is managed consistently, securely, accurately, and responsibly throughout its lifecycle.

This framework defines the roles, responsibilities, standards, controls, monitoring procedures, and escalation processes required to maintain reliable data. Although the system currently supports general datasets and recruitment datasets, the governance principles can be extended to other business areas.

---

## 2. Purpose

The purpose of this data governance framework is to:

- Establish clear responsibility for organisational data.
- Define data quality rules and standards.
- Ensure data is accurate, complete, valid, consistent, and unique.
- Provide a process for identifying and correcting data quality issues.
- Protect sensitive and confidential information.
- Support regular monitoring and reporting.
- Define escalation procedures for serious data quality incidents.
- Improve trust in data used for reporting and decision-making.

---

## 3. Scope

This framework applies to:

- Raw CSV datasets.
- Uploaded datasets.
- Recruitment and candidate data.
- Data quality reports.
- Monitoring history records.
- Alert logs.
- Scheduled monitoring processes.
- Email alert notifications.
- Users who create, update, review, or manage data.

The framework covers the complete data lifecycle, including:

1. Data collection.
2. Data entry.
3. Data validation.
4. Data storage.
5. Data usage.
6. Data monitoring.
7. Data correction.
8. Data retention.
9. Data disposal.

---

## 4. Data Governance Principles

### 4.1 Accountability

Every important dataset must have an assigned owner who is responsible for its quality, security, and authorised use.

### 4.2 Accuracy

Data must correctly represent the real-world person, object, transaction, or event it describes.

### 4.3 Completeness

Mandatory fields must contain the required values. Records with missing critical information must be reviewed and corrected.

### 4.4 Consistency

The same data must follow the same standards, formats, and business rules across different systems and files.

### 4.5 Validity

Data values must comply with approved formats, allowed values, and acceptable ranges.

### 4.6 Uniqueness

Duplicate records and duplicate identifiers must be prevented or corrected.

### 4.7 Timeliness

Data must be updated and monitored according to agreed schedules.

### 4.8 Security

Sensitive data must be protected from unauthorised access, alteration, disclosure, or deletion.

### 4.9 Transparency

Data quality rules, monitoring results, corrections, and incidents must be documented and traceable.

---

## 5. Governance Roles and Responsibilities

### 5.1 Data Governance Committee

The Data Governance Committee provides overall direction and approves governance policies.

Responsibilities include:

- Approving data standards.
- Reviewing serious data quality incidents.
- Assigning data owners.
- Approving changes to critical quality rules.
- Reviewing governance performance.
- Supporting corrective and preventive actions.

### 5.2 Data Owner

The Data Owner is accountable for a specific dataset or business data area.

Responsibilities include:

- Approving the use of the dataset.
- Defining business rules.
- Confirming mandatory fields.
- Reviewing major data quality problems.
- Approving corrective actions.
- Ensuring legal and organisational compliance.

For recruitment data, the Data Owner may be the Human Resources Manager or Recruitment Manager.

### 5.3 Data Steward

The Data Steward manages the operational quality of the data.

Responsibilities include:

- Reviewing monitoring reports.
- Investigating failed checks.
- Correcting data quality issues.
- Maintaining data definitions.
- Preventing repeated errors.
- Escalating serious problems.
- Communicating with data users.

### 5.4 System Administrator

The System Administrator manages the technical environment.

Responsibilities include:

- Maintaining the monitoring application.
- Managing scheduler execution.
- Protecting environment variables.
- Managing user access.
- Maintaining backups.
- Reviewing technical errors.
- Ensuring system availability.

### 5.5 Data Quality Analyst

The Data Quality Analyst monitors and analyses quality results.

Responsibilities include:

- Reviewing health scores.
- Analysing trends.
- Identifying recurring issues.
- Preparing data health reports.
- Recommending quality improvements.
- Supporting testing and validation.

### 5.6 Data User

Data Users access data for operational, analytical, or reporting purposes.

Responsibilities include:

- Using data only for authorised purposes.
- Reporting suspected errors.
- Avoiding unauthorised changes.
- Following approved data handling procedures.

---

## 6. RACI Responsibility Matrix

| Activity | Governance Committee | Data Owner | Data Steward | System Administrator | Data Quality Analyst |
|---|---|---|---|---|---|
| Approve governance policy | Accountable | Consulted | Consulted | Consulted | Consulted |
| Define data quality rules | Consulted | Accountable | Responsible | Consulted | Responsible |
| Run automated monitoring | Informed | Informed | Informed | Responsible | Consulted |
| Review quality reports | Informed | Accountable | Responsible | Consulted | Responsible |
| Correct data issues | Informed | Accountable | Responsible | Consulted | Consulted |
| Manage system security | Informed | Consulted | Informed | Responsible and Accountable | Informed |
| Escalate critical incidents | Accountable | Responsible | Responsible | Consulted | Responsible |
| Approve rule changes | Accountable | Responsible | Consulted | Consulted | Consulted |
| Maintain monitoring history | Informed | Informed | Consulted | Responsible | Responsible |
| Review data quality trends | Consulted | Accountable | Responsible | Informed | Responsible |

RACI definitions:

- Responsible: Performs the work.
- Accountable: Owns the final decision.
- Consulted: Provides advice or specialist knowledge.
- Informed: Receives updates about the activity.

---

## 7. Data Quality Dimensions

The monitoring system evaluates the following quality dimensions.

### 7.1 Completeness

Completeness checks whether required data is available.

Examples:

- Candidate ID must not be missing.
- Candidate name must not be empty.
- Email must be present when required.
- Mandatory recruitment fields must contain values.

### 7.2 Validity

Validity checks whether values follow approved rules.

Examples:

- Email addresses must follow a valid format.
- Phone numbers must follow the approved format.
- Application status must use approved values.
- Recruitment source must use approved values.
- Numeric values must be within acceptable ranges.

### 7.3 Uniqueness

Uniqueness checks whether records or identifiers are duplicated.

Examples:

- Candidate ID must be unique.
- Duplicate rows must be detected.
- Repeated business identifiers must be reviewed.

### 7.4 Consistency

Consistency checks whether similar data follows the same definitions and formats.

Examples:

- Status values must use the same spelling.
- Date columns must use an approved date format.
- Salary and experience values must use consistent units.

### 7.5 Accuracy

Accuracy checks whether data correctly represents reality.

Accuracy often requires verification against authorised source systems or supporting documents.

Examples:

- Candidate email belongs to the correct candidate.
- Expected salary reflects the submitted application.
- Job ID matches the correct job title.

### 7.6 Timeliness

Timeliness checks whether data is current and processed within the required period.

Examples:

- Recruitment records should be updated after status changes.
- Scheduled monitoring should run every day at 9:00 AM.
- Serious issues should be reviewed within the defined response period.

---

## 8. Data Quality Standards

The following minimum standards are recommended.

| Quality Dimension | Target |
|---|---:|
| Required column availability | 100% |
| Mandatory field completeness | At least 98% |
| Unique key compliance | 100% |
| Valid email format | At least 98% |
| Valid phone format | At least 95% |
| Valid categorical values | At least 98% |
| Duplicate record rate | Less than 1% |
| Scheduled monitoring completion | 100% |
| Critical incident response | Within 4 hours |
| High-severity issue review | Within 1 working day |

These targets may be adjusted according to business needs and approved by the Data Owner.

---

## 9. Recruitment Data Standards

The recruitment dataset should contain the following approved fields:

| Field | Requirement |
|---|---|
| candidate_id | Mandatory and unique |
| candidate_name | Mandatory |
| email | Mandatory and valid email format |
| phone | Mandatory and valid phone format |
| job_id | Mandatory |
| job_title | Mandatory |
| application_date | Mandatory and valid date |
| status | Must use an approved status |
| experience_years | Must be within the approved numeric range |
| expected_salary | Must be within the approved numeric range |
| source | Must use an approved recruitment source |

Approved status values include:

- Pending
- Shortlisted
- Rejected
- Hired

Approved source values must be maintained in the configuration file and approved by the Data Owner.

---

## 10. Data Quality Monitoring Process

The standard monitoring process is:

1. Select or receive the dataset.
2. Load the dataset using supported encoding formats.
3. Run general quality checks.
4. Run dataset-specific checks.
5. Calculate the data health score.
6. Generate alerts for failed checks.
7. Store the monitoring history.
8. Generate data health reports.
9. Send email notifications for serious issues.
10. Review and correct identified problems.
11. Re-run the monitoring process.
12. Confirm whether the health score has improved.

---

## 11. Monitoring Frequency

### Daily Monitoring

The default recruitment dataset is automatically monitored every day at 9:00 AM.

The scheduled process:

- Runs all applicable checks.
- Saves a JSON report.
- Saves a CSV summary.
- Updates the monitoring history.
- Updates the alert log.
- Sends an email for serious quality issues.

### Manual Monitoring

Users may run checks manually through the Streamlit dashboard.

Manual checks:

- Display current quality results.
- Display health scores and charts.
- Display profiling results.
- Allow manual JSON and CSV downloads.
- Do not automatically save reports inside the reports folder.

### Monthly Governance Review

A monthly governance review should examine:

- Average health score.
- Number of failed checks.
- Number of high and critical alerts.
- Recurring data quality issues.
- Delayed corrective actions.
- Rule changes.
- User access concerns.
- Governance improvement actions.

---

## 12. Health Score Classification

The system uses the following health classifications:

| Health Score | Status | Meaning |
|---:|---|---|
| 90–100 | Excellent | Data quality is very good |
| 75–89 | Good | Minor issues exist |
| 50–74 | Warning | Several issues require attention |
| 0–49 | Poor | Serious problems require immediate review |

The health score is a monitoring indicator. It should not replace professional review by the Data Owner or Data Steward.

---

## 13. Alert Severity Classification

| Severity | Typical Meaning | Response Time |
|---|---|---|
| Critical | Major risk to operations, compliance, or reporting | Within 4 hours |
| High | Significant quality issue affecting business use | Within 1 working day |
| Medium | Quality issue requiring planned correction | Within 3 working days |
| Low | Minor issue with limited impact | Within 5 working days |

Email alerts should be sent when:

- Health status is Poor.
- A High-severity alert is generated.
- A Critical alert is generated.

---

## 14. Data Issue Correction Process

When an issue is identified, the following process should be followed.

### Step 1: Record the issue

The system records:

- Check name.
- Issue count.
- Severity.
- Date and time.
- Dataset path.
- Health score.

### Step 2: Assign responsibility

The Data Steward assigns the issue to the appropriate business or technical person.

### Step 3: Investigate the root cause

Possible root causes include:

- Manual data-entry errors.
- Missing mandatory validation.
- Incorrect source-system data.
- Duplicate file imports.
- Incorrect transformation logic.
- Unapproved value formats.
- Technical integration failures.

### Step 4: Correct the data

Corrections must be made using authorised methods.

Examples:

- Fill missing required values.
- Remove duplicate records.
- Correct invalid email addresses.
- Correct invalid status values.
- Update out-of-range numeric values.

### Step 5: Validate the correction

The monitoring system must be run again after correction.

### Step 6: Close the issue

An issue may be closed only when:

- The corrected dataset passes the relevant check.
- The Data Steward confirms the correction.
- The reason and resolution are documented.

### Step 7: Prevent recurrence

Preventive actions may include:

- Input validation.
- Dropdown lists.
- Mandatory fields.
- Staff training.
- Source-system controls.
- Updated data quality rules.

---

## 15. Incident Escalation Process

The recommended escalation path is:

```text
Data Quality Analyst
        ↓
Data Steward
        ↓
Data Owner
        ↓
Data Governance Committee
        ↓
Senior Management
```

Critical incidents should be escalated immediately.
A critical incident may include:
 - Large-scale corruption of data.
 - Exposure of confidential candidate information.
 - Failure of scheduled monitoring for several days.
 - Incorrect reports used for important decisions.
 - Unauthorised modification or deletion.
 - Persistent health score below the approved threshold.

 ---

## 16. Access Control

Access should follow the principle of least privilege.

Recommended roles

 | Role                 | Access                                    |
| -------------------- | ----------------------------------------- |
| Administrator        | Full system and configuration access      |
| Data Quality Analyst | Run checks, review reports, view trends   |
| Data Steward         | Review and correct data                   |
| Data Owner           | Review summaries and approve actions      |
| General User         | Limited read-only access where authorised |

Sensitive files should not be committed to GitHub.

The following must remain private:

 - `.env`
 - SMTP username
 - SMTP password
 - App passwords
 - Personal candidate information
 - Confidential reports
 - Internal alert recipient addresses

---

## 17. Data Security Controls

Recommended security controls include:

- Store credentials in environment variables.
- Add `.env` to `.gitignore.`
- Use encrypted SMTP connections.
- Restrict access to reports and alert logs.
- Avoid using real personal data for public demonstrations.
- Maintain secure backups.
- Protect the operating system account.
- Review repository contents before pushing.
- Remove unnecessary personal information.
- Use approved retention and disposal procedures.

## 18. Data Retention

The organisation should define approved retention periods.

Recommended project defaults:

| Data Item                    | Recommended Retention                      |
| ---------------------------- | ------------------------------------------ |
| Raw uploaded temporary files | Delete after processing or within 24 hours |
| Scheduled JSON reports       | 12 months                                  |
| Scheduled CSV reports        | 12 months                                  |
| Alert logs                   | 12 months                                  |
| Monitoring history           | 24 months                                  |
| Email alert records          | According to organisational email policy   |
| Test datasets                | Until project testing is completed         |

Retention periods must be adjusted according to organisational and legal requirements.

---

## 19. Backup and Recovery

Recommended backup controls include:

- Daily backup of monitoring history.
- Daily backup of alert logs.
- Weekly backup of scheduled reports.
- Secure storage of configuration files.
- Regular recovery testing.
- Documented restoration procedures.
- Separate backup location from the primary project folder.

The `.env` file should be backed up securely and must not be stored in a public repository.

---

## 20. Change Management

Changes to data quality rules must be controlled.

The change process should include:

 1. Submit a rule-change request.
 2. Explain the business reason.
 3. Identify affected datasets.
 4. Review the potential impact.
 5. Obtain Data Owner approval.
 6. Update configuration or code.
 7. Test the change.
 8. Update documentation.
 9. Deploy the change.
 10. Monitor the results.

Examples of controlled changes include:

 - Adding a new mandatory field.
 - Changing an allowed status value.
 - Changing a numeric range.
 - Changing alert thresholds.
 - Changing the daily monitoring time.

---

## 21. Data Quality Key Performance Indicators

Recommended KPIs include:

| KPI                     | Calculation                                       |
| ----------------------- | ------------------------------------------------- |
| Average health score    | Total health scores divided by number of runs     |
| Failed check rate       | Failed checks divided by total checks             |
| Issue resolution rate   | Resolved issues divided by identified issues      |
| Duplicate rate          | Duplicate rows divided by total rows              |
| Missing value rate      | Missing values divided by total cells             |
| Critical alert count    | Number of critical alerts per period              |
| Repeat issue rate       | Repeated issues divided by total issues           |
| Monitoring success rate | Successful scheduled runs divided by planned runs |
| Average resolution time | Total resolution time divided by resolved issues  |

---

## 22. Governance Reporting

The monthly data governance report should include:

 - Executive summary.
 - Current health score.
 - Health score trend.
 - Total failed checks.
 - Total quality issues.
 - High and critical alerts.
 - Most common failed checks.
 - Corrective actions completed.
 - Outstanding actions.
 - Rule changes.
 - Security incidents.
 - Recommendations for the next period.

---

## 23. Data Governance Recommendations

### 23.1 Introduce source-level validation

Data should be validated before entering the monitoring system.

Examples:
 - Required fields.
 - Email validation.
 - Phone validation.
 - Dropdown status values.
 - Numeric range validation.

### 23.2 Assign formal data owners

Every important dataset should have a clearly documented Data Owner.

### 23.3 Establish regular governance meetings

The organisation should conduct monthly data quality reviews.

### 23.4 Maintain a data dictionary

A data dictionary should explain:

 - Column name.
 - Business definition.
 - Data type.
 - Mandatory status.
 - Allowed values.
 - Data owner.
 - Data source.
 - Validation rule.

### 23.5 Improve audit logging

Future system versions should record:

 - User who ran the check.
 - Dataset name.
 - Rule version.
 - Correction status.
 - Issue owner.
 - Issue closure date.

### 23.6 Implement role-based access control

The dashboard should eventually require login and role-based permissions.

### 23.7 Use a central database

For production use, monitoring history, alerts, and reports should be stored in a secured database instead of only CSV files.

### 23.8 Add service-level agreements

Response and resolution targets should be formally approved.

### 23.9 Conduct staff training

Employees should receive training on:

 - Correct data entry.
 - Data privacy.
 - Quality standards.
 - Incident reporting.
 - Data ownership responsibilities.

### 23.10 Review governance annually

The governance framework should be reviewed at least once per year or after major organisational or system changes.

---

## 24. Governance Review Checklist

The monthly governance review should confirm:

 - The scheduler ran successfully.
 - Reports were generated.
 - Alerts were reviewed.
 - Critical issues were escalated.
 - Corrective actions were completed.
 - Repeated issues were analysed.
 - Access permissions remain appropriate.
 - Environment credentials remain protected.
 - Data quality rules remain current.
 - Monitoring trends are improving.
 - Retention rules are followed.
 - Documentation is updated.

---

## 25. Conclusion

This data governance framework provides the policies, roles, standards, and procedures required to support the Data Quality Monitoring System. It helps ensure that data quality issues are detected consistently, assigned to the correct responsible persons, corrected within agreed timelines, and monitored over time.

Effective governance requires both technical controls and organisational responsibility. The monitoring system provides automated checks, reports, alerts, history, scheduling, and trend analysis, while the governance framework ensures that these outputs result in accountable and sustainable data quality improvements.
