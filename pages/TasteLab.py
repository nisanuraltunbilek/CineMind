
import streamlit as st
from utils.theme import apply_magic_theme
from database.user_repository import UserRepository

repo = UserRepository()

st.set_page_config(
    page_title="Film Zevki Laboratuvarı",
    page_icon="🎴",
    layout="centered"
)
apply_magic_theme()

st.markdown(
    """
    <style>
    .stApp{
        background: linear-gradient(180deg,#0B1026,#111B47,#1B2A5B);
    }

    .movie-card{
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 28px;
        padding: 40px;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    .movie-title{
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .movie-meta{
        font-size: 18px;
        color: #E8E8F0;
        margin-bottom: 6px;
    }

    .hint{
        text-align:center;
        color:#C7D2FE;
        margin-top:10px;
        margin-bottom:20px;
    }

    div[data-testid="column"]:nth-of-type(1) button{
        background:#BEE7FF !important;
        color:#083358 !important;
        border:none !important;
        border-radius:18px !important;
        height:64px !important;
        font-size:20px !important;
        font-weight:700 !important;
    }

    div[data-testid="column"]:nth-of-type(2) button{
        background:#E7D4FF !important;
        color:#4A148C !important;
        border:none !important;
        border-radius:18px !important;
        height:64px !important;
        font-size:20px !important;
        font-weight:700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;color:white;'>🎴 Film Zevki Laboratuvarı</h1>", unsafe_allow_html=True)
st.markdown("<p class='hint'>Beğendiklerini sağa, beğenmediklerini sola gönder.</p>", unsafe_allow_html=True)

movies = repo.get_all_movies()

if not movies:
    st.info("Önce kütüphanene birkaç film ekle.")
    st.stop()

if "taste_index" not in st.session_state:
    st.session_state.taste_index = 0

if "liked_movies" not in st.session_state:
    st.session_state.liked_movies = []

if "disliked_movies" not in st.session_state:
    st.session_state.disliked_movies = []

if "reaction" not in st.session_state:
    st.session_state.reaction = ""

idx = st.session_state.taste_index

# Emoji geri bildirimi
if st.session_state.reaction:
    st.markdown(
        f"<div style='text-align:center;font-size:42px;margin:20px 0;'>{st.session_state.reaction}</div>",
        unsafe_allow_html=True
    )

if idx >= len(movies):

    st.success("🎉 Tüm filmleri değerlendirdin!")

    st.markdown("### 💜 Beğendiklerin")

    if st.session_state.liked_movies:
        for m in st.session_state.liked_movies:
            st.write(f"• {m}")

    st.markdown("### 💙 Beğenmediklerin")

    if st.session_state.disliked_movies:
        for m in st.session_state.disliked_movies:
            st.write(f"• {m}")

    if st.button("🔄 Baştan Başla", use_container_width=True):
        st.session_state.taste_index = 0
        st.session_state.liked_movies = []
        st.session_state.disliked_movies = []
        st.session_state.reaction = ""
        st.rerun()

    st.stop()

movie = movies[idx]

title = movie[0]
genre = movie[1]
director = movie[2]
imdb = movie[3]

st.markdown(
    f"""
    <div class="movie-card">
        <div class="movie-title">🎬 {title}</div>
        <div class="movie-meta">🎭 {genre}</div>
        <div class="movie-meta">🎥 {director}</div>
        <div class="movie-meta">⭐ IMDb: {imdb}</div>
    </div>
    """,
    unsafe_allow_html=True
)

left, right = st.columns(2, gap="large")

with left:
    if st.button("👎 Beğenmedim", use_container_width=True):

        st.session_state.disliked_movies.append(title)
     
        st.session_state.taste_index += 1
        st.rerun()

with right:
    if st.button("👍 Beğendim", use_container_width=True):

        st.session_state.liked_movies.append(title)
        st.balloons()
        st.session_state.taste_index += 1
        st.rerun()

st.progress((idx + 1) / len(movies))

st.caption(f"{idx + 1} / {len(movies)} film değerlendirildi")
