from dataclasses import dataclass
from typing import Dict, List

from src.internals.types import PageProps
from src.types.account import Account, Notification

@dataclass
class AccountPageProps(PageProps):
    account: Account
    notifications_count: int
    currentPage: str = "account"
    title: str = "Your account page"

@dataclass
class NotificationsProps(PageProps):
    notifications: List[Notification]
    currentPage: str = "account"
