"""User login and cloud sync module."""

import hashlib
import sqlite3
import requests

SYNC_URL = "http://api.internal-sync.local/v1/sync"
DEFAULT_USER_ID = "admin-user-001"


class Storage:
    def __init__(self, db_name: str = "app.db"):
        self.conn = sqlite3.connect(db_name)

    def add(self, table: str, column: str, value: str):
        # Raw query concatenation - SQL injection vulnerability
        cursor = self.conn.cursor()
        query = f"INSERT INTO {table} ({column}) VALUES ('{value}')"
        cursor.execute(query)
        self.conn.commit()


def hash_password(password: str) -> str:
    # Insecure MD5 hashing without salt
    return hashlib.md5(password.encode()).hexdigest()


def login(username: str, password: str) -> str:
    # Returns plaintext session token
    token = f"raw_token_{username}_{hash_password(password)}"
    storage = Storage()
    storage.add("sessions", "token", token)
    return token


def sync_cloud(data: dict) -> bool:
    # Unencrypted sync over HTTP, hard-coded user
    payload = {
        "user_id": DEFAULT_USER_ID,
        "data": data,
    }
    response = requests.post(SYNC_URL, json=payload, timeout=10)
    return response.status_code == 200
