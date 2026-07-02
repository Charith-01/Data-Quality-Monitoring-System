# Recruitment Data Dictionary

## 1. Introduction

This data dictionary defines the approved structure, meaning, data type, validation requirements, and ownership of fields used in the recruitment dataset.

The purpose of this document is to ensure that recruitment data is recorded, interpreted, validated, and monitored consistently.

---

## 2. Dataset Information

| Item | Description |
|---|---|
| Dataset Name | Recruitment Dataset |
| Dataset Purpose | Store candidate applications and recruitment information |
| Primary Owner | Human Resources Department |
| Operational Steward | Recruitment Team |
| Monitoring Frequency | Daily at 9:00 AM and manually when required |
| File Format | CSV |
| Primary Key | candidate_id |
| Classification | Internal and confidential |

---

## 3. Field Definitions

| Column Name | Business Meaning | Data Type | Mandatory | Validation Rule | Example | Owner |
|---|---|---|---|---|---|---|
| candidate_id | Unique identifier assigned to each candidate | Text | Yes | Must not be empty and must be unique | CAND001 | Recruitment Team |
| candidate_name | Full name of the candidate | Text | Yes | Must not be empty | Nimal Perera | Recruitment Team |
| email | Candidate email address | Text | Yes | Must follow a valid email format | nimal@example.com | Recruitment Team |
| phone | Candidate contact number | Text | Yes | Must contain a valid approved phone number format | 0771234567 | Recruitment Team |
| job_id | Unique identifier of the job vacancy | Text | Yes | Must not be empty | JOB001 | HR Department |
| job_title | Name of the position applied for | Text | Yes | Must not be empty | Data Analyst | HR Department |
| application_date | Date the candidate submitted the application | Date | Yes | Must be a valid date | 2026-07-01 | Recruitment Team |
| status | Current stage of the application | Category | Yes | Must use an approved status value | Shortlisted | Recruitment Manager |
| experience_years | Number of years of relevant work experience | Numeric | Yes | Must be within the approved numeric range | 3 | Recruitment Team |
| expected_salary | Candidate’s expected salary amount | Numeric | Yes | Must be within the approved numeric range | 150000 | Recruitment Team |
| source | Channel through which the application was received | Category | Yes | Must use an approved recruitment source | LinkedIn | Recruitment Manager |

---

## 4. Approved Status Values

The `status` field must contain one of the following values:

| Status | Meaning |
|---|---|
| Pending | Application has been received but not reviewed |
| Shortlisted | Candidate has been selected for the next stage |
| Rejected | Candidate has not been selected |
| Hired | Candidate has been successfully recruited |

Values outside this list should be treated as invalid unless approved through the governance change-management process.

---

## 5. Approved Recruitment Sources

The `source` field must contain a value approved in the project configuration.

Typical approved values may include:

| Source | Meaning |
|---|---|
| LinkedIn | Application received through LinkedIn |
| Indeed | Application received through Indeed |
| Company Website | Application submitted through the organisation website |
| Referral | Candidate referred by an employee or authorised contact |
| Job Fair | Application received through a recruitment event |
| Recruitment Agency | Candidate supplied by an approved agency |
| Other | Approved alternative source |

The final approved values must match the values maintained in `config/data_quality_rules.py`.

---

## 6. Detailed Validation Rules

### 6.1 candidate_id

- Must not be null.
- Must not be empty.
- Must be unique.
- Should remain unchanged after assignment.
- Must not be reused for another candidate.

Example:

```text
CAND001
```

### 6.2 candidate_name
 - Must not be null.
 - Must not be empty.
 - Should contain the candidate’s full name.
 - Should not contain a candidate identifier instead of a name.

Example:
```text
Nimal Perera
```

### 6.3 email
 - Must not be null.
 - Must follow a valid email structure.
 - Should contain an @ symbol.
 - Should contain a valid domain section.
 - Should belong to the correct candidate.

Example:

