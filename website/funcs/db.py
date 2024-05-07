import sqlite3, json, re, datetime
import hashlib


class Users(object):
    @staticmethod
    def init():
        conn = sqlite3.connect("dbs/users.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                session_key TEXT NOT NULL
            )
        """
        )
        conn.commit()
        return True

    @staticmethod
    def check(username, password):
        if not password:
            conn = sqlite3.connect("dbs/users.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return True
            else:
                return False
        conn = sqlite3.connect("dbs/users.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def add(username, password, session_key):
        try:
            conn = sqlite3.connect("dbs/users.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, session_key) VALUES (?, ?, ?)",
                (username, hashlib.sha256(password.encode()).hexdigest(), session_key),
            )
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def user_info(session_key):
        try:
            conn = sqlite3.connect("dbs/users.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE session_key = ?", (session_key,))
            user = cursor.fetchone()
            conn.close()
            return user
        except Exception as e:
            print(e)
            return False