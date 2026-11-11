
from getpass import getpass

from banking.account import authenticate_account
from banking.withdraw import withdraw_money

from banking.exceptions import BankingError


def main():

    print("\n===================================")
    print("      PYBANK WITHDRAWAL TEST")
    print("===================================")

    try:
        account_no = input("Enter account number: ")

        pin = getpass("Enter your PIN: ")

        # Authenticate customer
        account = authenticate_account(account_no, pin)

        print(f"\nWelcome, {account['holder_name']}!")

        print(f"Current Balance: ₹{account['balance']:.2f}")

        # Enter withdrawal amount
        amount = input("\nEnter withdrawal amount: ₹")

        # Perform withdrawal
        receipt = withdraw_money(
            account_no,
            amount
        )

        # Display receipt
        print("\n===================================")
        print("       WITHDRAWAL RECEIPT")
        print("===================================")

        print(f"Account Number  : {receipt['account_no']}")
        print(f"Account Holder  : {receipt['holder_name']}")

        print("-----------------------------------")

        print(
            f"Previous Balance: "
            f"₹{receipt['previous_balance']:.2f}"
        )

        print(
            f"Withdrawal      : "
            f"₹{receipt['withdrawal_amount']:.2f}"
        )

        print("-----------------------------------")

        print(
            f"New Balance     : "
            f"₹{receipt['new_balance']:.2f}"
        )

        print(
            f"Today's Withdrawals: "
            f"₹{receipt['daily_withdrawn']:.2f}"
        )

        print(
            f"Remaining Daily Limit: "
            f"₹{receipt['remaining_daily_limit']:.2f}"
        )

        print("===================================")
        print("     WITHDRAWAL SUCCESSFUL!")
        print("===================================")

    except BankingError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
