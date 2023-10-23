import datetime
import hashlib


def generate_unique_key(user_id: int) -> str:
    data = 'ƛ' + str(user_id) + 'Ȿ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + 'ƪ'
    unique_key = hashlib.sha256(data.encode()).hexdigest()
    return unique_key
