
class BankingError(Exception):
    """Base exception for banking operations."""
    pass


class ValidationError(BankingError):
    """Raised when user input is invalid."""
    pass


class AccountNotFoundError(BankingError):
    """Raised when an account does not exist."""
    pass


class AccountLockedError(BankingError):
    """Raised when an account is locked."""
    pass


class InsufficientBalanceError(BankingError):
    """Raised when account balance is insufficient."""
    pass


class TransactionError(BankingError):
    """Raised when a transaction fails."""
    pass
