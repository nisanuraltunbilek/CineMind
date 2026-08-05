from database.models import Movie
from database.repository import MovieRepository


class MovieService:
    """
    Film işlemlerini yöneten servis katmanı.
    """

    def __init__(self):
        self.repository = MovieRepository()

    def add_movie(self, movie: Movie) -> None:
        self.repository.add_movie(movie)

    def get_all_movies(self) -> list[Movie]:
        return self.repository.get_all_movies()

    def find_movies(self, title: str) -> list[Movie]:
        return self.repository.find_by_title(title)

    def get_movie(self, movie_id: int) -> Movie | None:
        return self.repository.get_movie_by_id(movie_id)

    def update_movie(self, movie: Movie) -> None:
        self.repository.update_movie(movie)

    def delete_movie(self, movie_id: int) -> None:
        self.repository.delete_movie(movie_id)