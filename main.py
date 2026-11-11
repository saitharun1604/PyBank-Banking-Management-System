
from getpass import getpass
from decimal import Decimal

from banking.account import (
    create_account,
    authenticate_account
)

from banking.deposit import deposit_money
from banking.withdraw import withdraw_money
from banking.balance import check_balance

from banking.history import (
    get_transaction_history,
    get_account_summary
)

from banking.validators import validate_amount

from banking.exceptions import BankingError

from banking.display import (
    show_main_menu,
    show_account_menu,
    display_account_details,
    display_transaction_history,
    display_account_summary
)


def register_account():
    """Register a new customer account."""

    print("\n========== ACCOUNT REGISTRATION ==========")

    try:
        name = input("Enter your full name: ")

        pin = getpass("Create your 4-digit PIN: ")

        account_type = input(
            "Account type (SAVINGS/CURRENT): "
        )

        deposit = input("Opening deposit (₹): ")

        result = create_account(
            name,
            pin,
            account_type,
            deposit
        )

        print("\n===================================")
        print("       ACCOUNT CREATED!")
        print("===================================")

        print(f"Account Number : {result['account_no']}")
        print(f"Holder Name    : {result['holder_name']}")
        print(f"Account Type   : {result['account_type']}")
        print(f"Opening Balance: ₹{result['balance']:.2f}")

        print("\nPlease save your account number.")

    except BankingError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


def customer_deposit(account_no):

    print("\n========== DEPOSIT MONEY ==========")

    amount = input("Enter deposit amount (₹): ")

    receipt = deposit_money(
        account_no,
        amount
    )

    print("\n========== DEPOSIT RECEIPT ==========")

    print(f"Account Number  : {receipt['account_no']}")
    print(f"Account Holder  : {receipt['holder_name']}")
    print(f"Previous Balance: ₹{receipt['previous_balance']:.2f}")
    print(f"Deposit Amount  : ₹{receipt['deposit_amount']:.2f}")
    print("-------------------------------------")
    print(f"New Balance     : ₹{receipt['new_balance']:.2f}")

    print("\nDEPOSIT SUCCESSFUL!")


def customer_withdraw(account_no):

    print("\n========== WITHDRAW MONEY ==========")

    amount = input("Enter withdrawal amount (₹): ")

    receipt = withdraw_money(
        account_no,
        amount
    )

    print("\n========== WITHDRAWAL RECEIPT ==========")

    print(f"Account Number  : {receipt['account_no']}")
    print(f"Account Holder  : {receipt['holder_name']}")
    print(f"Previous Balance: ₹{receipt['previous_balance']:.2f}")
    print(f"Withdrawal      : ₹{receipt['withdrawal_amount']:.2f}")
    print("----------------------------------------")
    print(f"New Balance     : ₹{receipt['new_balance']:.2f}")
    print(f"Daily Withdrawn : ₹{receipt['daily_withdrawn']:.2f}")
    print(f"Remaining Limit : ₹{receipt['remaining_daily_limit']:.2f}")

    print("\nWITHDRAWAL SUCCESSFUL!")


def customer_balance(account_no):

    details = check_balance(account_no)

    display_account_details(details)


def show_paginated_history(
    account_no,
    txn_type=None,
    start_date=None,
    end_date=None
):
    """Display transaction history page by page."""

    page_size = 10
    page = 0

    while True:

        offset = page * page_size

        transactions = get_transaction_history(
            account_no,
            limit=page_size,
            offset=offset,
            txn_type=txn_type,
            start_date=start_date,
            end_date=end_date
        )

        if not transactions:
            if page == 0:
                print("\nNo transactions found.")
            else:
                print("\nNo more transactions available.")
            break

        print(f"\n========== PAGE {page + 1} ==========")

        display_transaction_history(transactions)

        print("\nN - Next Page")
        print("P - Previous Page")
        print("Q - Return to Account Menu")

        choice = input("Enter choice: ").strip().upper()

        if choice == "N":

            if len(transactions) < page_size:
                print("\nYou have reached the last page.")
            else:
                page += 1

        elif choice == "P":

            if page > 0:
                page -= 1
            else:
                print("\nYou are already on the first page.")

        elif choice == "Q":
            break

        else:
            print("\nInvalid choice.")



def customer_history(account_no):

    print("\n========== TRANSACTION HISTORY ==========")

    print("1. All Transactions")
    print("2. Filter by Transaction Type")
    print("3. Filter by Date Range")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":

        show_paginated_history(account_no)

    elif choice == "2":

        print("\nTransaction Types:")
        print("DEPOSIT")
        print("WITHDRAWAL")
        print("BALANCE_CHECK")

        txn_type = input("\nEnter transaction type: ")

        show_paginated_history(
            account_no,
            txn_type=txn_type
        )

    elif choice == "3":

        start_date = input(
            "Enter start date (YYYY-MM-DD): "
        )

        end_date = input(
            "Enter end date (YYYY-MM-DD): "
        )

        show_paginated_history(
            account_no,
            start_date=start_date,
            end_date=end_date
        )

    else:
        print("Invalid choice.")


def customer_summary(account_no):

    summary = get_account_summary(account_no)

    display_account_summary(summary)


def customer_menu(account):

    account_no = account["account_no"]

    while True:

        show_account_menu(account["holder_name"])

        choice = input("\nEnter your choice: ").strip()

        try:

            if choice == "1":

                customer_deposit(account_no)

            elif choice == "2":

                customer_withdraw(account_no)

            elif choice == "3":

                customer_balance(account_no)

            elif choice == "4":

                customer_history(account_no)

            elif choice == "5":

                customer_summary(account_no)

            elif choice == "6":

                print("\nYou have successfully logged out.")
                break

            else:

                print("\nInvalid choice. Select 1 to 6.")

        except BankingError as e:

            print(f"\nBanking Error: {e}")

        except (ValueError, TypeError) as e:

            print(f"\nInvalid input: {e}")

        except Exception as e:

            print(f"\nUnexpected error: {e}")


def customer_login():

    print("\n========== CUSTOMER LOGIN ==========")

    try:

        account_no = input("Enter account number: ")

        pin = getpass("Enter your PIN: ")

        account = authenticate_account(
            account_no,
            pin
        )

        print("\nLogin successful!")

        print(f"Welcome, {account['holder_name']}!")

        customer_menu(account)

    except BankingError as e:

        print(f"\nLogin failed: {e}")

    except Exception as e:

        print(f"\nUnexpected error: {e}")


def main():

    print("\nInitializing PyBank...")

    from banking.db_setup import create_tables

    try:
        create_tables()
    except Exception as e:
        print(f"Unable to initialize database: {e}")
        return

    while True:

        show_main_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            register_account()

        elif choice == "2":

            customer_login()

        elif choice == "3":

            print("\nThank you for using PyBank!")
            print("Have a great day!")
            break

        else:

            print("\nInvalid choice. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
