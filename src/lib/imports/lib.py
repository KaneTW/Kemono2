from typing import Union
from src.types.kemono_error import KemonoError, KemonoValidationError
from .types import service_constraints, Encodings


def validate_import_key(key: str, service: str) -> Union[KemonoError, str]:
    """
    Validates the key according to these rules:
    - Trim spaces from both sides.
    - Minimum and maximum length of the key (depending on service).
    - Encoding
    """
    formatted_key = key.strip()
    key_length = len(formatted_key.encode('utf-8'))
    constraints = service_constraints[service]
    is_valid_length = None

    # is key of fixed length
    if (constraints.length):
        is_valid_length = constraints.length == key_length
    else:
        is_valid_length = constraints.min_length < key_length < constraints.max_length

    # is key within length constraints
    if (not is_valid_length):
        req_length = constraints.length if constraints.length else f"{constraints.min_length}-{constraints.max_length}"

        return KemonoValidationError(f"""
            The key \"{key}\" of service \"{service}\" and length \"{key_length}\" is not valid length. Required length is \"{req_length}\".
        """)

    # is of valid case, if present
    if (constraints.case == "lower" and not formatted_key.islower()):
        return KemonoValidationError(f"""
            The key \"{key}\" of service \"{service}\" is of invalid casing.
        """)

    # is key ascii
    if (constraints.encoding == Encodings.ASCII and not formatted_key.isascii()):
        return KemonoValidationError(f"The key \"{key}\" of service \"{service}\" is of invalid encoding.")

    # is matching a pattern

    if (constraints.pattern and not constraints.pattern.search(formatted_key)):
        return KemonoValidationError(f"The key \"{key}\" of service \"{service}\" is of invalid pattern.")

    return formatted_key
