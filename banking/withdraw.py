
from decimal import Decimal
from datetime import date

from banking.config import (
    get_connection,
    MIN_WITHDRAWAL,
    MINIMUM_BALANCE,
    DAILY_WITHDRAWAL_LIMIT
)

from banking.validators import validate_amount

from banking.exceptions import (
    ValidationError,
    AccountNotFoundError,
    AccountLockedError,
    InsufficientBalanceError
)


def withdraw_money(account_no: str, amount):
    """Withdraw money from an active bank account."""

    account_no = account_no.strip().upper()
    amount = validate_amount(amount)

    # Validate minimum withdrawal
    if amount < Decimal(str(MIN_WITHDRAWAL)):
        raise ValidationError(
            f"Minimum withdrawal amount is ₹{MIN_WITHDRAWAL}."
        )

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Step 1: Lock the account row
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

        # Step 2: Check available balance
        previous_balance = Decimal(str(account["balance"]))

        new_balance = previous_balance - amount

        if new_balance < Decimal(str(MINIMUM_BALANCE)):
            raise InsufficientBalanceError(
                f"Minimum balance of ₹{MINIMUM_BALANCE} must be maintained."
            )

        # Step 3: Create today's withdrawal tracker if absent
        today = date.today()

        cursor.execute(
            """
            INSERT IGNORE INTO daily_withdrawal_limits
            (account_no, limit_date, total_withdrawn)
            VALUES (%s, %s, 0.00)
            """,
            (account_no, today)
        )

        # Step 4: Lock today's withdrawal tracker row
        cursor.execute(
            """
            SELECT total_withdrawn
            FROM daily_withdrawal_limits
            WHERE account_no = %s
            AND limit_date = %s
            FOR UPDATE
            """,
            (account_no, today)
        )

        daily_record = cursor.fetchone()

        if daily_record is None:
            raise RuntimeError(
                "Unable to retrieve daily withdrawal record."
            )

        already_withdrawn = Decimal(
            str(daily_record["total_withdrawn"])
        )

        new_daily_total = already_withdrawn + amount

        # Step 5: Check daily withdrawal limit
        if new_daily_total > Decimal(
            str(DAILY_WITHDRAWAL_LIMIT)
        ):
            remaining_limit = (
                Decimal(str(DAILY_WITHDRAWAL_LIMIT))
                - already_withdrawn
            )

            raise ValidationError(
                f"Daily withdrawal limit exceeded. "
                f"Remaining limit: ₹{remaining_limit:.2f}"
            )

        # Step 6: Update account balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (new_balance, account_no)
        )

        # Step 7: Update daily withdrawal tracker
        cursor.execute(
            """
            UPDATE daily_withdrawal_limits
            SET total_withdrawn = %s
            WHERE account_no = %s
            AND limit_date = %s
            """,
            (new_daily_total, account_no, today)
        )

        # Step 8: Record transaction
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
            VALUES (%s, 'WITHDRAWAL', %s, %s, %s)
            """,
            (
                account_no,
                amount,
                new_balance,
                "Cash withdrawal"
            )
        )

        # Step 9: Record audit log
        cursor.execute(
            """
            INSERT INTO audit_log
            (account_no, event_type, details)
            VALUES (%s, %s, %s)
            """,
            (
                account_no,
                "WITHDRAWAL_SUCCESS",
                f"Withdrawn ₹{amount:.2f}"
            )
        )

        # Step 10: Commit all changes
        connection.commit()

        # Step 11: Return withdrawal receipt
        return {
            "account_no": account_no,
            "holder_name": account["holder_name"],
            "previous_balance": previous_balance,
            "withdrawal_amount": amount,
            "new_balance": new_balance,
            "daily_withdrawn": new_daily_total,
            "remaining_daily_limit": (
                Decimal(str(DAILY_WITHDRAWAL_LIMIT))
                - new_daily_total
            )
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()
