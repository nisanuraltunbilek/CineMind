from datetime import datetime
from utils.theme import apply_magic_theme
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from utils.poster_service import get_poster
from database.user_repository import UserRepository
from recommender.content_based import ContentBasedRecommender

# Repository başlatma
repo = UserRepository()

st.set_page_config(
    page_title="Kontrol Paneli",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
apply_magic_theme()

# Matplotlib varsayılan stil ayarları (Streamlit temalarına uyum için)
plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "text.color": "gray",
    "axes.labelcolor": "gray",
    "xtick.color": "gray",
    "ytick.color": "gray"
})

st.title("📊 CineMind Kontrol Paneli")

movies = repo.get_all_movies()

if not movies:
    st.info("Henüz kütüphanende film yok.")
    st.stop()

# En yüksek puanlı film
rated_movies = [m for m in movies if m[4] is not None and m[4] > 0]

if rated_movies:

    top_movie = max(rated_movies, key=lambda x: x[4])

    top_title = top_movie[0]
    top_rating = top_movie[4]

    poster = get_poster(top_title)

    st.markdown("## 🏆 En Yüksek Puan Verdiğin Film")
    st.markdown(
    """
    <style>
    .gold-card{
        border:2px solid #F59E0B;
        border-radius:26px;
        padding:18px;
        background:linear-gradient(135deg, rgba(245,158,11,0.10), rgba(255,255,255,0.03));
        box-shadow:0 0 28px rgba(245,158,11,0.28);
        margin-bottom:14px;
    }
    </style>
    <div class="gold-card">
    """,
    unsafe_allow_html=True
)

    c1, c2 = st.columns([1, 2])

    with c1:
        if poster:
            st.image(poster, width=220)

    with c2:
        st.markdown(f"# 🎬 {top_title}")
        st.markdown(f"### ⭐ {top_rating}/10")
        st.success("Bu film senin kütüphanendeki zirve seçimin!")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

# -----------------------------
# DataFrame Yapılandırması
# -----------------------------
df = pd.DataFrame(
    movies,
    columns=[
        "title",
        "genre",
        "director",
        "imdb",
        "rating",
        "favorite",
        "watch_date"
    ]
)

df["watch_date"] = pd.to_datetime(df["watch_date"], errors="coerce")
df["year_watched"] = df["watch_date"].dt.year

# Puanı girilmiş geçerli filmler için filtre
df["rating_valid"] = pd.to_numeric(df["rating"], errors="coerce")

# -----------------------------
# Yıl Seçici
# -----------------------------
current_year = datetime.now().year

available_years = sorted(
    [int(y) for y in df["year_watched"].dropna().unique()],
    reverse=True
)

if available_years:
    default_index = (
        available_years.index(current_year)
        if current_year in available_years
        else 0
    )

    selected_year = st.selectbox(
        "📅 Yıl Seç",
        available_years,
        index=default_index,
        key="year_selector"
    )

    year_df = df[df["year_watched"] == selected_year].copy()
else:
    selected_year = current_year
    year_df = df.copy()

st.markdown("---")

# -----------------------------
# Yıllık Özet
# -----------------------------
st.subheader(f"🎯 {selected_year} Özeti")

if not year_df.empty:
    total_movies = len(year_df)

    # Türleri ayrıştır ve temizle
    all_genres = []
    for g in year_df["genre"].dropna():
        all_genres.extend([x.strip() for x in str(g).split(",") if x.strip()])

    genre_series = pd.Series(all_genres)
    top_genre = genre_series.mode().iloc[0] if not genre_series.empty else "-"

    top_director = (
        year_df["director"].dropna().value_counts().idxmax()
        if not year_df["director"].dropna().empty
        else "-"
    )

    # 0'dan büyük puanların ortalamasını al (Puanlanmamış filmleri dahil etme)
    ratings_series = year_df[year_df["rating_valid"] > 0]["rating_valid"]
    avg_rating = round(ratings_series.mean(), 2) if not ratings_series.empty else 0

    st.success(
        f"""
📅 **{selected_year} yılında {total_movies} film izledin.**

🎭 En çok izlediğin tür: **{top_genre}**

🎥 En çok izlediğin yönetmen: **{top_director}**

⭐ Ortalama puanın: **{avg_rating}**
"""
    )
else:
    st.info("Bu yıl için izleme verisi yok.")

st.markdown("---")

# -----------------------------
# Üst Metrikler
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(f"🎬 {selected_year} İzlenen", len(year_df))

with col2:
    st.metric("❤️ Favori Film", int(year_df["favorite"].sum()))

with col3:
    ratings = year_df[year_df["rating_valid"] > 0]["rating_valid"]
    avg = round(ratings.mean(), 2) if not ratings.empty else 0
    st.metric("⭐ Ortalama Puan", avg)

st.markdown("---")

# =================================================
# KÜÇÜK VE ŞIK GRAFİK KARTLARI
# =================================================

left_col, right_col = st.columns(2, gap="large")