```text
nimal.perera@example.com
```

Invalid examples:

```text
nimal.example.com
nimal@
@nimal.com
```

### 6.4 phone
 - Must not be null.
 - Must be stored as text to preserve leading zeroes.
 - Must follow the approved phone-number format.
 - The current monitoring rule expects a Sri Lankan number beginning with 0 and containing 10 digits.

Example:

```text
0771234567
```

Invalid examples:

```text
771234567
07712345
phone123
```

### 6.5 job_id
 - Must not be null.
 - Must not be empty.
 - Must identify an approved job vacancy.
 - Should match the related job title.

Example:

```text
JOB001
```

### 6.6 job_title
 - Must not be null.
 - Must not be empty.
 - Must describe the role associated with the job identifier.
 - Should use consistent job-title naming.

Example:

```text
Data Analyst
```

### 6.7 application_date
 - Must not be null.
 - Must contain a valid date.
 - Should use a consistent format.
 - Recommended format is YYYY-MM-DD.
 - Should not be a future date unless specifically allowed.

Example:

```text
2026-07-01
```

### 6.8 status
 - Must not be null.
 - Must use one approved value.
 - Must use consistent spelling and capitalisation.

Approved values:

```text
Pending
Shortlisted
Rejected
Hired
```

### 6.9 experience_years
 - Must be numeric.
 - Must not be negative.
 - Must fall within the range configured in NUMERIC_RULES.
 - Decimal values may be allowed if approved.

Example:

```text
3
```

Invalid examples:

```text
-2
many
unknown
```

### 6.10 expected_salary
 - Must be numeric.
 - Must not be negative.
 - Must fall within the configured range.
 - Must use one approved currency and unit.
 - The dataset should not mix monthly and annual salary values.

Example:

```text
150000
```

### 6.11 source
 - Must not be null.
 - Must use an approved source value.
 - Must match a value maintained in the project configuration.
 - New source values require approval before use.

Example:

```text
LinkedIn
```

---

## 7. Data Quality Dimensions by Field

| Column Name      | Completeness | Validity |  Uniqueness | Consistency | Accuracy |
| ---------------- | -----------: | -------: | ----------: | ----------: | -------: |
| candidate_id     |          Yes |      Yes |         Yes |         Yes |      Yes |
| candidate_name   |          Yes |      Yes |          No |         Yes |      Yes |
| email            |          Yes |      Yes | Recommended |         Yes |      Yes |
| phone            |          Yes |      Yes | Recommended |         Yes |      Yes |
| job_id           |          Yes |      Yes |          No |         Yes |      Yes |
| job_title        |          Yes |      Yes |          No |         Yes |      Yes |
| application_date |          Yes |      Yes |          No |         Yes |      Yes |
| status           |          Yes |      Yes |          No |         Yes |      Yes |
| experience_years |          Yes |      Yes |          No |         Yes |      Yes |
| expected_salary  |          Yes |      Yes |          No |         Yes |      Yes |
| source           |          Yes |      Yes |          No |         Yes |      Yes |

---

## 8. Missing Value Rules

The following fields are mandatory and should not contain null or empty values:

```text
candidate_id
candidate_name
email
phone
job_id
job_title
application_date
status
experience_years
expected_salary
source
```

When a mandatory value is missing:

 1. The quality check should fail.
 2. The issue should appear in the dashboard.
 3. The issue should be written to the alert log.
 4. The Data Steward should investigate the source.
 5. The record should be corrected before business use.

---

## 9. Duplicate Rules

Duplicate rows

A row is considered duplicated when all values match another row.

Duplicate rows should be reviewed and removed unless there is a documented business reason to retain them.

Duplicate candidate identifiers

The `candidate_id` field must be unique.

A duplicated candidate identifier may indicate:

 - The same candidate was imported twice.
 - An identifier was reused.
 - Multiple candidates were assigned the same identifier.
 - The source system generated an incorrect value.

 ---

