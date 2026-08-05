from database.database import Database


class UserRepository:

    def __init__(self):
        self.database = Database()
        self.create_table()

    def create_table(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_movies(
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
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watchlist(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_title TEXT NOT NULL,
                genre TEXT,
                director TEXT,
                imdb REAL
            )
        """)

        connection.commit()
        connection.close()

    def movie_exists(self, movie_title):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM user_movies
            WHERE LOWER(movie_title) = LOWER(?)
        """, (movie_title,))

        exists = cursor.fetchone()[0]
        connection.close()

        return exists > 0

    def add_movie(
        self,
        movie_title,
        genre,
        director,
        actors,
        imdb,
        user_rating,
        favorite,
        watch_date
    ):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO user_movies(
                movie_title,
                genre,
                director,
                actors,
                imdb,
                user_rating,
                favorite,
                watch_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            movie_title,
            genre,
            director,
            actors,
            imdb,
            user_rating,
            favorite,
            watch_date
        ))

        connection.commit()
        connection.close()

    def get_all_movies(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                movie_title,
                genre,
                director,
                imdb,
                user_rating,
                favorite,
                watch_date
            FROM user_movies
            ORDER BY id DESC
        """)

        movies = cursor.fetchall()
        connection.close()

        return movies

    def delete_movie(self, movie_title):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM user_movies
            WHERE LOWER(movie_title) = LOWER(?)
        """, (movie_title,))

        connection.commit()
        deleted = cursor.rowcount
        connection.close()

        return deleted

    def toggle_favorite(self, movie_title):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE user_movies
            SET favorite = CASE
                WHEN favorite = 1 THEN 0
                ELSE 1
            END
            WHERE LOWER(movie_title) = LOWER(?)
        """, (movie_title,))

        connection.commit()
        connection.close()

    def get_total_movies(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM user_movies")
        total = cursor.fetchone()[0]
        connection.close()

        return total

    def get_favorite_count(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM user_movies
            WHERE favorite = 1
        """)

        total = cursor.fetchone()[0]
        connection.close()

        return total

    def get_average_rating(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT AVG(user_rating)
            FROM user_movies
        """)

        avg = cursor.fetchone()[0]
        connection.close()

        if avg is None:
            return 0

        return round(avg, 2)

    def get_last_movie(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT movie_title
            FROM user_movies
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return "-"

        return row[0]

    def get_this_month_count(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM user_movies
            WHERE strftime('%Y-%m', watch_date) = strftime('%Y-%m', 'now')
        """)

        total = cursor.fetchone()[0]
        connection.close()

        return total

    def get_this_year_count(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM user_movies
            WHERE strftime('%Y', watch_date) = strftime('%Y', 'now')
        """)

        total = cursor.fetchone()[0]
        connection.close()

        return total

    # --- TEK İZLEME LİSTESİ (WATCHLIST) METODLARI ---

    def add_to_watchlist(self, movie_title, genre=None, director=None, imdb=None):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO watchlist(
                movie_title,
                genre,
                director,
                imdb
            )
            VALUES (?, ?, ?, ?)
        """, (movie_title, genre, director, imdb))

        connection.commit()
        connection.close()

    def get_watchlist(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                movie_title,
                genre,
                director,
                imdb
            FROM watchlist
            ORDER BY id DESC
        """)

        movies = cursor.fetchall()
        connection.close()

        return movies

    def remove_from_watchlist(self, movie_title):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM watchlist
            WHERE LOWER(movie_title) = LOWER(?)
        """, (movie_title,))

        connection.commit()
        connection.close()

    # --- İSTATİSTİK METODLARI ---

    def get_genre_statistics(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                genre,
                COUNT(*)
            FROM user_movies
            GROUP BY genre
            ORDER BY COUNT(*) DESC
        """)

        result = cursor.fetchall()
        connection.close()

        return result

    def get_top_rated_movies(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                movie_title,
                user_rating
            FROM user_movies
            ORDER BY user_rating DESC
            LIMIT 5
        """)

        movies = cursor.fetchall()
        connection.close()

        return movies

    def get_favorite_directors(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT director, COUNT(*) AS total
            FROM user_movies
            GROUP BY director
            ORDER BY total DESC
            LIMIT 5
        """)

        directors = cursor.fetchall()
        connection.close()

        return directors

    def get_favorite_actors(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT actors
            FROM user_movies
        """)

        rows = cursor.fetchall()
        connection.close()

        actor_count = {}

        for row in rows:
            if not row[0]:
                continue

            actors = row[0].split(",")
            for actor in actors:
                actor = actor.strip()
                if actor:
                    actor_count[actor] = actor_count.get(actor, 0) + 1

        return sorted(
            actor_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

    def get_favorite_genres(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT genre, COUNT(*) AS total
            FROM user_movies
            GROUP BY genre
            ORDER BY total DESC
            LIMIT 5
        """)

        rows = cursor.fetchall()
        connection.close()

        return rows

    def get_average_imdb(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT AVG(imdb)
            FROM user_movies
        """)

        avg = cursor.fetchone()[0]
        connection.close()

        return round(avg, 2) if avg else 0

    def get_average_user_rating(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT AVG(user_rating)
            FROM user_movies
        """)

        avg = cursor.fetchone()[0]
        connection.close()

        return round(avg, 2) if avg else 0

    def get_imdb_scores(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT imdb
            FROM user_movies
            WHERE imdb IS NOT NULL
        """)

        scores = [row[0] for row in cursor.fetchall()]
        connection.close()

        return scores

    def get_watch_dates(self):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT watch_date
            FROM user_movies
            WHERE watch_date IS NOT NULL
        """)

        dates = [row[0] for row in cursor.fetchall()]
        connection.close()

        return dates

    def update_movie(self, movie_title, user_rating, watch_date):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE user_movies
            SET
                user_rating = ?,
                watch_date = ?
            WHERE LOWER(movie_title) = LOWER(?)
        """, (
            user_rating,
            watch_date,
            movie_title
        ))

        connection.commit()
        connection.close()

    def update_favorite(self, movie_title, favorite):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE user_movies
            SET favorite = ?
            WHERE LOWER(movie_title) = LOWER(?)
        """, (
            favorite,
            movie_title
        ))

        connection.commit()
        connection.close()