import sqlite3
from pathlib import Path

DB_PATH = Path("database/cinemind.db")

class MarathonRepository:

    def __init__(self):
        self._create_table()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_table(self):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS marathons(
                director TEXT PRIMARY KEY,
                films TEXT,
                current_day INTEGER DEFAULT 1
            )
            """
        )

        conn.commit()
        conn.close()

    def start_marathon(self, director, films):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            "REPLACE INTO marathons(director, films, current_day) VALUES (?, ?, 1)",
            (director, "|".join(films))
        )

        conn.commit()
        conn.close()

    def get_marathon(self, director):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT films, current_day FROM marathons WHERE director=?",
            (director,)
        )

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        films = row[0].split("|")
        return {
            "films": films,
            "current_day": row[1]
        }

    def complete_today(self, director):
        marathon = self.get_marathon(director)

        if not marathon:
            return

        next_day = marathon["current_day"] + 1

        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            "UPDATE marathons SET current_day=? WHERE director=?",
            (next_day, director)
        )

        conn.commit()
        conn.close()

    def reset_marathon(self, director):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM marathons WHERE director=?",
            (director,)
        )

        conn.commit()
        conn.close()