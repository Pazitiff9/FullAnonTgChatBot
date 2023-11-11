import datetime
import hashlib
import random


def generate_unique_key(user_id: int) -> str:
    data = 'ƛ' + str(user_id) + 'Ȿ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + 'ƪ' + str(random.random())
    unique_key = hashlib.sha256(data.encode()).hexdigest()
    return unique_key
