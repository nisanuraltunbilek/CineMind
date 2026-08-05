import streamlit as st
from utils.theme import apply_magic_theme
from database.repository import MovieRepository
from database.user_repository import UserRepository
from datetime import date

repo = MovieRepository()
user_repo = UserRepository()

st.set_page_config(
    page_title="AI Önerileri",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)
apply_magic_theme()

st.title("🤖 CineMind AI")
st.caption("Ruh haline göre sana film önerelim ✨")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox(
        "😊 Ruh Halin",
        [
            "Mutlu",
            "Duygusal",
            "Heyecanlı",
            "Gizem",
            "Korku",
            "Romantik",
            "Bilim Kurgu"
        ]
    )

    genre = st.selectbox(
        "🎭 Tür",
        [
            "Action",
            "Adventure",
            "Drama",
            "Comedy",
            "Crime",
            "Fantasy",
            "Sci-Fi",
            "Animation",
            "Romance",
            "Thriller"
        ]
    )

with col2:
    imdb = st.slider(
        "⭐ Minimum IMDb",
        5.0,
        10.0,
        8.0,
        0.1
    )

    year = st.slider(
        "📅 En Eski Yıl",
        1950,
        2025,
        2000
    )

st.write("")

# Önerilen filmleri session state üzerinde saklayarak sayfa yenilenmelerinde kaybolmasını engelliyoruz
if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = None

if st.button("✨ Bana Film Öner", use_container_width=True):
    st.session_state.recommended_movies = repo.recommend_movies(
        genre,
        imdb,
        year
    )

movies = st.session_state.recommended_movies

if movies is not None:
    if not movies:
        st.warning("Bu filtrelere uygun film bulunamadı.")
    else:
        st.success(f"🎬 {len(movies)} film bulundu.")
        st.info(
            f"💡 Bu öneriler **{mood}** ruh hali, **{genre}** türü, "
            f"**{year}+** yılı ve **{imdb}+ IMDb** filtresine göre seçildi."
        )

        st.markdown("---")

        for movie in movies:
            with st.container(border=True):
                st.subheader(f"🎬 {movie.title}")

                c1, c2 = st.columns(2)

                with c1:
                    st.write(f"📅 **Yıl:** {movie.year}")
                    st.write(f"🎭 **Tür:** {movie.genre}")
                    st.write(f"🎥 **Yönetmen:** {movie.director}")

                with c2:
                    st.write(f"⭐ **IMDb:** {movie.imdb}")
                    st.write(f"🎬 **Oyuncular:** {movie.actors}")

                if hasattr(movie, "description") and movie.description:
                    st.write(f"📝 **Konu:** {movie.description}")

                st.markdown("---")

                b1, b2 = st.columns(2)

                with b1:
                    if st.button(
                        "📚 Kütüphaneye Ekle",
                        key=f"lib_{movie.title}",
                        use_container_width=True
                    ):
                        if user_repo.movie_exists(movie.title):
                            st.info("Bu film zaten kütüphanende.")
                        else:
                            user_repo.add_movie(
                                movie.title,
                                movie.genre,
                                movie.director,
                                movie.actors,
                                movie.imdb,
                                0,
                                0,
                                ""
                            )
                            st.success(f"🎉 {movie.title} kütüphanene eklendi!")

                with b2:
                    if st.button(
                        "⏰ Daha Sonra İzle",
                        key=f"watch_{movie.title}",
                        use_container_width=True
                    ):
                        user_repo.add_to_watchlist(movie.title)
                        st.success("Daha sonra izle listesine eklendi.")

                st.markdown("")