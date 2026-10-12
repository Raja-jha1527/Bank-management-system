from typing import Optional

from signup import get_connection


def get_balance(account_number: str) -> Optional[float]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT Balance FROM CUSTOMER WHERE Account_Number = ?",
            (account_number,),
        ).fetchone()
    return row[0] if row else None


def show_balance(account_number: str) -> None:
    balance = get_balance(account_number)
    if balance is None:
        print("Account not found")
        return
    print(f"Current balance: {balance:.2f}")


def show_history(account_number: str, limit: int = 10) -> None:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT Created_At, Type, Amount, Balance_After
            FROM TRANSACTIONS
            WHERE Account_Number = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (account_number, limit),
        ).fetchall()

    if not rows:
        print("No transactions yet")
        return

    print(f"\nLast {len(rows)} transactions (newest first)")
    print(f"{'Date/Time':<20}{'Type':<10}{'Amount':>12}{'Balance':>12}")
    print("-" * 54)
    for created_at, tx_type, amount, balance_after in rows:
        print(f"{created_at:<20}{tx_type:<10}{amount:>12.2f}{balance_after:>12.2f}")