
import hashlib
import secrets
from decimal import Decimal

from banking.config import (
    get_connection,
    MIN_OPENING_DEPOSIT,
    MAX_DEPOSIT
)

from banking.validators import (
    validate_name,
    validate_pin,
    validate_account_type,
    validate_amount
)

from banking.exceptions import (
    ValidationError,
    AccountNotFoundError,
    AccountLockedError
)


def hash_pin(pin: str) -> str:
    """Convert PIN into SHA-256 hash."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def generate_account_number(cursor) -> str:
    """Generate a unique account number."""

    while True:
        account_no = f"ACC{secrets.randbelow(10**12):012d}"

        cursor.execute(
            "SELECT account_no FROM accounts WHERE account_no = %s",
            (account_no,)
        )

        if cursor.fetchone() is None:
            return account_no


def write_audit_log(cursor, account_no, event_type, details):
    """Record an account-related event."""

    cursor.execute(
        """
        INSERT INTO audit_log
        (account_no, event_type, details)
        VALUES (%s, %s, %s)
        """,
        (account_no, event_type, details)
    )


def create_account(holder_name, pin, account_type, opening_deposit):
    """Create a new bank account."""

    # Validate customer inputs
    holder_name = validate_name(holder_name)
    pin = validate_pin(pin)
    account_type = validate_account_type(account_type)
    opening_deposit = validate_amount(opening_deposit)

    if opening_deposit < Decimal(str(MIN_OPENING_DEPOSIT)):
        raise ValidationError(
            f"Opening deposit must be at least ₹{MIN_OPENING_DEPOSIT}."
        )

    if opening_deposit > Decimal(str(MAX_DEPOSIT)):
        raise ValidationError(
            f"Opening deposit cannot exceed ₹{MAX_DEPOSIT}."
        )

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor()

        # Generate unique account number
        account_no = generate_account_number(cursor)

        # Hash the PIN
        pin_hash = hash_pin(pin)

        # Insert account
        cursor.execute(
            """
            INSERT INTO accounts
            (
                account_no,
                holder_name,
                pin_hash,
                balance,
                account_type
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                account_no,
                holder_name,
                pin_hash,
                opening_deposit,
                account_type
            )
        )

        # Record opening deposit
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
                opening_deposit,
                opening_deposit,
                "Initial account opening deposit"
            )
        )

        # Record account creation event
        write_audit_log(
            cursor,
            account_no,
            "ACCOUNT_CREATED",
            "New bank account created successfully."
        )

        connection.commit()

        return {
            "account_no": account_no,
            "holder_name": holder_name,
            "account_type": account_type,
            "balance": opening_deposit
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()


def authenticate_account(account_no, pin):
    """Authenticate customer using account number and PIN."""

    account_no = account_no.strip().upper()
    pin = validate_pin(pin)

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Lock account row during authentication
        cursor.execute(
            """
            SELECT *
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (account_no,)
        )

        account = cursor.fetchone()

        if account is None:
            write_audit_log(
                cursor,
                None,
                "LOGIN_FAILED",
                f"Login attempted for unknown account: {account_no}"
            )
            connection.commit()
            raise AccountNotFoundError("Account does not exist.")

        if account["status"] == "LOCKED":
            write_audit_log(
                cursor,
                account_no,
                "LOGIN_BLOCKED",
                "Login attempted on locked account."
            )
            connection.commit()
            raise AccountLockedError(
                "Your account is locked. Contact the bank."
            )

        if account["status"] != "ACTIVE":
            connection.commit()
            raise ValidationError("Account is not active.")

        entered_hash = hash_pin(pin)

        if entered_hash == account["pin_hash"]:

            cursor.execute(
                """
                UPDATE accounts
                SET failed_attempts = 0
                WHERE account_no = %s
                """,
                (account_no,)
            )

            write_audit_log(
                cursor,
                account_no,
                "LOGIN_SUCCESS",
                "Customer logged in successfully."
            )

            connection.commit()

            return account

        # Incorrect PIN
        failed_attempts = account["failed_attempts"] + 1

        if failed_attempts >= 3:

            cursor.execute(
                """
                UPDATE accounts
                SET failed_attempts = %s,
                    status = 'LOCKED'
                WHERE account_no = %s
                """,
                (failed_attempts, account_no)
            )

            write_audit_log(
                cursor,
                account_no,
                "ACCOUNT_LOCKED",
                "Account locked after 3 incorrect PIN attempts."
            )

            connection.commit()

            raise AccountLockedError(
                "Three incorrect attempts. Your account is now locked."
            )

        cursor.execute(
            """
            UPDATE accounts
            SET failed_attempts = %s
            WHERE account_no = %s
            """,
            (failed_attempts, account_no)
        )

        write_audit_log(
            cursor,
            account_no,
            "LOGIN_FAILED",
            f"Incorrect PIN attempt {failed_attempts}."
        )

        connection.commit()

        remaining = 3 - failed_attempts

        raise ValidationError(
            f"Incorrect PIN. {remaining} attempt(s) remaining."
        )

    except (AccountNotFoundError, AccountLockedError, ValidationError):
        raise

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()
