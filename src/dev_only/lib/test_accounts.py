import string
import json
import os

from random import Random

from configs.constants import test_path
from src.lib.account import create_account

from typing import List

class Account_Creds:
    def __init__(self,
        username: str,
        password: str
    ) -> None:
        self.username = username
        self.password = password

acc_random = Random('Sneed')
username_vocabulary = string.ascii_letters + string.digits
password_vocabulary = string.ascii_letters + string.digits + string.punctuation

def register_test_accounts() -> List[Account_Creds]:
    accounts = make_test_accounts()
    print(f"Made {len(accounts)} accounts")
    for account in accounts:
        is_created = create_account(account.username, account.password)
        
        print(f"Created account № {accounts.index(account) + 1}")
        if (not is_created):
            print(f"Failed to create an account with the name \"{account.username}\" and password of \"{account.password}\"")
    
    return accounts

def write_test_accounts_data(account_data: List[Account_Creds]) -> bool:
    output_file = str(test_path) + "/accounts.json"
    if os.path.isdir(test_path) == False:
        os.mkdir(test_path)

    with open(output_file, 'wt') as f:
        f.write(create_accounts_json(account_data))
        f.close()
    print(f"Saved credentials for created accounts at \"{output_file}\".")
    return True

def make_test_accounts(count: int = 100) -> List[Account_Creds]:
    accounts = [generate_creds() for item in range(count)]

    return accounts

def generate_creds() -> Account_Creds:
    user = Account_Creds(
        username= generate_random_string(5, 20, username_vocabulary, acc_random),
        password= generate_random_string(10, 255, password_vocabulary, acc_random)
    )

    return user

def generate_random_string(min_length: int, max_length: int, vocabulary: str, random: Random = acc_random) -> str:
    string_length = random.randint(min_length, max_length)
    result_string = ''.join(random.choice(vocabulary) for char in range(string_length))

    return result_string

def create_accounts_json(accounts: List[Account_Creds]) -> str:
    return json.dumps(accounts, 
        default= lambda x: x.__dict__,
        indent=2
    )
