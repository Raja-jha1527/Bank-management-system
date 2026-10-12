import sqlite3
from login import login,account_menu
from signup import register_customer, get_connection, init_db


def confirm_details(customer: dict) -> bool:
    print("\nCheck your details")
    print(f"Full Name: {customer['Name']}")
    print(f"Gmail: {customer['Gmail']}")
    print(f"Contact Number: {customer['Contact']}")
    print("Press 1 to continue\nPress 2 to exit")
    return input("Enter: ").strip() == "1"


def save_customer(customer: dict) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO CUSTOMER (Account_Number, Name, Gmail, Contact, Balance)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    customer["Account_Number"],
                    customer["Name"],
                    customer["Gmail"],
                    customer["Contact"],
                    0,
                ),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("This Gmail, contact number, or account number is already registered.")
        return False


def signup() -> None:
    customer = register_customer()
    if customer is None:
        print("Registration cancelled")
        return
    if not confirm_details(customer):
        print("Registration cancelled")
        return
    if save_customer(customer):
        print("Congratulations, your account has been created!")
        print(f"Account Number: {customer['Account_Number']}")


def main() -> None:
    init_db()
    print("Press 1 for login")
    print("Press 2 for signup")
    query = input("Enter: ").strip()

    if query == "1":
        customer = login()
        if customer:
            account_menu(customer)
    elif query == "2":
        signup()
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()