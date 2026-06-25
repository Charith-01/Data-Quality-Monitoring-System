# Data Quality Rules Configuration

REQUIRED_COLUMNS = [
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

MANDATORY_FIELDS = [
    "candidate_id",
    "candidate_name",
    "email",
    "phone",
    "job_id",
    "application_date",
    "status"
]

VALID_STATUS_VALUES = [
    "Pending",
    "Shortlisted",
    "Rejected",
    "Hired"
]

VALID_SOURCES = [
    "LinkedIn",
    "TopJobs",
    "Referral",
    "Company Website",
    "Other"
]

UNIQUE_COLUMNS = [
    "candidate_id"
]

NUMERIC_RULES = {
    "experience_years": {
        "min": 0,
        "max": 40
    },
    "expected_salary": {
        "min": 0,
        "max": 1000000
    }
}