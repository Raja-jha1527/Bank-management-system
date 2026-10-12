from decimal import Decimal, InvalidOperation
from typing import Optional

from signup import get_connection

MAX_AMOUNT = Decimal("1000000")


def parse_amount(text: str) -> Optional[Decimal]:
    try:
        amount = Decimal(text)
    except InvalidOperation:
        return None
    if not amount.is_finite() or amount <= 0:
        return None
    if amount.as_tuple().exponent < -2:  # more than 2 decimal places
        return None
    if amount > MAX_AMOUNT:
        return None
    return amount


def deposit(account_number: str) -> None:
    amount = parse_amount(input("Amount to deposit: ").strip())
    if amount is None:
        print(f"Invalid amount (positive, max 2 decimals, up to {MAX_AMOUNT})")
        return

    value = float(amount)
    with get_connection() as conn:
        # Balance update and history record are committed together
        conn.execute(
            "UPDATE CUSTOMER SET Balance = Balance + ? WHERE Account_Number = ?",
            (value, account_number),
        )
        new_balance = conn.execute(
            "SELECT Balance FROM CUSTOMER WHERE Account_Number = ?",
            (account_number,),
        ).fetchone()[0]
        conn.execute(
            """
            INSERT INTO TRANSACTIONS (Account_Number, Type, Amount, Balance_After)
            VALUES (?, 'DEPOSIT', ?, ?)
            """,
            (account_number, value, new_balance),
        )
        conn.commit()

    print(f"Deposited {value:.2f}. New balance: {new_balance:.2f}")
