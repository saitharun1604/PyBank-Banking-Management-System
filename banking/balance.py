
from banking.config import get_connection

from banking.exceptions import (
    AccountNotFoundError,
    AccountLockedError,
    ValidationError
)


def check_balance(account_no: str):
    """Retrieve account balance and record the enquiry."""

    account_no = account_no.strip().upper()

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Retrieve and lock account information
        cursor.execute(
            """
            SELECT
                account_no,
                holder_name,
                balance,
                account_type,
                status
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
                "Your account is locked. Balance enquiry is unavailable."
            )

        if account["status"] != "ACTIVE":
            raise ValidationError(
                "Your account is inactive."
            )

        # Record balance enquiry
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
            VALUES (%s, 'BALANCE_CHECK', NULL, %s, %s)
            """,
            (
                account_no,
                account["balance"],
                "Customer balance enquiry"
            )
        )

        connection.commit()

        return {
            "account_no": account["account_no"],
            "holder_name": account["holder_name"],
            "balance": account["balance"],
            "account_type": account["account_type"],
            "status": account["status"]
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()
