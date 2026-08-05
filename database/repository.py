"""
repository.py

CineMind veritabanı işlemleri.
"""

from database.database import Database
from database.models import Movie


class MovieRepository:
    """
    Film veritabanı işlemleri.
    """

    def __init__(self):
        self.database = Database()

    def add_movie(self, movie: Movie) -> None:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO movies
            (
                title,
                year,
                genre,
                director,
                actors,
                imdb,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                movie.title,
                movie.year,
                movie.genre,
                movie.director,
                movie.actors,
                movie.imdb,
                movie.description,
            ),
        )

        connection.commit()
        connection.close()

    def get_all_movies(self) -> list[Movie]:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM movies")

        rows = cursor.fetchall()

        connection.close()

        movies = []

        for row in rows:
            movies.append(
                Movie(
                    id=row["id"],
                    title=row["title"],
                    year=row["year"],
                    genre=row["genre"],
                    director=row["director"],
                    actors=row["actors"],
                    imdb=row["imdb"],
                    description=row["description"],
                )
            )

        return movies

    def find_by_title(self, title: str) -> list[Movie]:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE LOWER(title) LIKE LOWER(?)
            ORDER BY imdb DESC
            """,
            (f"%{title}%",)
        )

        rows = cursor.fetchall()

        connection.close()

        movies = []

        for row in rows:
            movies.append(
                Movie(
                    id=row["id"],
                    title=row["title"],
                    year=row["year"],
                    genre=row["genre"],
                    director=row["director"],
                    actors=row["actors"],
                    imdb=row["imdb"],
                    description=row["description"],
                )
            )

        return movies

    def find_by_genre(self, genre: str) -> list[Movie]:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE LOWER(genre) LIKE LOWER(?)
            ORDER BY imdb DESC
            """,
            (f"%{genre}%",)
        )

        rows = cursor.fetchall()

        connection.close()

        movies = []

        for row in rows:
            movies.append(
                Movie(
                    id=row["id"],
                    title=row["title"],
                    year=row["year"],
                    genre=row["genre"],
                    director=row["director"],
                    actors=row["actors"],
                    imdb=row["imdb"],
                    description=row["description"],
                )
            )

        return movies

    def find_by_director(self, director: str) -> list[Movie]:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE LOWER(director) LIKE LOWER(?)
            ORDER BY imdb DESC
            """,
            (f"%{director}%",)
        )

        rows = cursor.fetchall()

        connection.close()

        movies = []

        for row in rows:
            movies.append(
                Movie(
                    id=row["id"],
                    title=row["title"],
                    year=row["year"],
                    genre=row["genre"],
                    director=row["director"],
                    actors=row["actors"],
                    imdb=row["imdb"],
                    description=row["description"],
                )
            )

        return movies

    def find_by_imdb(self, rating: float) -> list[Movie]:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE imdb >= ?
            ORDER BY imdb DESC
            """,
            (rating,)
        )

        rows = cursor.fetchall()

        connection.close()

        movies = []

        for row in rows:
            movies.append(
                Movie(
                    id=row["id"],
                    title=row["title"],
                    year=row["year"],
                    genre=row["genre"],
                    director=row["director"],
                    actors=row["actors"],
                    imdb=row["imdb"],
                    description=row["description"],
                )
            )

        return movies

    def find_by_year(self, year: int) -> list[Movie]:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE year = ?
            ORDER BY imdb DESC
            """,
            (year,)
        )

        rows = cursor.fetchall()

        connection.close()

        movies = []

        for row in rows:
            movies.append(
                Movie(
                    id=row["id"],
                    title=row["title"],
                    year=row["year"],
                    genre=row["genre"],
                    director=row["director"],
                    actors=row["actors"],
                    imdb=row["imdb"],
                    description=row["description"],
                )
            )

        return movies
    
    def get_movie_by_id(self, movie_id: int) -> Movie | None:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE id = ?
            """,
            (movie_id,)
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return Movie(
            id=row["id"],
            title=row["title"],
            year=row["year"],
            genre=row["genre"],
            director=row["director"],
            actors=row["actors"],
            imdb=row["imdb"],
            description=row["description"],
        )

    def update_movie(self, movie: Movie) -> None:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE movies
            SET
                title = ?,
                year = ?,
                genre = ?,
                director = ?,
                actors = ?,
                imdb = ?,
                description = ?
            WHERE id = ?
            """,
            (
                movie.title,
                movie.year,
                movie.genre,
                movie.director,
                movie.actors,
                movie.imdb,
                movie.description,
                movie.id,
            ),
        )

        connection.commit()
        connection.close()

    def delete_movie(self, movie_id: int) -> None:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM movies
            WHERE id = ?
            """,
            (movie_id,),
        )

        connection.commit()
        connection.close()

    def random_movie(self) -> Movie | None:

        connection = self.database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            ORDER BY RANDOM()
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return Movie(
            id=row["id"],
            title=row["title"],
            year=row["year"],
            genre=row["genre"],
            director=row["director"],
            actors=row["actors"],
            imdb=row["imdb"],
            description=row["description"],
        )

    def recommend_movies(self, genre, min_imdb, year):

       connection = self.database.get_connection()
       cursor = connection.cursor()

       cursor.execute(
          """
          SELECT *
          FROM movies
          WHERE genre LIKE ?
            AND imdb >= ?
            AND year >= ?
          ORDER BY imdb DESC
          LIMIT 10
          """,
          (f"%{genre}%", min_imdb, year)
      )

       rows = cursor.fetchall()
       connection.close()

       movies = []

       for row in rows:
         movies.append(
             Movie(
                id=row["id"],
                title=row["title"],
                year=row["year"],
                genre=row["genre"],
                director=row["director"],
                actors=row["actors"],
                imdb=row["imdb"],
                description=row["description"],
            )
        )

       return movies