from dataclasses import dataclass
from datetime import datetime

from src.internals.types import DatabaseEntry
# from typing import Optional, Union, Literal
# from packaging.version import parse as parse_version

account_roles = ['consumer', 'moderator', 'administrator']
visible_roles = account_roles[:-1]

@dataclass
class Account(DatabaseEntry):
    id: int
    username: str
    created_at: datetime
    role: str

# @dataclass
# class Consumer(Account):
#     pass
    
# @dataclass
# class Moderator(Account):
#     pass

# @dataclass
# class Administrator(Account):
#     pass

# class Agreement:
#     """
#     The user's agreement.
#     """
#     name: str
#     agreed_at: datetime
#     version: str
#     def is_outdated(self, version: str) -> bool:
#         current_version = parse_version(self.version)
#         new_version = parse_version(version)
#         return current_version < new_version

# class __Import:
#     """
#     The user's import.
#     """
#     id: str
#     service: str
#     approved: list[str]
#     rejected: list[str]
#     pending: list[str]
