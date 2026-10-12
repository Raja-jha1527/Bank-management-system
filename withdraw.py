from signup import get_connection
from deposit import parse_amount


def withdraw(account_number: str) -> None:
    amount = parse_amount(input("Amount to withdraw: ").strip())
    if amount is None:
        print("Invalid amount")
        return

    value = float(amount)
    with get_connection() as conn:
        # The WHERE clause blocks overdrafts atomically
        cursor = conn.execute(
            """
            UPDATE CUSTOMER SET Balance = Balance - ?
            WHERE Account_Number = ? AND Balance >= ?
            """,
            (value, account_number, value),
        )
        if cursor.rowcount == 0:
            print("Insufficient balance")
            return

        new_balance = conn.execute(
            "SELECT Balance FROM CUSTOMER WHERE Account_Number = ?",
            (account_number,),
        ).fetchone()[0]
        conn.execute(
            """
            INSERT INTO TRANSACTIONS (Account_Number, Type, Amount, Balance_After)
            VALUES (?, 'WITHDRAW', ?, ?)
            """,
            (account_number, value, new_balance),
        )
        conn.commit()

    print(f"Withdrawn {value:.2f}. New balance: {new_balance:.2f}")