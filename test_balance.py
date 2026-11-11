
from getpass import getpass

from banking.account import authenticate_account
from banking.balance import check_balance

from banking.exceptions import BankingError


def main():

    print("\n===================================")
    print("       PYBANK BALANCE ENQUIRY")
    print("===================================")

    try:
        account_no = input("Enter account number: ")

        pin = getpass("Enter your PIN: ")

        # Authenticate customer
        account = authenticate_account(
            account_no,
            pin
        )

        print(f"\nWelcome, {account['holder_name']}!")

        # Retrieve and record balance enquiry
        details = check_balance(account_no)

        # Display account information
        print("\n===================================")
        print("        ACCOUNT DETAILS")
        print("===================================")

        print(f"Account Number : {details['account_no']}")
        print(f"Account Holder : {details['holder_name']}")
        print(f"Account Type   : {details['account_type']}")
        print(f"Account Status : {details['status']}")

        print("-----------------------------------")

        print(f"Available Balance: ₹{details['balance']:.2f}")

        print("===================================")
        print("    BALANCE ENQUIRY SUCCESSFUL!")
        print("===================================")

    except BankingError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
