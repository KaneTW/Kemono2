from datetime import datetime, timedelta
import string
from random import randint, choice

varchar_vocab = string.ascii_letters + string.digits
text_vocab = string.printable
unix_epoch_start = datetime.fromtimestamp(30256871)

def generate_random_string(min_length: int = 5, max_length: int = 250, vocabulary: str = varchar_vocab) -> str:
    string_length = randint(min_length, max_length)
    result_string = ''.join(choice(vocabulary) for char in range(string_length))

    return result_string

def generate_random_number(min: int = 1, max: int = 999999) -> int:
    return randint(min, max)

def generate_random_boolean() -> bool:
    result = bool(randint(0, 1))

    return result

def generate_random_date(min_date: datetime = unix_epoch_start, max_date: datetime = datetime.now()) -> datetime:
    int_delta = int((max_date - min_date).total_seconds())
    random_second = randint(0, int_delta)
    random_date = min_date + timedelta(seconds=random_second)
    return random_date
