"""
CineMind Content-Based Recommendation Engine

Bu modül TF-IDF ve Cosine Similarity kullanarak
film önerileri oluşturur.
"""

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    """
    İçerik tabanlı öneri sistemi.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent

        self.dataset_path = project_root / "datasets" / "movies.csv"

        self.movies = None
        self.tfidf = None
        self.similarity_matrix = None

    def fit(self):
        """
        Film verilerini yükler ve TF-IDF matrisini oluşturur.
        """

        self.movies = pd.read_csv(self.dataset_path)
        self.movies = self.movies.fillna("")

        self.movies["content"] = (
             self.movies["Genre"] + " " +
             self.movies["Director"] + " " +
             self.movies["Star1"] + " " +
             self.movies["Star2"] + " " +
             self.movies["Star3"] + " " +
             self.movies["Star4"] + " " +
             self.movies["Overview"]
)

        self.tfidf = TfidfVectorizer(stop_words="english")

        tfidf_matrix = self.tfidf.fit_transform(
            self.movies["content"]
        )

        self.similarity_matrix = cosine_similarity(tfidf_matrix)

    def recommend(self, movie_title: str, top_n: int = 5):
        """
        Verilen filme benzer filmleri önerir.
        """

        if self.movies is None:
            self.fit()

        movie = self.movies[
             self.movies["Series_Title"].str.lower() == movie_title.lower()
         ]
  
        if movie.empty:
            return []

        movie_index = movie.index[0]

        similarity_scores = list(
            enumerate(self.similarity_matrix[movie_index])
        )

        similarity_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        similarity_scores = similarity_scores[1:top_n + 1]

        recommendations = []

        for index, score in similarity_scores:
            recommendations.append(self.movies.iloc[index])

        return recommendations

    def recommend_for_user(self, watched_movies, top_n=10):
        """
        Kullanıcının izlediği filmlere göre öneri üretir.
        """

        if self.movies is None:
            self.fit()

        watched_indices = []

        for movie in watched_movies:

            result = self.movies[
                self.movies["Series_Title"].str.lower() == movie.lower()
            ]

            if not result.empty:
                watched_indices.append(result.index[0])

        if not watched_indices:
            return []

        scores = self.similarity_matrix[watched_indices].mean(axis=0)

        recommendations = []

        watched_lower = [movie.lower() for movie in watched_movies]

        for index, score in enumerate(scores):

            title = self.movies.iloc[index]["Series_Title"]

            if title.lower() not in watched_lower:
                recommendations.append((index, score))

        recommendations.sort(
            key=lambda x: x[1],
            reverse=True
        )

        result = []

        for index, score in recommendations[:top_n]:
            result.append(self.movies.iloc[index])

        return result