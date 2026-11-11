
from getpass import getpass

from banking.account import authenticate_account

from banking.history import (
    get_transaction_history,
    get_account_summary
)

from banking.exceptions import BankingError


def main():

    print("\n===================================")
    print("       PYBANK TRANSACTION HISTORY")
    print("===================================")

    try:
        account_no = input("Enter account number: ")
        pin = getpass("Enter your PIN: ")

        account = authenticate_account(account_no, pin)

        print(f"\nWelcome, {account['holder_name']}!")

        print("\n1. All Transactions")
        print("2. Filter by Transaction Type")
        print("3. Filter by Date Range")
        print("4. Account Summary")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":

            transactions = get_transaction_history(account_no)

        elif choice == "2":

            txn_type = input(
                "Enter type (DEPOSIT/WITHDRAWAL/BALANCE_CHECK): "
            )

            transactions = get_transaction_history(
                account_no,
                txn_type=txn_type
            )

        elif choice == "3":

            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")

            transactions = get_transaction_history(
                account_no,
                start_date=start_date,
                end_date=end_date
            )

        elif choice == "4":

            summary = get_account_summary(account_no)

            print("\n========== ACCOUNT SUMMARY ==========")

            print(f"Total Transactions: {summary['total_transactions']}")
            print(f"Total Deposits: ₹{summary['total_deposits']:.2f}")
            print(f"Total Withdrawals: ₹{summary['total_withdrawals']:.2f}")

            print(f"Deposit Count: {summary['deposit_count']}")
            print(f"Withdrawal Count: {summary['withdrawal_count']}")
            print(f"Balance Enquiries: {summary['balance_check_count']}")

            return

        else:
            print("Invalid choice.")
            return

        print("\n========== TRANSACTION HISTORY ==========")

        if not transactions:
            print("No transactions found.")

        for txn in transactions:

            amount = (
                f"₹{txn['amount']:.2f}"
                if txn['amount'] is not None
                else "N/A"
            )

            print("-----------------------------------")
            print(f"Transaction ID: {txn['txn_id']}")
            print(f"Type: {txn['txn_type']}")
            print(f"Amount: {amount}")
            print(f"Balance After: ₹{txn['balance_after']:.2f}")
            print(f"Description: {txn['description']}")
            print(f"Date: {txn['txn_date']}")

    except BankingError as e:
        print(f"\nError: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nInvalid input: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
