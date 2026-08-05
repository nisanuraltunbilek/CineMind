
import streamlit as st
from utils.theme import apply_magic_theme

st.set_page_config(
    page_title="Ayarlar",
    page_icon="⚙️",
    layout="wide"
)
apply_magic_theme()

# Session state başlangıç değerleri
defaults = {
    "theme": "Koyu",
    "age_limit": "16+",
    "min_imdb": 7.0,
    "start_year": 2000,
    "notifications": True,
    "fav_genres": ["Drama", "Sci-Fi"]
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("⚙️ Ayarlar")
st.caption("CineMind deneyimini kendine göre özelleştir.")

st.markdown("---")

# -----------------------------
# Görünüm
# -----------------------------
st.subheader("🌙 Görünüm")

theme = st.radio(
    "Tema",
    ["Koyu", "Açık", "Sistem"],
    index=["Koyu", "Açık", "Sistem"].index(st.session_state.theme),
    horizontal=True
)

st.markdown("---")

# -----------------------------
# İçerik Filtreleri
# -----------------------------
st.subheader("🔞 İçerik Filtreleri")

age_limit = st.selectbox(
    "Maksimum yaş sınırı",
    ["Tümü", "7+", "13+", "16+", "18+"],
    index=["Tümü", "7+", "13+", "16+", "18+"].index(
        st.session_state.age_limit
    )
)

st.markdown("---")

# -----------------------------
# Favori Türler
# -----------------------------
st.subheader("🎭 Favori Türler")

all_genres = [
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

fav_genres = st.multiselect(
    "Sana daha sık önerilsin istediğin türler",
    all_genres,
    default=st.session_state.fav_genres
)

st.markdown("---")

# -----------------------------
# Öneri Tercihleri
# -----------------------------
st.subheader("⭐ Öneri Tercihleri")

min_imdb = st.slider(
    "Minimum IMDb puanı",
    5.0,
    10.0,
    float(st.session_state.min_imdb),
    0.1
)

start_year = st.slider(
    "Varsayılan başlangıç yılı",
    1950,
    2026,
    int(st.session_state.start_year)
)

st.markdown("---")

# -----------------------------
# Bildirimler
# -----------------------------
st.subheader("🔔 Bildirimler")

notifications = st.toggle(
    "Yeni öneriler ve günün filmi bildirimleri",
    value=st.session_state.notifications
)

st.markdown("---")

# -----------------------------
# Butonlar
# -----------------------------
col1, col2 = st.columns(2)

with col1:

   if st.button("💾 Ayarları Kaydet", use_container_width=True):

    st.session_state.theme = theme
    st.session_state.age_limit = age_limit
    st.session_state.fav_genres = fav_genres
    st.session_state.min_imdb = min_imdb
    st.session_state.start_year = start_year
    st.session_state.notifications = notifications

    # Tema dosyasını güncelle
    if theme == "Açık":

        config_text = """
[theme]
base="light"
primaryColor="#7C3AED"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F3F4F6"
textColor="#111827"
font="sans serif"
"""

    else:  # Koyu veya Sistem

        config_text = """
[theme]
base="dark"
primaryColor="#C084FC"
backgroundColor="#0B1026"
secondaryBackgroundColor="#1B2A5B"
textColor="#FFFFFF"
font="sans serif"
"""

    with open(".streamlit/config.toml", "w", encoding="utf-8") as f:
        f.write(config_text)

    st.success("Ayarlar kaydedildi! Tema değişikliği için uygulamayı yeniden başlat.") 

with col2:

    if st.button("🔄 Varsayılanlara Dön", use_container_width=True):

        for key, value in defaults.items():
            st.session_state[key] = value

        st.success("Varsayılan ayarlar geri yüklendi.")
        st.rerun()

st.markdown("---")

# -----------------------------
# Özet Kartı
# -----------------------------
st.subheader("📋 Geçerli Ayarlar")

st.info(
    f"""
🌙 **Tema:** {st.session_state.theme}

🔞 **Yaş sınırı:** {st.session_state.age_limit}

🎭 **Favori türler:** {', '.join(st.session_state.fav_genres)}

⭐ **Minimum IMDb:** {st.session_state.min_imdb}

📅 **Başlangıç yılı:** {st.session_state.start_year}

🔔 **Bildirimler:** {'Açık' if st.session_state.notifications else 'Kapalı'}
"""
)

