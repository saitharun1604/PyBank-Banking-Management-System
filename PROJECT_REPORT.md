# PYBANK – BANKING MANAGEMENT SYSTEM

**Project Report**

**Prepared by:** K Sai Tharun  
**Department:** Computer Science and Engineering  
**University:** Mohan Babu University  
**Project Technologies:** Python, MySQL  
**Project Type:** Banking Management System

---

# 1. Abstract

PyBank is a Python and MySQL-based Banking Management System developed to simulate essential banking operations through a menu-driven application.

The system provides account registration, customer authentication, deposits, withdrawals, balance enquiries, transaction history and account summaries.

It uses MySQL as its relational database to store customer account information, financial transactions, audit logs and daily withdrawal records.

The project demonstrates Python modular programming, database connectivity, input validation, exception handling and database transaction management.

# 2. Introduction

Banking management systems help organize customer accounts and financial transactions efficiently.

PyBank was developed to implement fundamental banking operations using Python and MySQL. The application provides a simple terminal-based interface through which customers can access banking services.

The system separates its functionality into individual Python modules, making the application easier to maintain and extend.

# 3. Problem Statement

Managing banking operations requires accurate account information, reliable transaction records and proper validation of financial activities.

The objective of this project is to develop a database-connected banking application that handles common banking operations while enforcing predefined business rules.

# 4. Project Objectives

- Develop a customer account registration system.
- Implement customer authentication using PIN verification.
- Generate unique account numbers.
- Implement deposit and withdrawal operations.
- Provide account balance enquiries.
- Maintain transaction history.
- Generate account summaries.
- Implement daily withdrawal restrictions.
- Maintain audit records.
- Integrate Python with MySQL.

# 5. Hardware and Software Requirements

## Hardware Requirements

- Computer or laptop
- Minimum 4 GB RAM
- Minimum 500 MB available storage
- Keyboard and monitor

## Software Requirements

- Operating System: Windows
- Programming Language: Python
- Database: MySQL 8.0
- Database Tool: MySQL Workbench
- IDE: Visual Studio Code
- Python Library: MySQL Connector/Python
- Version Control: Git and GitHub

# 6. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| MySQL | Database management |
| MySQL Connector | Database connectivity |
| VS Code | Development environment |
| Git | Version control |
| GitHub | Source code hosting |

# 7. System Architecture

The application follows a modular architecture.

## Main Components

1. Presentation Layer – Displays menus and customer information.
2. Application Layer – Handles account operations, validation and business logic.
3. Database Layer – Connects Python to MySQL and manages stored information.

## Application Workflow

Customer → Main Menu → Authentication → Customer Menu → Banking Operations → MySQL Database

# 8. Database Design

The project uses the following four main database tables.

## 8.1 Accounts

Stores customer account information.

Important fields include:

- Account number
- Customer name
- Account type
- Account balance
- Account status
- PIN authentication information

## 8.2 Transactions

Stores financial and balance enquiry records.

Important fields include:

- Transaction ID
- Account number
- Transaction type
- Transaction amount
- Balance after transaction
- Description
- Transaction date

## 8.3 Audit Log

Maintains records of important account activities.

## 8.4 Daily Withdrawal Limits

Tracks daily withdrawal totals for individual accounts.

# 9. Module Descriptions

## 9.1 Account Management

Provides customer registration and login functionality.

Features:
- Account number generation
- PIN validation
- PIN hashing
- Customer authentication
- Account locking after three incorrect PIN attempts

## 9.2 Deposit Management

Allows customers to deposit money.

Implemented business rules:
- Minimum deposit: ₹500
- Maximum deposit: ₹1,00,000

Successful deposits update account balances and transaction records.

## 9.3 Withdrawal Management

Allows customers to withdraw money.

Implemented business rules:
- Minimum withdrawal: ₹100
- Minimum account balance: ₹1,000
- Daily withdrawal limit: ₹50,000

The system checks available balance and daily withdrawal usage before processing withdrawals.

## 9.4 Balance Enquiry

Displays:
- Account number
- Customer name
- Account type
- Account status
- Available balance

Successful enquiries are recorded in transaction history.

## 9.5 Transaction History

Provides access to previous account transactions.

Features:
- Transaction history
- Transaction type filtering
- Date range filtering
- Pagination

## 9.6 Account Summary

Calculates:
- Total transactions
- Total deposits
- Total withdrawals
- Deposit count
- Withdrawal count
- Balance enquiry count

# 10. Security and Transaction Management

The project incorporates several security and reliability mechanisms:

- PIN hashing using SHA-256.
- Account locking after repeated incorrect login attempts.
- Input validation.
- Custom exception handling.
- Database transactions using commit and rollback.
- Row-level locking for concurrent withdrawal processing.
- Audit logging.

**Security improvement:** For production applications, replace plain SHA-256 PIN hashing with a salted, deliberately slow password-hashing algorithm such as Argon2id or PBKDF2. Additional controls are required before handling real financial information.

# 11. Testing and Results

The following scenarios are included in the project's testing plan.

| Test | Expected result |
|---|---|
| Account registration | Account created |
| Valid customer login | Login successful |
| Incorrect PIN | Login rejected |
| Three incorrect PIN attempts | Account locked |
| Valid deposit | Balance increased |
| Invalid deposit | Transaction rejected |
| Valid withdrawal | Balance decreased |
| Insufficient balance | Withdrawal rejected |
| Daily withdrawal limit exceeded | Withdrawal rejected |
| Balance enquiry | Current balance displayed |
| Transaction history | Records displayed |
| Account summary | Financial summary displayed |

Actual test outcomes and screenshots should be added after final verification.

# 12. Limitations

- The application currently uses a terminal-based interface.
- It is designed for educational purposes.
- It does not integrate with real banking payment networks.
- It does not provide production-grade authentication or authorization.
- It does not include a web-based administrator dashboard.

# 13. Future Enhancements

- Develop a graphical user interface.
- Build a web-based banking application.
- Add administrator functionality.
- Introduce email and SMS notifications.
- Generate downloadable transaction statements.
- Implement stronger authentication.
- Add automated unit and integration tests.
- Deploy the application using cloud infrastructure.

# 14. Conclusion

PyBank demonstrates the implementation of fundamental banking operations using Python and MySQL.

The project integrates account management, authentication, deposits, withdrawals, balance enquiries and transaction reporting into a modular application.

Through this project, practical knowledge was gained in Python programming, relational databases, SQL queries, exception handling, input validation and database transaction management.

The application provides a foundation for further development into a more comprehensive banking management solution.

# 15. References

1. Python Documentation – https://docs.python.org/3/
2. MySQL Documentation – https://dev.mysql.com/doc/
3. MySQL Connector/Python – https://dev.mysql.com/doc/connector-python/en/
4. Git Documentation – https://git-scm.com/doc
5. GitHub Documentation – https://docs.github.com/

---

**Project:** PyBank – Banking Management System  
**Author:** K Sai Tharun  
**University:** Mohan Babu University