# -----------------------------
# İzlenme Grafiği
# -----------------------------
with left_col:

    with st.container(border=True):

        st.markdown(f"### 📅 {selected_year} İzlenme Grafiği")

        watch_df = year_df[year_df["watch_date"].notna()].copy()

        if not watch_df.empty:

            chart_df = (
                watch_df.groupby("watch_date")
                .size()
                .reset_index(name="count")
            )

            fig, ax = plt.subplots(figsize=(5, 2.6))

            ax.plot(
                chart_df["watch_date"],
                chart_df["count"],
                marker="o",
                color="#E50914",
                linewidth=2
            )

            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_title("")
            ax.grid(alpha=0.2)

            fig.tight_layout()

            st.pyplot(fig, clear_figure=True)

            plt.close(fig)

        else:

            st.info("Veri yok.")

# -----------------------------
# Tür Grafiği
# -----------------------------
with right_col:

    with st.container(border=True):

        st.markdown(f"### 🎭 {selected_year} Türler")

        genres_list = []

        for row in year_df["genre"].dropna():

            genres_list.extend([
                g.strip()
                for g in str(row).split(",")
                if g.strip()
            ])

        if genres_list:

            genre_counts = (
                pd.Series(genres_list)
                .value_counts()
                .head(5)
            )

            fig2, ax2 = plt.subplots(figsize=(3.4, 3.4))

            ax2.pie(
                genre_counts.values,
                labels=genre_counts.index,
                autopct="%1.0f%%",
                startangle=140,
                textprops={"fontsize": 8}
            )

            fig2.tight_layout()

            st.pyplot(fig2, clear_figure=True)

            plt.close(fig2)

        else:

            st.info("Veri yok.")

st.markdown("<br>", unsafe_allow_html=True)

left_col2, right_col2 = st.columns(2, gap="large")

# -----------------------------
# Yönetmen Grafiği
# -----------------------------
with left_col2:

    with st.container(border=True):

        st.markdown(f"### 🎥 {selected_year} Yönetmenler")

        director_counts = (
            year_df["director"]
            .dropna()
            .value_counts()
            .head(5)
        )

        if not director_counts.empty:

            fig3, ax3 = plt.subplots(figsize=(5, 2.6))

            ax3.barh(
                director_counts.index[::-1],
                director_counts.values[::-1],
                color="#7C3AED"
            )

            ax3.set_xlabel("")

            fig3.tight_layout()

            st.pyplot(fig3, clear_figure=True)

            plt.close(fig3)

        else:

            st.info("Veri yok.")

# -----------------------------
# Oyuncu Grafiği
# -----------------------------
with right_col2:

    with st.container(border=True):

        st.markdown(f"### 🎬 {selected_year} Oyuncular")

        try:

            titles_in_year = (
                year_df["title"]
                .dropna()
                .tolist()
            )

            if titles_in_year:

                placeholders = ",".join(["?"] * len(titles_in_year))

                query = (
                    f"SELECT actors FROM movies WHERE title IN ({placeholders})"
                )

                with repo.database.get_connection() as connection:

                    cursor = connection.cursor()

                    cursor.execute(query, titles_in_year)

                    rows = cursor.fetchall()

                actor_counts = {}

                for row in rows:

                    if row and row[0]:

                        actors = [
                            a.strip()
                            for a in str(row[0]).split(",")
                            if a.strip()
                        ]

                        for actor in actors:

                            actor_counts[actor] = (
                                actor_counts.get(actor, 0) + 1
                            )

                if actor_counts:

                    actor_series = (
                        pd.Series(actor_counts)
                        .sort_values(ascending=False)
                        .head(5)
                    )

                    fig4, ax4 = plt.subplots(figsize=(5, 2.6))

                    ax4.barh(
                        actor_series.index[::-1],
                        actor_series.values[::-1],
                        color="#2563EB"
                    )

                    ax4.set_xlabel("")

                    fig4.tight_layout()

                    st.pyplot(fig4, clear_figure=True)

                    plt.close(fig4)

                else:

                    st.info("Veri yok.")

            else:

                st.info("Veri yok.")

        except Exception as e:

            st.warning(f"Grafik yüklenemedi: {e}")

st.markdown("---")

# -----------------------------
# Son Eklenenler
# -----------------------------
st.subheader("🆕 Son Eklenen Filmler")

for title in df["title"].tail(5)[::-1]:
    st.write(f"• {title}")

# -----------------------------
# Beğendiğim Filmler
# -----------------------------
st.markdown("---")
st.subheader("✨ Beğendiğim Filmler")

liked_movies = st.session_state.get("liked_movies", [])

if liked_movies:
    for title in liked_movies:
        with st.container(border=True):
            st.markdown(f"### 🎬 {title}")
            c1, c2 = st.columns(2)

            with c1:
                if st.button(
                    "📚 Kütüphanede",
                    key=f"liked_lib_{title}"
                ):
                    st.success("Film zaten kütüphanende.")

            with c2:
                if st.button(
                    "⏰ Daha Sonra İzle",
                    key=f"liked_watch_{title}"
                ):
                    repo.add_to_watchlist(title)
                    st.success("İzleme listesine eklendi.")
else:
    st.info("Henüz Film Zevki Laboratuvarı'nda film beğenmedin.")