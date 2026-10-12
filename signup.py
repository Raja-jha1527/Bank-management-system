
import re
import random
import sqlite3
from contextlib import contextmanager
from typing import Callable, Optional

DB_PATH = "bank.db"
MAX_TRIES = 3


@contextmanager
def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS CUSTOMER (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Account_Number TEXT UNIQUE NOT NULL,
                Name TEXT NOT NULL,
                Gmail TEXT UNIQUE NOT NULL,
                Contact TEXT UNIQUE NOT NULL,
                Balance REAL NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS TRANSACTIONS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Account_Number TEXT NOT NULL,
                Type TEXT NOT NULL,
                Amount REAL NOT NULL,
                Balance_After REAL NOT NULL,
                Created_At TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (Account_Number) REFERENCES CUSTOMER(Account_Number)
            )
            """
        )
        conn.commit()
def fetch_customers() -> list[tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Gmail, Contact, Account_Number FROM CUSTOMER")
        return cursor.fetchall()


def prompt_with_retries(
    prompt: str,
    validator: Callable[[str], bool],
    invalid_message: str,
    max_tries: int = MAX_TRIES,
) -> Optional[str]:
    for attempt in range(1, max_tries + 1):
        value = input(prompt).strip()
        if validator(value):
            return value

        print(invalid_message)
        if attempt == max_tries:
            print("Limit reached, try later")
            return None

        print("Press 1 for retry\nPress 2 for exit")
        if input("Enter: ").strip() != "1":
            return None
    return None


def get_name() -> Optional[str]:
    def is_valid(value: str) -> bool:
        return bool(value) and all(c.isalpha() or c == " " for c in value)

    return prompt_with_retries("Full Name: ", is_valid, "Invalid Name")


def get_number(used_contacts: set[str]) -> Optional[str]:
    def is_valid(value: str) -> bool:
        return (
            value.isascii()
            and value.isdigit()
            and len(value) == 10
            and value not in used_contacts
        )

    return prompt_with_retries(
        "Contact Number: ", is_valid, "Invalid or already registered number"
    )


def get_email(used_emails: set[str]) -> Optional[str]:
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", re.IGNORECASE)

    def is_valid(value: str) -> bool:
        return bool(pattern.match(value)) and value.lower() not in used_emails

    email = prompt_with_retries(
        "Gmail: ", is_valid, "Invalid or already registered Gmail"
    )
    return email.lower() if email else None


def generate_account_number(existing: set[str]) -> str:
    while True:
        candidate = str(random.randint(1_000_000_000, 9_999_999_999))
        if candidate not in existing:
            return candidate


def register_customer() -> Optional[dict]:
    customers = fetch_customers()
    used_emails = {str(row[0]).lower() for row in customers}
    used_contacts = {str(row[1]) for row in customers}
    used_accounts = {str(row[2]) for row in customers}

    name = get_name()
    if name is None:
        return None

    phone = get_number(used_contacts)
    if phone is None:
        return None

    gmail = get_email(used_emails)
    if gmail is None:
        return None

    return {
        "Name": name,
        "Contact": phone,
        "Gmail": gmail,
        "Account_Number": generate_account_number(used_accounts),
    }