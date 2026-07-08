from csv import DictReader
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()
CSV_FILE = Path(__file__).with_name("data_science_projects_latest.csv")


def _parse_entry_date(raw_date: str) -> datetime | None:
    if not raw_date:
        return None

    try:
        return datetime.strptime(raw_date.strip(), "%d-%m-%Y")
    except ValueError:
        return None


def _extract_emails(raw_value: str) -> list[str]:
    if not raw_value:
        return []

    normalized = raw_value.replace("|", ",").replace(";", ",")
    return [value.strip() for value in normalized.split(",") if value.strip()]


def _name_from_email(email: str) -> str:
    local_part = email.split("@", maxsplit=1)[0]
    candidate = local_part.split("_", maxsplit=1)[0]
    return candidate.capitalize()

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/teams-notification")
def teams_notification():
    if not CSV_FILE.exists():
        return {
            "entry_date": None,
            "recipient": [],
            "message": ["CSV file not found."],
        }

    with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as csv_file:
        rows = list(DictReader(csv_file))

    recipient_to_usecases: dict[str, list[str]] = {}
    dated_rows = [
        (row, _parse_entry_date(row.get("Entry Date (DD-MM-YYYY)", "")))
        for row in rows
    ]
    dated_rows = [(row, date_val) for row, date_val in dated_rows if date_val is not None]

    if not dated_rows:
        return {
            "entry_date": None,
            "recipient": [],
            "message": ["No valid dated records found in CSV."],
        }

    latest_date = max(date_val for _, date_val in dated_rows)
    latest_date_rows = [row for row, date_val in dated_rows if date_val == latest_date]

    if not latest_date_rows:
        return {
            "entry_date": latest_date.strftime("%d-%m-%Y"),
            "recipient": [],
            "message": ["No records found for the latest date."],
        }

    for row in latest_date_rows:
        use_case = row.get("Use case", "Unknown Use case").strip() or "Unknown Use case"
        for email in _extract_emails(row.get("Data Scientist", "")):
            recipient_to_usecases.setdefault(email, [])
            if use_case not in recipient_to_usecases[email]:
                recipient_to_usecases[email].append(use_case)

    recipients = list(recipient_to_usecases.keys())
    messages = []
    for email in recipients:
        use_cases = ", ".join(recipient_to_usecases[email])
        messages.append(
            f"Please share the latest update for: {use_cases}. "
            f"(Entry Date: {latest_date.strftime('%d-%m-%Y')})"
        )

    return {
        "recipient": recipients,
        "message": messages,
    }
