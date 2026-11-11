
from getpass import getpass

from banking.account import authenticate_account
from banking.deposit import deposit_money
from banking.exceptions import BankingError


def main():

    print("\n===================================")
    print("       PYBANK DEPOSIT TEST")
    print("===================================")

    try:
        account_no = input("Enter account number: ")

        pin = getpass("Enter your PIN: ")

        # Authenticate customer
        account = authenticate_account(account_no, pin)

        print(f"\nWelcome, {account['holder_name']}!")

        # Ask deposit amount
        amount = input("\nEnter deposit amount: ")

        # Perform deposit
        receipt = deposit_money(
            account_no,
            amount
        )

        # Display receipt
        print("\n===================================")
        print("         DEPOSIT RECEIPT")
        print("===================================")

        print(f"Account Number  : {receipt['account_no']}")
        print(f"Account Holder  : {receipt['holder_name']}")
        print(f"Previous Balance: ₹{receipt['previous_balance']:.2f}")
        print(f"Deposit Amount  : ₹{receipt['deposit_amount']:.2f}")
        print("-----------------------------------")
        print(f"New Balance     : ₹{receipt['new_balance']:.2f}")

        print("===================================")
        print("       DEPOSIT SUCCESSFUL!")
        print("===================================")

    except BankingError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
