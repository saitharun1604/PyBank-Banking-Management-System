
from datetime import date, datetime, timedelta

from banking.config import get_connection
from banking.exceptions import ValidationError


ALLOWED_TYPES = (
    "DEPOSIT",
    "WITHDRAWAL",
    "BALANCE_CHECK"
)


def get_transaction_history(
    account_no,
    limit=10,
    offset=0,
    txn_type=None,
    start_date=None,
    end_date=None
):
    """Retrieve filtered and paginated transaction history."""

    account_no = account_no.strip().upper()

    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValidationError("Limit must be between 1 and 100.")

    if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
        raise ValidationError("Offset cannot be negative.")

    if txn_type:
        txn_type = txn_type.strip().upper()

        if txn_type not in ALLOWED_TYPES:
            raise ValidationError("Invalid transaction type.")

    # Validate dates
    if start_date:
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)

        if not isinstance(start_date, date):
            raise ValidationError("Invalid start date.")

    if end_date:
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        if not isinstance(end_date, date):
            raise ValidationError("Invalid end date.")

    if start_date and end_date and start_date > end_date:
        raise ValidationError("Start date cannot be after end date.")

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                txn_id,
                account_no,
                txn_type,
                amount,
                balance_after,
                description,
                txn_date
            FROM transactions
            WHERE account_no = %s
        """

        params = [account_no]

        # Filter by transaction type
        if txn_type:
            query += " AND txn_type = %s"
            params.append(txn_type)

        # Filter by date range
        if start_date:
            query += " AND txn_date >= %s"
            params.append(datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query += " AND txn_date < %s"
            params.append(
                datetime.combine(
                end_date + timedelta(days=1),
                datetime.min.time()
            )
        )

        query += """
            ORDER BY txn_date DESC, txn_id DESC
            LIMIT %s OFFSET %s
        """

        params.extend([limit, offset])

        cursor.execute(query, tuple(params))

        return cursor.fetchall()

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()


def get_account_summary(account_no):
    """Calculate account transaction summary."""

    account_no = account_no.strip().upper()

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection unavailable.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_transactions,

                COALESCE(
                    SUM(CASE
                        WHEN txn_type = 'DEPOSIT'
                        THEN amount ELSE 0
                    END), 0
                ) AS total_deposits,

                COALESCE(
                    SUM(CASE
                        WHEN txn_type = 'WITHDRAWAL'
                        THEN amount ELSE 0
                    END), 0
                ) AS total_withdrawals,

                SUM(CASE
                    WHEN txn_type = 'DEPOSIT'
                    THEN 1 ELSE 0
                END) AS deposit_count,

                SUM(CASE
                    WHEN txn_type = 'WITHDRAWAL'
                    THEN 1 ELSE 0
                END) AS withdrawal_count,

                SUM(CASE
                    WHEN txn_type = 'BALANCE_CHECK'
                    THEN 1 ELSE 0
                END) AS balance_check_count

            FROM transactions
            WHERE account_no = %s
            """,
            (account_no,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        connection.close()
