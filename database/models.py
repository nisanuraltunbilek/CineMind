"""
models.py

CineMind veri modelleri.

Bu dosya uygulamanın kullanacağı temel nesneleri içerir.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    """
    Film modeli.
    """

    id: Optional[int] = None

    title: str = ""
    year: int = 0

    genre: str = ""

    director: str = ""

    actors: str = ""

    imdb: float = 0.0

    description: str = ""


@dataclass
class UserMovie:
    """
    Kullanıcının izlediği film modeli.
    """

    id: Optional[int] = None

    movie_id: int = 0

    rating: float = 0.0

    favorite: bool = False

    watch_date: str = ""