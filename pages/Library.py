from datetime import date, datetime
import urllib.parse
import pandas as pd
import streamlit as st

from database.user_repository import UserRepository
from utils.poster_service import get_poster
from utils.theme import apply_magic_theme

def star_rating(value):
    try:
        value = float(value)
    except:
        return "-"

    full = int(round(value))
    return "★" * full + "☆" * (10 - full)

# Repository başlatma
repo = UserRepository()

st.set_page_config(
    page_title="Kütüphanem",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
apply_magic_theme()

st.title("❤️ Kütüphanem")

# -----------------------------
# 1. Kütüphane Filmleri Bölümü
# -----------------------------
movies = repo.get_all_movies()
# -----------------------------
# Film Listesini Aç / Kapat
# -----------------------------

if "show_movie_list" not in st.session_state:
    st.session_state.show_movie_list = False

button_text = (
    "🎬 Filmleri Gizle"
    if st.session_state.show_movie_list
    else "🎬 Filmleri Göster"
)

if st.button(button_text, use_container_width=True):

    st.session_state.show_movie_list = (
        not st.session_state.show_movie_list
    )

if st.session_state.show_movie_list:

    st.markdown(
        """
        <div style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:18px;
            padding:18px;
            margin-top:10px;
        ">
        """,
        unsafe_allow_html=True
    )

    for i, movie in enumerate(movies, start=1):

        st.markdown(
            f"**{i}.** 🎬 {movie[0]}"
        )

    st.markdown("</div>", unsafe_allow_html=True)

if not movies:
    st.info("Henüz kütüphanene film eklemedin.")
else:
    st.markdown("---")

    # Üst istatistikler
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎬 Toplam Film", len(movies))

    favorites = sum(1 for movie in movies if movie[5] == 1)

    with col2:
        st.metric("❤️ Favori", favorites)

    ratings = [
        movie[4]
        for movie in movies
        if movie[4] is not None and movie[4] > 0
    ]

    average = round(sum(ratings) / len(ratings), 2) if ratings else 0

    with col3:
        st.metric("⭐ Ortalama Puan", average)

    st.markdown("---")

    # Film kartları
    for movie in movies:
        title = movie[0]
        genre = movie[1]
        director = movie[2]
        imdb = movie[3]
        rating = movie[4] if movie[4] is not None else 0.0
        favorite = bool(movie[5])
        watch_date = movie[6]

        edit_key = f"edit_{title}"

        if edit_key not in st.session_state:
            st.session_state[edit_key] = False

        card_style = (
          "background:linear-gradient(135deg, rgba(255,0,120,0.08), rgba(255,255,255,0.03)); border:1px solid rgba(255,0,120,0.25); box-shadow:0 0 24px rgba(255,0,120,0.18); border-radius:22px; padding:18px; margin-bottom:14px;"
        if favorite else
           "background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:22px; padding:18px; margin-bottom:14px;"
)

        st.markdown(f'<div style="{card_style}">', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        poster_url = get_poster(title)

        col_img, col_info = st.columns([1, 3])

            # Poster sütunu
        with col_img:
                if poster_url:
                    st.image(poster_url, width=140)
                else:
                    st.markdown(
                        """
                        <div style="
                            width:140px;
                            height:210px;
                            border-radius:18px;
                            background:linear-gradient(135deg,#1B2A5B,#7C3AED);
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            text-align:center;
                            color:white;
                            font-weight:700;
                            font-size:16px;
                            box-shadow:0 0 14px rgba(124,58,237,0.35);
                        ">
                            🎬<br>Poster
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Bilgi sütunu
        with col_info:
                st.subheader(f"🎬 {title}")
                st.write(f"🎭 Tür: {genre if genre else '-'}")
                st.write(f"🎥 Yönetmen: {director if director else '-'}")
                st.write(f"⭐ IMDb: {imdb}  {star_rating(imdb)}")
            
                # 🎬 Fragman butonu
                trailer_query = urllib.parse.quote(f"{title} official trailer")
                trailer_url = f"https://www.youtube.com/results?search_query={trailer_query}"

                st.link_button(
                    "🎬 Fragmanı İzle",
                    trailer_url,
                    use_container_width=True
                )

                # Favori bilgisi
                if favorite:
                    st.success("❤️ Favori Film")

                # Favori butonu
                if st.button(
                    "💛 Favoriden Çıkar" if favorite else "🤍 Favorilere Ekle",
                    key=f"fav_btn_{title}"
                ):
                    repo.toggle_favorite(title)
                    st.rerun()

                st.markdown("---")

                # Düzenleme modu
                if st.session_state[edit_key]:
                    new_rating = st.slider(
                        "🌟 Senin Puanın",
                        min_value=0.0,
                        max_value=10.0,
                        value=float(rating),
                        step=0.5,
                        key=f"rating_{title}"
                    )

                    # Kayıtlı tarihi güvenli şekilde çöz
                    if watch_date not in [None, "", "-"]:
                        try:
                            saved_date = pd.to_datetime(watch_date).date()
                        except Exception:
                            saved_date = date.today()
                    else:
                        saved_date = date.today()

                    st.markdown("#### 📅 İzlenme Tarihi")

                    col_day, col_month, col_year = st.columns(3)

                    with col_day:
                        selected_day = st.selectbox(
                            "Gün",
                            list(range(1, 32)),
                            index=min(saved_date.day - 1, 30),
                            key=f"day_{title}"
                        )

                    months = [
                        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
                    ]

                    with col_month:
                        selected_month = st.selectbox(
                            "Ay",
                            months,
                            index=saved_date.month - 1,
                            key=f"month_{title}"
                        )

                    with col_year:
                        years = list(range(1950, datetime.now().year + 1))
                        saved_year_index = years.index(saved_date.year) if saved_date.year in years else len(years) - 1
                        selected_year = st.selectbox(
                            "Yıl",
                            years,
                            index=saved_year_index,
                            key=f"year_{title}"
                        )

                    month_number = months.index(selected_month) + 1

                    # Geçersiz gün-ay seçimlerini engellemek için try-except
                    try:
                        new_date = date(selected_year, month_number, selected_day)
                    except ValueError:
                        st.error("Geçersiz bir tarih seçtiniz (Örn: 31 Şubat). Lütfen günü düzeltin.")
                        new_date = None

                    month_name = months[month_number - 1]

                    st.caption(
                        f"📅 Seçilen tarih: {selected_day} {month_name} {selected_year}"
                    )

                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button("💾 Kaydet", key=f"save_{title}"):
                            if new_date:
                                repo.update_movie(
                                    title,
                                    new_rating,
                                    str(new_date)
                                )
                                st.session_state[edit_key] = False
                                st.success("Kaydedildi.")
                                st.rerun()

                    with c2:
                        if st.button("❌ İptal", key=f"cancel_{title}"):
                            st.session_state[edit_key] = False
                            st.rerun()

                else:
                    st.write(
                        f"🌟 Senin Puanın: {rating if rating > 0 else '-'}"
                    )

                    st.write(
                        f"📅 İzlenme Tarihi: {watch_date if watch_date else '-'}"
                    )

                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button(
                            "✏️ Düzenle",
                            key=f"edit_btn_{title}"
                        ):
                            st.session_state[edit_key] = True
                            st.rerun()

                    with c2:
                        if st.button(
                            "🗑 Sil",
                            key=f"delete_{title}"
                        ):
                            repo.delete_movie(title)
                            st.rerun()

# -----------------------------
# 2. Daha Sonra İzle Bölümü
# -----------------------------
st.markdown("---")
st.subheader("⏰ Daha Sonra İzle")

watchlist = repo.get_watchlist()

if watchlist:
   for idx, item in enumerate(watchlist):

    w_title = item[0]
    w_genre = item[1] if len(item) > 1 else None
    w_director = item[2] if len(item) > 2 else None
    w_imdb = item[3] if len(item) > 3 else None

    poster_url = get_poster(w_title)

    with st.container(border=True):

        col_img, col_info = st.columns([1, 3])

        with col_img:

            if poster_url:
                st.image(poster_url, width=120)

            else:
                st.markdown(
                    """
                    <div style="
                        width:120px;
                        height:180px;
                        border-radius:16px;
                        background:linear-gradient(135deg,#1B2A5B,#7C3AED);
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        text-align:center;
                        color:white;
                        font-weight:700;
                        font-size:15px;
                    ">
                        🎬<br>Poster
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_info:

            st.subheader(f"🎬 {w_title}")

            if w_genre:
                st.write(f"🎭 Tür: {w_genre}")

            if w_director:
                st.write(f"🎥 Yönetmen: {w_director}")

            if w_imdb:
                st.write(f"⭐ IMDb: {w_imdb}")

            trailer_query = urllib.parse.quote(
                f"{w_title} official trailer"
            )

            trailer_url = (
                f"https://www.youtube.com/results?search_query={trailer_query}"
            )

            st.link_button(
                "🎬 Fragmanı İzle",
                trailer_url,
                use_container_width=True
            )

            if st.button(
                "❌ Listeden Kaldır",
                key=f"remove_watch_{w_title}_{idx}",
                use_container_width=True
            ):

                repo.remove_from_watchlist(w_title)

                st.rerun()

            
else:
    st.info("Liste boş.")