import sqlite3


class SQLiteManager:
    def __init__(self, db_file_path):
        self.conn = sqlite3.connect(db_file_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, user_status INT);")
        self.conn.execute("CREATE TABLE IF NOT EXISTS chats(first_user_id INT, second_user_id INT);")
        self.conn.execute("CREATE TABLE IF NOT EXISTS secrets(user_id INT, secret_value TEXT);")
        self.conn.commit()

    def is_user_registered(self, user_id: int) -> bool:
        cursor = self.conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return bool(cursor.fetchone())

    def register_new_user(self, new_user_id: int):
        self.conn.execute("INSERT INTO users (user_id, user_status) VALUES (?, 0)", (new_user_id,))
        self.conn.commit()

    def update_user_status(self, user_id: int, new_status: int):
        self.conn.execute("UPDATE users SET user_status = ? WHERE user_id = ?", (new_status, user_id))
        self.conn.commit()

    def get_user_status(self, user_id: int) -> int:
        cursor = self.conn.execute("SELECT user_status FROM users WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()
        return data[0] if data else 0

    def find_companion(self, old_user_id: int) -> tuple[int]:
        cursor = self.conn.execute("SELECT user_id FROM users "
                                   "WHERE user_status = 1 AND user_id != ? ORDER BY RANDOM() LIMIT 1", (old_user_id,))
        return cursor.fetchone()

    def register_new_chat(self, first_user: int, second_user: int):
        self.conn.execute("INSERT INTO chats (first_user_id, second_user_id) VALUES (?, ?)", (first_user, second_user))
        self.conn.commit()

    def find_chat_by_id(self, user_id) -> tuple[int, int]:
        cursor = self.conn.execute("SELECT first_user_id, second_user_id FROM chats "
                                   f"WHERE first_user_id = {user_id} OR second_user_id = {user_id}")
        return cursor.fetchone()

    def delete_chat(self, part_chat_id: int):
        self.conn.execute(f"DELETE FROM chats WHERE first_user_id = {part_chat_id} OR second_user_id = {part_chat_id}")
        self.conn.commit()

    def add_user_secret(self, user_id: int, secret: str):
        self.conn.execute(f"INSERT INTO secrets (user_id, secret_value) VALUES (?, ?)", (user_id, secret))
        self.conn.commit()

    def delete_user_secret(self, secret: str):
        self.conn.execute(f"DELETE FROM secrets WHERE secret_value = ?", (secret,))
        self.conn.commit()

    def find_user_by_secret(self, secret: str) -> tuple[int]:
        cursor = self.conn.execute("SELECT user_id FROM secrets WHERE secret_value = ?", (secret,))
        return cursor.fetchone()

    def count_user_secrets(self, user_id: int) -> int:
        cursor = self.conn.execute("SELECT COUNT(user_id) FROM secrets WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]

    def close(self):
        self.conn.close()
