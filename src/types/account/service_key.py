from dataclasses import dataclass
from datetime import datetime

from src.internals.types import DatabaseEntry

@dataclass
class Service_Key(DatabaseEntry):
    id: int
    service: str
    added: datetime
    dead: bool
    contributor_id: int = None
    encrypted_key: str = None
    discord_channel_ids: str = None
