from dataclasses import dataclass
from typing import Dict, List

from src.internals.types import PageProps
from src.types.account import Account, Notification, Service_Key

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

@dataclass
class ServiceKeysProps(PageProps):
    service_keys: List[Service_Key]
    currentPage: str = "account"
    title: str = "Your service keys"
