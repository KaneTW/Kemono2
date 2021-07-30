from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from packaging.version import parse as parse_version

@dataclass
class __Agreement:
    """
    The user's agreement.
    """
    name: str
    agreed_at: datetime
    version: str
    def is_outdated(self, version: str) -> bool:
        current_version = parse_version(self.version)
        new_version = parse_version(version)
        return current_version < new_version

@dataclass
class __Import:
    """
    The user's import.
    """
    id: str
    service: str
    approved: list[str]
    rejected: list[str]
    pending: list[str]

@dataclass
class __Profile:
    id: str
    username: str
    password: str
    created_at: datetime
    imports: list[__Import]
    agreements: list[__Agreement]

class __Account:
    def __init__(self) -> None:
        self.Agreement = __Agreement
        self.Import = __Import
        self.Profile = __Profile

# account = __Account()
