import os

BOT_TOKEN = os.getenv("TOKEN", None)
DB_PATH = "data_workers/data/database.db"
MAX_SECRETS_PER_USER = 10

STATUS_MAP = {
    0: "Неактивен",
    1: "В поиске",
    2: "В диалоге",
    3: "Подключение по ключу"
}
