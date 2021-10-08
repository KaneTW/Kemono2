from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, unique

from typing import Optional, TypedDict
from src.internals.types import DatabaseEntry

@dataclass
class Notification(DatabaseEntry):
    id: int
    account_id: int
    type: str
    created_at: datetime
    extra_info: Optional[TypedDict]
    is_seen: bool= False

@unique
class Notification_Types(IntEnum):
    ACCOUNT_ROLE_CHANGE = 1

class ACCOUNT_ROLE_CHANGE(TypedDict):
    old_role: str
    new_role: str

notification_extra = {
    Notification_Types.ACCOUNT_ROLE_CHANGE: lambda old_role, new_role: ACCOUNT_ROLE_CHANGE(old_role= old_role, new_role= new_role)
}
