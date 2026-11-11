
from decimal import Decimal

from banking.config import (
    get_connection,
    MIN_DEPOSIT,
    MAX_DEPOSIT
)

from banking.validators import validate_amount
from banking.exceptions import (
    ValidationError,
    AccountNotFoundError,
    AccountLockedError
)


def deposit_money(account_no: str, amount):
    """Deposit money into an active bank account."""

    account_no = account_no.strip().upper()
    amount = validate_amount(amount)

    # Check deposit limits
    if amount < Decimal(str(MIN_DEPOSIT)):
        raise ValidationError(
            f"Minimum deposit amount is ₹{MIN_DEPOSIT}."
        )

    if amount > Decimal(str(MAX_DEPOSIT)):
        raise ValidationError(
            f"Maximum deposit amount is ₹{MAX_DEPOSIT}."
        )

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Lock the account row
        cursor.execute(
            """
            SELECT account_no, holder_name, balance, status
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (account_no,)
        )

        account = cursor.fetchone()

        if account is None:
            raise AccountNotFoundError(
                "Account does not exist."
            )

        if account["status"] == "LOCKED":
            raise AccountLockedError(
                "Your account is locked."
            )

        if account["status"] != "ACTIVE":
            raise ValidationError(
                "Account is not active."
            )

        # Calculate new balance
        previous_balance = Decimal(str(account["balance"]))
        new_balance = previous_balance + amount

        # Update account balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (new_balance, account_no)
        )

        # Insert transaction record
        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_no,
                txn_type,
                amount,
                balance_after,
                description
            )
            VALUES (%s, 'DEPOSIT', %s, %s, %s)
            """,
            (
                account_no,
                amount,
                new_balance,
                "Cash deposit"
            )
        )

        # Insert audit record
        cursor.execute(
            """
            INSERT INTO audit_log
            (account_no, event_type, details)
            VALUES (%s, %s, %s)
            """,
            (
                account_no,
                "DEPOSIT_SUCCESS",
                f"Deposited ₹{amount:.2f}"
            )
        )

        # Save all database changes
        connection.commit()

        # Return receipt information
        return {
            "account_no": account_no,
            "holder_name": account["holder_name"],
            "previous_balance": previous_balance,
            "deposit_amount": amount,
            "new_balance": new_balance
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()
