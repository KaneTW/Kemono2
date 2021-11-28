from typing import Union
from src.types.kemono_error import KemonoError, KemonoValidationError
from .types import service_constraints


def validate_import_key(key: str, service: str) -> Union[KemonoError, str]:
    """
    Validates the key according to these rules:
    - Trim spaces from both sides.
    - Minimum and maximum length of the key (depending on service).
    - ASCII characters only.
    """
    formatted_key = key.strip()
    key_length = len(formatted_key.encode('utf-8'))
    constraints = service_constraints[service]
    is_valid_length = constraints.min_length < key_length < constraints.max_length

    # key is within length constraints
    if (not is_valid_length):
        return KemonoValidationError(f"The key \"{key}\" of service \"{service}\" and length \"{key_length}\" is outside of \"{constraints.min_length} - {constraints.max_length}\" range. You should let the administrator know about this.")

    # key is ascii
    if (not formatted_key.isascii()):
        return KemonoValidationError(f"The key \"{key}\" is of invalid encoding.")

    return formatted_key
