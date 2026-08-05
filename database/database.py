from pathlib import Path
import sqlite3


class Database:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        data_folder = project_root / "data"
        data_folder.mkdir(exist_ok=True)

        self.db_path = data_folder / "cinemind.db"

    def get_connection(self):

        print("=" * 50)
        print("DB PATH:", self.db_path)
        print("=" * 50)

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        return connection

    def initialize(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        # Film tablosu
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                year INTEGER,

                genre TEXT,

                director TEXT,

                actors TEXT,

                imdb REAL,

                description TEXT
            )
            """
        )

        # Kullanıcı kütüphanesi
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_movies (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                movie_title TEXT NOT NULL,

                genre TEXT,

                director TEXT,

                actors TEXT,

                imdb REAL,

                user_rating REAL,

                favorite INTEGER DEFAULT 0,

                watch_date TEXT
            )
            """
        )

        # Daha Sonra İzle listesi
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT UNIQUE
            )
            """
        )

        connection.commit()
        connection.close()


if __name__ == "__main__":

    database = Database()

    database.initialize()

    print("✅ Veritabanı hazır.")