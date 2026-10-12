from typing import Optional

from signup import get_connection, MAX_TRIES
from balance import show_balance, show_history
from deposit import deposit
from withdraw import withdraw


def find_customer(account_number: str, contact: str) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT Account_Number, Name, Gmail, Contact, Balance
            FROM CUSTOMER
            WHERE Account_Number = ? AND Contact = ?
            """,
            (account_number, contact),
        ).fetchone()

    if row is None:
        return None
    return {
        "Account_Number": row[0],
        "Name": row[1],
        "Gmail": row[2],
        "Contact": row[3],
        "Balance": row[4],
    }


def login() -> Optional[dict]:
    for attempt in range(1, MAX_TRIES + 1):
        account = input("Account Number: ").strip()
        contact = input("Contact Number: ").strip()

        customer = find_customer(account, contact)
        if customer:
            print(f"\nWelcome back, {customer['Name']}!")
            return customer

        print("Invalid account number or contact number")
        if attempt == MAX_TRIES:
            print("Limit reached, try later")
            return None

        print("Press 1 for retry\nPress 2 for exit")
        if input("Enter: ").strip() != "1":
            return None
    return None


def account_menu(customer: dict) -> None:
    account_number = customer["Account_Number"]
    while True:
        print("\nPress 1 for check balance")
        print("Press 2 for deposit")
        print("Press 3 for withdraw")
        print("Press 4 for transaction history")
        print("Press 5 for logout")
        choice = input("Enter: ").strip()

        if choice == "1":
            show_balance(account_number)
        elif choice == "2":
            deposit(account_number)
        elif choice == "3":
            withdraw(account_number)
        elif choice == "4":
            show_history(account_number)
        elif choice == "5":
            print("Logged out")
            return
        else:
            print("Invalid option")

