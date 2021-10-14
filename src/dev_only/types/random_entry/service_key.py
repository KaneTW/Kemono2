from flask import g

from src.dev_only.internals import service_name
from src.utils.random import generate_random_boolean, generate_random_number, generate_random_date
from src.types.account import Service_Key

def generate_discord_ids():
    if generate_random_boolean():
        ids = [str(generate_random_number()) for id in range(generate_random_number(1, 20))]
        return " ".join(ids)
    else:
        return None

class Random_Service_key(Service_Key):
    def __init__(self):
        self.id = generate_random_number()
        self.contributor_id = g.account.id if g.get('account') else generate_random_number()
        self.service = service_name
        self.added = generate_random_date()
        self.dead = generate_random_boolean()
        self.discord_channel_ids = generate_discord_ids()
        self.encrypted_key = ""
