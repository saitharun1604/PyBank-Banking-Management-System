
import re
from decimal import Decimal, InvalidOperation

from banking.exceptions import ValidationError


def validate_name(name: str) -> str:
    name = name.strip()

    if len(name) < 3 or len(name) > 50:
        raise ValidationError(
            "Name must contain between 3 and 50 characters."
        )

    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", name):
        raise ValidationError(
            "Name can contain letters, spaces, dots, apostrophes and hyphens only."
        )

    return name


def validate_pin(pin: str) -> str:
    if not re.fullmatch(r"\d{4}", pin):
        raise ValidationError(
            "PIN must contain exactly 4 digits."
        )

    return pin


def validate_account_type(account_type: str) -> str:
    account_type = account_type.strip().upper()

    if account_type not in ("SAVINGS", "CURRENT"):
        raise ValidationError(
            "Account type must be SAVINGS or CURRENT."
        )

    return account_type


def validate_amount(amount) -> Decimal:
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        raise ValidationError("Enter a valid amount.")

    if not value.is_finite():
        raise ValidationError("Amount must be a finite number.")

    if value <= 0:
        raise ValidationError("Amount must be greater than zero.")

    if value.as_tuple().exponent < -2:
        raise ValidationError(
            "Amount cannot have more than 2 decimal places."
        )

    return value.quantize(Decimal("0.01"))
