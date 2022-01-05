from .types import ServiceConstraints, ValidationResult


def validate_import_key(key: str, service: str) -> ValidationResult:
    """
    Validates the key according to the `service` rules
    """
    # Trim spaces from both sides.
    formatted_key = key.strip()
    errors = ServiceConstraints[service](formatted_key, [])

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        modified_result=formatted_key
    )
