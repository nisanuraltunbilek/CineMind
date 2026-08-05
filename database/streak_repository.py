import sqlite3
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path("database/cinemind.db")

class StreakRepository:

    def __init__(self):
        self._create_table()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_table(self):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_stats(
                id INTEGER PRIMARY KEY,
                last_login TEXT,
                streak INTEGER DEFAULT 0
            )
            """
        )

        conn.commit()
        conn.close()

    def update_login(self):

        today = date.today()

        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT last_login, streak FROM user_stats WHERE id=1"
        )

        row = cur.fetchone()

        if row is None:

            cur.execute(
                "INSERT INTO user_stats(id, last_login, streak) VALUES (1, ?, 1)",
                (str(today),)
            )

            conn.commit()
            conn.close()
            return 1

        last_login = date.fromisoformat(row[0])
        streak = row[1]

        if last_login == today:

            conn.close()
            return streak

        if last_login == today - timedelta(days=1):
            streak += 1
        else:
            streak = 1

        cur.execute(
            "UPDATE user_stats SET last_login=?, streak=? WHERE id=1",
            (str(today), streak)
        )

        conn.commit()
        conn.close()

        return streak