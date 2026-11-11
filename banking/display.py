
def show_main_menu():
    print("\n" + "=" * 40)
    print("          WELCOME TO PYBANK")
    print("=" * 40)
    print("\n1. Open New Account")
    print("2. Login to Existing Account")
    print("3. Exit")


def show_account_menu(holder_name):
    print("\n" + "=" * 40)
    print("       PYBANK CUSTOMER MENU")
    print("=" * 40)

    print(f"\nWelcome, {holder_name}!\n")

    print("1. Deposit Money")
    print("2. Withdraw Money")
    print("3. Check Balance")
    print("4. Transaction History")
    print("5. Account Summary")
    print("6. Logout")


def display_account_details(account):
    print("\n" + "=" * 40)
    print("          ACCOUNT DETAILS")
    print("=" * 40)

    print(f"Account Number : {account['account_no']}")
    print(f"Account Holder : {account['holder_name']}")
    print(f"Account Type   : {account['account_type']}")
    print(f"Account Status : {account['status']}")
    print(f"Balance        : ₹{account['balance']:.2f}")

    print("=" * 40)


def display_transaction_history(transactions):
    print("\n" + "=" * 65)
    print("                 TRANSACTION HISTORY")
    print("=" * 65)

    if not transactions:
        print("No transactions found.")
        return

    for txn in transactions:

        amount = (
            f"₹{txn['amount']:.2f}"
            if txn['amount'] is not None
            else "N/A"
        )

        print("-" * 65)
        print(f"Transaction ID : {txn['txn_id']}")
        print(f"Type           : {txn['txn_type']}")
        print(f"Amount         : {amount}")
        print(f"Balance After  : ₹{txn['balance_after']:.2f}")
        print(f"Description    : {txn['description']}")
        print(f"Date           : {txn['txn_date']}")

    print("=" * 65)


def display_account_summary(summary):
    print("\n" + "=" * 40)
    print("           ACCOUNT SUMMARY")
    print("=" * 40)

    print(f"Total Transactions : {summary['total_transactions']}")
    print(f"Total Deposits     : ₹{summary['total_deposits']:.2f}")
    print(f"Total Withdrawals  : ₹{summary['total_withdrawals']:.2f}")

    print(f"Deposit Count      : {summary['deposit_count']}")
    print(f"Withdrawal Count   : {summary['withdrawal_count']}")
    print(f"Balance Enquiries  : {summary['balance_check_count']}")

    print("=" * 40)
