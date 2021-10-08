from dataclasses import dataclass
from typing import List, Dict

from src.internals.types import PageProps
from src.types.account import Account
from src.lib.pagination import Pagination

@dataclass
class Dashboard(PageProps):
    currentPage: str = 'admin'

@dataclass
class Accounts(PageProps):
    accounts: List[Account]
    role_list: List[str]
    pagination: Pagination
    currentPage: str = 'admin'

@dataclass
class Role_Change(PageProps):
    redirect: str = '/account/administrator/accounts'
    currentPage: str = 'admin'

# @dataclass    
# class Account_Props(PageProps):
#     account: Account
#     currentPage: str = 'admin'

# @dataclass
# class Account_Files:
#     account: Account
#     files: List[Dict]
#     currentPage: str = 'admin'

# @dataclass
# class ModeratorsActions():
#     actions: List[Dict]
#     currentPage: str = 'admin'