## 10. Data Ownership

| Data Element                      | Data Owner          | Data Steward         |
| --------------------------------- | ------------------- | -------------------- |
| Candidate personal details        | HR Manager          | Recruitment Officer  |
| Job information                   | Recruitment Manager | HR Officer           |
| Application status                | Recruitment Manager | Recruitment Officer  |
| Experience and salary information | HR Manager          | Recruitment Officer  |
| Recruitment source                | Recruitment Manager | Recruitment Officer  |
| Monitoring reports                | Data Owner          | Data Quality Analyst |
| Alert logs                        | Data Owner          | Data Quality Analyst |
| Monitoring history                | System Owner        | System Administrator |

---

## 11. Data Classification

Recruitment data should be treated as confidential because it may include personal information.

Examples of sensitive information include:

 - Candidate name.
 - Email address.
 - Phone number.
 - Salary expectation.
 - Employment history.
 - Application outcome.

Access should be limited to authorised HR staff, data quality staff, and system administrators.

---

## 12. Data Retention

Recommended retention periods are:

| Data Item                      | Retention Period                           |
| ------------------------------ | ------------------------------------------ |
| Active candidate records       | According to recruitment policy            |
| Unsuccessful candidate records | According to HR and legal requirements     |
| Temporary uploaded CSV files   | Delete after processing or within 24 hours |
| Data quality reports           | 12 months                                  |
| Alert logs                     | 12 months                                  |
| Monitoring history             | 24 months                                  |

The organisation must approve the final retention periods.

---

## 13. Data Correction Procedure

When invalid recruitment data is identified:

 1. Confirm the failed rule.
 2. Identify the affected record.
 3. Review the original source.
 4. Contact the responsible Data Steward.
 5. Correct the value using an authorised method.
 6. Record the reason for correction.
 7. Run the data quality checks again.
 8. Confirm that the issue is resolved.
 9. Close the issue after review.

---

## 14. Change Management

Changes to this data dictionary must be approved.

Examples include:
 - Adding a new column.
 - Removing an existing column.
 - Changing a mandatory field.
 - Updating an allowed status.
 - Updating a recruitment source.
 - Changing a numeric range.
 - Changing the phone format.
 - Changing data ownership.

Each change should include:
 - Business reason.
 - Requested change.
 - Affected systems.
 - Risk assessment.
 - Approval.
 - Testing.
 - Documentation update.

---

## 15. Example Valid Record

```csv
candidate_id,candidate_name,email,phone,job_id,job_title,application_date,status,experience_years,expected_salary,source
CAND001,Nimal Perera,nimal.perera@example.com,0771234567,JOB001,Data Analyst,2026-07-01,Shortlisted,3,150000,LinkedIn
```
---

## 16. Example Invalid Record

```csv
candidate_id,candidate_name,email,phone,job_id,job_title,application_date,status,experience_years,expected_salary,source
CAND001,,invalid-email,77123,JOB001,Data Analyst,wrong-date,Selected,-2,text,UnknownSource
```

Possible failures include:
 - Missing candidate name.
 - Invalid email.
 - Invalid phone.
 - Invalid date.
 - Unapproved status.
 - Negative experience.
 - Non-numeric salary.
 - Unapproved recruitment source.

---

## 17. Review Frequency

This data dictionary should be reviewed:
 - Every six months.
 - When the recruitment process changes.
 - When new fields are added.
 - When business rules change.
 - When validation problems repeatedly occur.
 - When the monitoring system is updated.

---

## 18. Conclusion

This recruitment data dictionary provides a consistent definition for each field used in the recruitment dataset. It supports accurate data entry, automated validation, data quality monitoring, governance, reporting, and issue correction.

All users who create, update, monitor, or use recruitment data should follow the definitions and validation rules in this document.

```
Important: when you paste this into the `.md` file, do not include the outer triple backticks that wrap the whole example. Keep only the inner `csv` code blocks.
```
