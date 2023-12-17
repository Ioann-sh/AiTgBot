import sqlite3

class DB:

    def __init__(self, settings):
        self.conn = sqlite3.connect(settings['PATH'])
        self.cursor = self.conn.cursor()
        print("database up")

    def __del__(self):
        self.conn.close()
        print("database connection closed")

    def getUserByUserId(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=:user_id", {"user_id": user_id})
        return self.cursor.fetchone()

    def registration(self, name, user_id):
        query = "INSERT INTO users (name, user_id) VALUES (:name, :user_id)"
        val = (name, user_id)
        self.cursor.execute(query, val)
        return self.conn.commit()