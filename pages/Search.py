
import streamlit as st
import urllib.parse

from utils.theme import apply_magic_theme
from utils.poster_service import get_poster
from database.repository import MovieRepository
from database.user_repository import UserRepository

def star_rating(value):
    try:
        value = float(value)
    except:
        return "-"

    full = int(round(value))
    return "★" * full + "☆" * (10 - full)



movie_repo = MovieRepository()
user_repo = UserRepository()

st.set_page_config(
    page_title="Film Ara",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_magic_theme()

st.title("🔍 Film Ara")

# Session State
if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "watch_message" not in st.session_state:
    st.session_state.watch_message = ""

film_adi = st.text_input("Film adı gir")

# Arama butonu
if st.button("🔍 Ara", use_container_width=True):

    if film_adi.strip() == "":
        st.warning("Lütfen film adı gir.")

    else:
        st.session_state.search_results = movie_repo.find_by_title(film_adi)

# Daha sonra izle mesajı
if st.session_state.watch_message:
    st.success(st.session_state.watch_message)

# Sonuç yoksa
if film_adi.strip() != "" and len(st.session_state.search_results) == 0:
    st.error("❌ Film bulunamadı.")

# Sonuçları göster
for film in st.session_state.search_results:

    with st.container(border=True):

        poster_url = get_poster(film.title)

        col_img, col_info = st.columns([1, 3])

        # Poster sütunu
        with col_img:

            if poster_url:
                st.image(poster_url, width=150)

            else:
                st.markdown(
                    """
                    <div style="
                        width:150px;
                        height:225px;
                        border-radius:18px;
                        background:linear-gradient(135deg,#1B2A5B,#7C3AED);
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        text-align:center;
                        color:white;
                        font-weight:700;
                        font-size:18px;
                        box-shadow:0 0 14px rgba(124,58,237,0.35);
                    ">
                        🎬<br>Poster
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Bilgi sütunu
        with col_info:

            st.subheader(f"🎬 {film.title}")

            st.write(f"📅 **Yıl:** {film.year}")
            st.write(f"🎭 **Tür:** {film.genre}")
            st.write(f"🎥 **Yönetmen:** {film.director}")
            st.write(f"⭐ **IMDb:** {film.imdb}")

            if film.actors:
                st.write(f"🎬 **Oyuncular:** {film.actors}")

            # 🎬 Fragman butonu
            trailer_query = urllib.parse.quote(
                f"{film.title} official trailer"
            )

            trailer_url = (
                f"https://www.youtube.com/results?search_query={trailer_query}"
            )

            st.link_button(
                "🎬 Fragmanı İzle",
                trailer_url,
                use_container_width=True
            )

            st.divider()

            # Kütüphaneye ekle
            if user_repo.movie_exists(film.title):

                st.success("✅ Bu film zaten kütüphanende.")

            else:

                if st.button(
                    f"📚 {film.title} filmini kütüphaneye ekle",
                    key=f"add_{film.id}",
                    use_container_width=True
                ):

                    try:

                        user_repo.add_movie(
                            film.title,
                            film.genre,
                            film.director,
                            film.actors,
                            film.imdb,
                            0,
                            0,
                            ""
                        )

                        st.success("🎉 Film başarıyla eklendi!")

                    except Exception as e:

                        st.error(f"Hata oluştu:\n{e}")

            st.write("")

            # Daha sonra izle butonu
            if st.button(
                f"⏰ {film.title} daha sonra izle",
                key=f"watch_{film.id}",
                use_container_width=True
            ):

                try:

                    user_repo.add_to_watchlist(film.title)

                    st.session_state.watch_message = (
                        f"⏰ **{film.title}** izleme listesine eklendi."
                    )

                    st.success(st.session_state.watch_message)

                except Exception as e:

                    st.error(f"İzleme listesine eklenemedi:\n{e}")

        st.markdown("<br>", unsafe_allow_html=True)

