# PyBank – Banking Management System

A Python and MySQL-based Banking Management System designed to simulate essential banking operations with secure authentication, transaction management and account monitoring.

## Project Overview

PyBank is a menu-driven banking application developed using Python and MySQL. It allows customers to create accounts, securely log in, deposit money, withdraw money, check balances and view transaction history.

## Features

- Customer account registration
- Automatic unique account number generation
- Secure PIN hashing using SHA-256
- Customer authentication
- Account locking after three incorrect PIN attempts
- Deposit and withdrawal operations
- Minimum balance enforcement
- Daily withdrawal limit tracking
- Balance enquiry
- Transaction history with filtering and pagination
- Account financial summary
- Audit logging
- MySQL database integration
- Database transaction management

## Technologies Used

- Python
- MySQL
- MySQL Connector/Python
- VS Code
- Git and GitHub

## Project Structure

```text
PyBank/
├── banking/
│   ├── __init__.py
│   ├── config.py
│   ├── db_setup.py
│   ├── exceptions.py
│   ├── validators.py
│   ├── account.py
│   ├── deposit.py
│   ├── withdraw.py
│   ├── balance.py
│   ├── history.py
│   └── display.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Banking Rules

| Rule | Limit |
|---|---:|
| Minimum Deposit | ₹500 |
| Maximum Deposit | ₹1,00,000 |
| Minimum Withdrawal | ₹100 |
| Minimum Balance | ₹1,000 |
| Daily Withdrawal Limit | ₹50,000 |
| Maximum Incorrect PIN Attempts | 3 |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/saitharun1604/PyBank-Banking-Management-System.git
```

### 2. Navigate to the project

```bash
cd PyBank-Banking-Management-System
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure MySQL

Create the database:

```sql
CREATE DATABASE banking_db;
```

Configure your MySQL credentials using environment variables before running the application.

### 7. Run the application

```bash
python main.py
```

## Main Menu

1. Open New Account
2. Login to Existing Account
3. Exit

## Customer Menu

1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Transaction History
5. Account Summary
6. Logout

## Database Tables

- accounts
- transactions
- audit_log
- daily_withdrawal_limits

## Learning Outcomes

- Python modular programming
- MySQL database connectivity
- CRUD operations
- SQL transactions
- Row-level locking
- Exception handling
- Authentication and PIN hashing
- Banking business rule implementation

## Author

**K Sai Tharun**

GitHub: https://github.com/saitharun1604

Portfolio: https://saitharun-portfolio.netlify.app/

---

*This project is developed for educational purposes and is not intended for real financial transactions.*