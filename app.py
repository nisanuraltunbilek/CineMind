
import random
import streamlit as st
import urllib.parse
from utils.poster_service import get_poster
from database.user_repository import UserRepository
from recommender.content_based import ContentBasedRecommender
from database.marathon_repository import MarathonRepository
from database.streak_repository import StreakRepository


streak_repo = StreakRepository()
streak = streak_repo.update_login()

marathon_repo = MarathonRepository()
st.set_page_config(
    page_title="CineMind",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# BÜYÜLÜ SİNEMATİK CSS
# -------------------------------------------------
st.markdown(
    """
<style>

/* Arka plan */
.stApp{
    background: radial-gradient(circle at top,#1B2A5B 0%,#111B47 35%,#0B1026 100%);
    overflow-x:hidden;
}

/* Hareketli yıldız katmanı */
.stApp::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        radial-gradient(2px 2px at 20px 30px,#ffffff,transparent),
        radial-gradient(1px 1px at 90px 120px,#ffffff,transparent),
        radial-gradient(2px 2px at 200px 80px,#ffffff,transparent),
        radial-gradient(1px 1px at 300px 200px,#ffffff,transparent),
        radial-gradient(2px 2px at 450px 150px,#ffffff,transparent),
        radial-gradient(1px 1px at 600px 90px,#ffffff,transparent),
        radial-gradient(2px 2px at 800px 250px,#ffffff,transparent);
    background-size:900px 400px;
    opacity:0.35;
    animation:starsMove 90s linear infinite;
    pointer-events:none;
    z-index:0;
}

@keyframes starsMove{
    from{transform:translateY(0);}
    to{transform:translateY(-400px);}
}

.block-container{
    position:relative;
    z-index:1;
    padding-top:1.5rem;
}

/* Başlık */
.hero{
    text-align:center;
    padding:20px 10px 10px 10px;
}

.hero h1{
    font-size:74px;
    margin:0;
    color:white;
    letter-spacing:2px;
    text-shadow:
        0 0 10px rgba(255,255,255,0.5),
        0 0 30px rgba(192,132,252,0.6),
        0 0 60px rgba(124,58,237,0.45);
}

.hero p{
    font-size:22px;
    color:#E9D5FF;
    margin-top:12px;
    text-shadow:0 0 12px rgba(192,132,252,0.5);
}

/* Kartlar */
.card{
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.14);
    border-radius:28px;
    min-height:220px;
    padding:28px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow:0 10px 30px rgba(0,0,0,0.28);
    transition:all .28s ease;
}

.card:hover{
    transform:translateY(-8px) scale(1.02);
    border-color:rgba(192,132,252,0.75);
    box-shadow:
        0 0 18px rgba(192,132,252,0.45),
        0 0 48px rgba(124,58,237,0.35),
        0 18px 40px rgba(0,0,0,0.35);
}

.card h2{
    color:white;
    font-size:34px;
    margin-bottom:10px;
}

.card p{
    color:#E5E7EB;
    font-size:16px;
    margin:0;
}

/* Butonlar */
div[data-testid="stButton"] button{
    width:100%;
    height:58px;
    border-radius:18px;
    border:none;
    font-size:18px;
    font-weight:700;
    color:white;
    background:linear-gradient(135deg,#7C3AED,#A855F7,#C084FC);
    box-shadow:0 6px 18px rgba(124,58,237,0.35);
    transition:all .22s ease;
}

div[data-testid="stButton"] button:hover{
    transform:translateY(-2px);
    box-shadow:
        0 0 18px rgba(192,132,252,0.6),
        0 10px 24px rgba(124,58,237,0.45);
}

/* Öneri bannerı */
.recommend-card{
    position:relative;
    overflow:hidden;
    background:linear-gradient(135deg,rgba(20,20,40,0.92),rgba(35,25,70,0.92));
    border:1px solid rgba(255,255,255,0.12);
    border-radius:30px;
    padding:36px;
    margin-top:10px;
    box-shadow:0 18px 50px rgba(0,0,0,0.45);
}

.recommend-card::after{
    content:"";
    position:absolute;
    top:-120px;
    right:-120px;
    width:280px;
    height:280px;
    border-radius:50%;
    background:radial-gradient(circle,rgba(192,132,252,0.28),transparent 70%);
    filter:blur(10px);
}

.recommend-title{
    color:#E9D5FF;
    font-size:18px;
    letter-spacing:1px;
    text-transform:uppercase;
}

.recommend-movie{
    color:white;
    font-size:44px;
    font-weight:800;
    margin:8px 0 12px 0;
    text-shadow:0 0 18px rgba(192,132,252,0.45);
}

.recommend-desc{
    color:#E5E7EB;
    font-size:18px;
    line-height:1.6;
    max-width:720px;
}

/* Bölüm başlığı */
.section-title{
    color:white;
    margin-top:24px;
    margin-bottom:10px;
    text-shadow:0 0 10px rgba(192,132,252,0.35);
}

.magic-box{
    background:rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:24px;
    padding:22px;
    text-align:center;
    margin-top:10px;
    color:white;
}

/* Film kartı hover efekti */
.movie-card{
    transition:all .28s ease;
}

.movie-card:hover{
    transform:translateY(-6px) scale(1.015);
    box-shadow:0 16px 40px rgba(124,58,237,0.35);
}

/* Dashboard kartı premium efekti */
.dashboard-card{
    border-radius:22px;
    padding:14px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 10px 24px rgba(0,0,0,0.22);
    transition:all .25s ease;
}

.dashboard-card:hover{
    border-color:rgba(168,85,247,0.55);
    box-shadow:
        0 0 18px rgba(168,85,247,0.28),
        0 0 44px rgba(124,58,237,0.22);
    transform:translateY(-3px);
}

/* Dashboard kartı premium efekti */
.dashboard-card{
    border-radius:22px;
    padding:14px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 10px 24px rgba(0,0,0,0.22);
    transition:all .25s ease;
}

.dashboard-card:hover{
    border-color:rgba(168,85,247,0.55);
    box-shadow:
        0 0 18px rgba(168,85,247,0.28),
        0 0 44px rgba(124,58,237,0.22);
    transform:translateY(-3px);
}

</style>
""",
    unsafe_allow_html=True
)

# 🔥 GİRİŞ SERİSİ
st.markdown(
    f"""
    <div style="
        background:rgba(255,255,255,0.06);
        border:1px solid rgba(255,255,255,0.12);
        border-radius:22px;
        padding:18px;
        text-align:center;
        color:white;
        margin-bottom:14px;
    ">
        <div style="font-size:16px;color:#C4B5FD;">🔥 Giriş Serin</div>
        <div style="font-size:44px;font-weight:800;margin-top:6px;">{streak} Gün</div>
        <div style="color:#E5E7EB;">
            Her gün giriş yap, serini koru ve rozet kazan!
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 🏅 ROZETLER
st.markdown("## 🏅 Rozetlerin")

repo = UserRepository()
movies = repo.get_all_movies()

badges = []

if streak >= 7:
    badges.append("🔥 Sinemasever")

if streak >= 30:
    badges.append("🌙 Gece Kuşu")

if len(movies) >= 10:
    badges.append("🎬 Koleksiyoncu")

if len(movies) >= 50:
    badges.append("🍿 Maratoncu")

if len(movies) >= 100:
    badges.append("🏆 Arşivci")

if badges:
    st.write(" • ".join(badges))
else:
    st.info("Henüz rozet kazanmadın 🎬")

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown(
    """
<div class="hero">
    <h1>🌙 CineMind</h1>
    <p>Sinema sadece izlenmez, hissedilir. Kendi evrenine hoş geldin ✨</p>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

# -------------------------------------------------
# ANA KARTLAR
# -------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown(
        """
        <div class="card">
            <h2>🔎 Film Ara</h2>
            <p>Binlerce film arasında kaybol, yeni dünyalar keşfet.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🔎 Film Ara", use_container_width=True):
        st.switch_page("pages/Search.py")

    st.markdown(
        """
        <div class="card">
            <h2>📚 Kütüphanem</h2>
            <p>İzlediğin filmleri, favorilerini ve anılarını sakla.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("📚 Kütüphanem", use_container_width=True):
        st.switch_page("pages/Library.py")

with col2:

    st.markdown(
        """
        <div class="card">
            <h2>🤖 AI Önerileri</h2>
            <p>Ruh haline ve zevkine göre kişisel öneriler al.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🤖 AI Önerileri", use_container_width=True):
        st.switch_page("pages/AI.py")

    st.markdown(
        """
        <div class="card">
            <h2>📊 Kontrol Paneli</h2>
            <p>Sinema alışkanlıklarını büyülü grafiklerle keşfet.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("📊 Kontrol Paneli", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# KİŞİSEL GÜNÜN ÖNERİSİ
# -------------------------------------------------
repo = UserRepository()
movies = repo.get_all_movies()

# 🔥 BURADAN SONRA YAPIŞTIR
st.markdown(
    f"""
    <div style="
        background:rgba(255,255,255,0.06);
        border:1px solid rgba(255,255,255,0.12);
        border-radius:22px;
        padding:18px;
        text-align:center;
        color:white;
        margin-bottom:14px;
    ">
        <div style="font-size:16px;color:#C4B5FD;">🔥 Giriş Serin</div>
        <div style="font-size:44px;font-weight:800;margin-top:6px;">{streak} Gün</div>
        <div style="color:#E5E7EB;">
            Her gün giriş yap, serini koru ve rozet kazan!
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 🏅 ROZETLER
st.markdown("## 🏅 Rozetlerin")

badges = []

if streak >= 7:
    badges.append("🔥 Sinemasever")

if streak >= 30:
    badges.append("🌙 Gece Kuşu")

if len(movies) >= 10:
    badges.append("🎬 Koleksiyoncu")

if len(movies) >= 50:
    badges.append("🍿 Maratoncu")

if len(movies) >= 100:
    badges.append("🏆 Arşivci")

if badges:
    st.write(" • ".join(badges))
else:
    st.info("Henüz rozet kazanmadın 🎬")

liked_movies = [
    movie[0]
    for movie in movies
    if movie[4] is not None and movie[4] >= 8
]

recommended_title = None

if liked_movies:

    try:

        recommender = ContentBasedRecommender()
        recommendations = recommender.recommend_for_user(liked_movies)

        if recommendations:

            first_rec = recommendations[0]

            if hasattr(first_rec, "get"):
                recommended_title = first_rec.get(
                    "Series_Title",
                    "Film Önerisi"
                )
            elif isinstance(first_rec, (tuple, list)):
                recommended_title = first_rec[0]
            else:
                recommended_title = str(first_rec)

    except Exception:
        recommended_title = None

if recommended_title:

    st.markdown(
        f"""
        <div class="recommend-card">
            <div class="recommend-title">🌟 Günün Sihirli Önerisi</div>
            <div class="recommend-movie">🎬 {recommended_title}</div>
            <div class="recommend-desc">
                Kütüphanendeki yüksek puanlı filmler, favori türlerin ve izleme alışkanlıkların analiz edildi.
                Bu film bu akşam seni en çok etkileyebilecek seçim olarak öne çıktı.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="recommend-card">
            <div class="recommend-title">🌟 Günün Sihirli Önerisi</div>
            <div class="recommend-movie">🎬 Interstellar</div>
            <div class="recommend-desc">
                Henüz yeterli puanlı filmin yok. Birkaç filme puan ver, sana tamamen kişisel öneriler hazırlayalım.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# -------------------------------------------------
# 🔮 RÜYA GİBİ SİNEMATİK KAPILAR
# -------------------------------------------------
st.markdown("### 🔮 Bu gece hangi dünyaya açılmak istersin?")

b1, b2, b3 = st.columns(3)

with b1:

    if st.button("🌙 Duygusal Bir Film", use_container_width=True):

        st.balloons()

        st.markdown(
            """
            <div style="
                background:rgba(255,255,255,0.08);
                border:1px solid rgba(255,255,255,0.12);
                border-radius:24px;
                padding:22px;
                text-align:center;
                color:white;
                box-shadow:0 0 25px rgba(192,132,252,0.45);
                margin-bottom:20px;
            ">
                <h2>💜 Kalbinin Kapısı Açıldı</h2>
                <p>Sessiz bir gece, hafif bir yağmur ve seni derinden etkileyecek bir hikâye seçildi… ✨</p>
                <p style="font-size:22px;font-weight:700;">🎬 Eternal Sunshine of the Spotless Mind</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("💫 Duygusal Dünyaya Geç", key="go_emotional"):
            st.switch_page("pages/AI.py")

with b2:

    if st.button("🚀 Bilim Kurgu Macerası", use_container_width=True):

        st.snow()

        st.markdown(
            """
            <div style="
                background:rgba(255,255,255,0.08);
                border:1px solid rgba(255,255,255,0.12);
                border-radius:24px;
                padding:22px;
                text-align:center;
                color:white;
                box-shadow:0 0 25px rgba(96,165,250,0.45);
                margin-bottom:20px;
            ">
                <h2>🌌 Yıldız Geçidi Aktif</h2>
                <p>Zaman bükülüyor, galaksiler açılıyor ve yeni bir macera seni çağırıyor… 🚀✨</p>
                <p style="font-size:22px;font-weight:700;">🎬 Interstellar</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🚀 Yıldızlara Yolculuk Et", key="go_scifi"):
            st.switch_page("pages/AI.py")

with b3:

    if st.button("🕯️ Gizemli Bir Hikâye", use_container_width=True):

        st.toast("✨ Gizem kapısı aralandı...")

        # Ekranın üstünde dağınık mor yıldızlar
        st.markdown(
            """
            <style>

            .magic-overlay{
                position:fixed;
                inset:0;
                pointer-events:none;
                z-index:99999;
                overflow:hidden;
            }

            .star{
                position:absolute;
                color:#E9D5FF;
                opacity:0;
                animation:floatUp 5s linear infinite;
                text-shadow:
                    0 0 10px rgba(192,132,252,0.95),
                    0 0 22px rgba(168,85,247,0.8);
            }

            /* bazıları büyük bazıları küçük */
            .s1,.s5,.s9{font-size:34px;}
            .s2,.s6,.s10{font-size:18px;}
            .s3,.s7,.s11{font-size:28px;}
            .s4,.s8,.s12{font-size:22px;}

            /* DAĞINIK KONUM */
            .s1{left:6%; top:82%; animation-delay:0s;}
            .s2{left:18%; top:68%; animation-delay:0.4s;}
            .s3{left:31%; top:88%; animation-delay:0.8s;}
            .s4{left:44%; top:74%; animation-delay:1.2s;}
            .s5{left:58%; top:86%; animation-delay:1.6s;}
            .s6{left:72%; top:64%; animation-delay:2s;}
            .s7{left:86%; top:80%; animation-delay:2.4s;}
            .s8{left:14%; top:56%; animation-delay:2.8s;}
            .s9{left:52%; top:50%; animation-delay:3.2s;}
            .s10{left:78%; top:58%; animation-delay:3.6s;}
            .s11{left:36%; top:44%; animation-delay:4s;}
            .s12{left:64%; top:38%; animation-delay:4.4s;}

            @keyframes floatUp{
                0%{
                    transform:translateY(0) scale(0.6) rotate(0deg);
                    opacity:0;
                }
                15%{opacity:1;}
                80%{opacity:1;}
                100%{
                    transform:translateY(-180px) scale(1.4) rotate(360deg);
                    opacity:0;
                }
            }

            </style>

            <div class="magic-overlay">
                <div class="star s1">✦✧</div>
                <div class="star s2">✧✧✧</div>
                <div class="star s3">✦✧</div>
                <div class="star s4">✧</div>
                <div class="star s5">✦✧</div>
                <div class="star s6">✧✧✧</div>
                <div class="star s7">✦✧</div>
                <div class="star s8">✧</div>
                <div class="star s9">✦✧</div>
                <div class="star s10">✧✧✧</div>
                <div class="star s11">✦✧</div>
                <div class="star s12">✧</div>
                <div class="star s13">✦✧</div>
                <div class="star s14>✧✧✧</div>
                <div class="star s15>✦✧</div>
                <div class="star s16">✧</div>
                <div class="star s17">✦✧</div>
                <div class="star s18">✧✧✧</div>
                <div class="star s19">✦✧</div>
                <div class="star s20">✧</div>
                <div class="star s21">✦✧</div>
                <div class="star s22">✧✧✧</div>
                <div class="star s23">✦✧</div>
                <div class="star s24">✧</div>
                <div class="star s25">✦✧</div>
                <div class="star s26">✧✧✧</div>
                <div class="star s27">✦✧</div>
                <div class="star s28">✧</div>
                <div class="star s29">✦✧</div>
                <div class="star s30">✧✧✧</div>
                <div class="star s31">✦✧</div>
                <div class="star s32>✧</div>
                <div class="star s33>✦✧</div>
                <div class="star s34">✧✧✧</div>
                <div class="star s35">✦✧</div>
                <div class="star s36">✧</div>
                <div class="star s37">✦✦</div>
                <div class="star s38">✦✦</div>
                <div class="star s39>✦✦</div>
                <div class="star s40>✦✦</div>
                <div class="star s41">✦✦✦</div>
                <div class="star s42">✦✦✦</div>
                <div class="star s43">✦✦✦</div>
                <div class="star s44">✦✦✦</div>

            </div>
            """,
            unsafe_allow_html=True
        )

    #BUTONUN DİBİNDE KART

# -------------------------------------------------
# SİHİRLİ BÖLÜM
# -------------------------------------------------

st.markdown(
    "<h2 class='section-title'>🪄 Bu Akşam Ne İzlesem?</h2>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .hero-banner{
        position:relative;
        overflow:hidden;
        border-radius:32px;
        min-height:380px;
        background:
            linear-gradient(90deg, rgba(5,8,20,0.92) 0%,
                                   rgba(5,8,20,0.78) 45%,
                                   rgba(5,8,20,0.25) 100%),
            url('https://image.tmdb.org/t/p/original/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg');
        background-size:cover;
        background-position:center;
        padding:42px;
        display:flex;
        align-items:flex-end;
        box-shadow:0 18px 60px rgba(0,0,0,0.45);
        border:1px solid rgba(255,255,255,0.10);
    }

    .hero-content{
        max-width:520px;
    }

    .hero-kicker{
        color:#C4B5FD;
        font-size:15px;
        letter-spacing:2px;
        text-transform:uppercase;
        margin-bottom:8px;
    }

    .hero-title{
        color:white;
        font-size:54px;
        font-weight:900;
        line-height:1.0;
        margin-bottom:14px;
        text-shadow:0 0 24px rgba(0,0,0,0.55);
    }

    .hero-desc{
        color:#E5E7EB;
        font-size:18px;
        line-height:1.6;
        text-shadow:0 0 12px rgba(0,0,0,0.45);
    }
    </style>

    <div class="hero-banner">
        <div class="hero-content">
            <div class="hero-kicker">CineMind Öneriyor</div>
            <div class="hero-title">Interstellar</div>
            <div class="hero-desc">
                İnsanlığın geleceği için yıldızların ötesine yapılan unutulmaz yolculuk.
                Bilim kurgu, duygu ve görsel şölenin mükemmel birleşimi.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

hero_col1, hero_col2 = st.columns(2)

with hero_col1:
    st.link_button(
        "🎬 Fragmanı İzle",
        "https://www.youtube.com/results?search_query=Interstellar+official+trailer",
        use_container_width=True
    )

with hero_col2:
    if st.button("📚 Kütüphaneme Git", use_container_width=True):
        st.switch_page("pages/Library.py")

st.markdown("<br>", unsafe_allow_html=True)
# -------------------------------------------------
# SON EKLENEN FİLM
# -------------------------------------------------

st.markdown(
    "<h2 class='section-title'>🆕 Son Eklediğin Film</h2>",
    unsafe_allow_html=True
)

if movies:

    latest_movie = movies[-1]

    latest_title = latest_movie[0]
    latest_genre = latest_movie[1]
    latest_director = latest_movie[2]
    latest_imdb = latest_movie[3]

    latest_poster = get_poster(latest_title)

    with st.container(border=True):

        c1, c2 = st.columns([1, 2])

        with c1:

            if latest_poster:
                st.image(latest_poster, width=180)

        with c2:

            st.markdown(f"# 🎬 {latest_title}")
            st.write(f"🎭 Tür: {latest_genre}")
            st.write(f"🎥 Yönetmen: {latest_director}")
            st.write(f"⭐ IMDb: {latest_imdb}")

            latest_query = urllib.parse.quote(
                f"{latest_title} official trailer"
            )

            latest_url = (
                f"https://www.youtube.com/results?search_query={latest_query}"
            )

            st.link_button(
                "🎬 Fragmanı İzle",
                latest_url,
                use_container_width=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

magic_pool = liked_movies if liked_movies else [m[0] for m in movies]

if st.button("✨ Bana Büyülü Bir Film Seç", use_container_width=True):

    if magic_pool:

        magic_pick = random.choice(magic_pool)

        st.markdown(
            f"""
            <div class="magic-box">
                <div style="font-size:22px;">🌌 Kozmik seçim yapıldı!</div>
                <div style="font-size:34px;font-weight:800;margin-top:8px;">🎥 {magic_pick}</div>
                <div style="margin-top:10px;color:#E9D5FF;">
                    Işıklar kapansın, patlamış mısır hazır olsun. Bu geceki filmin bu ✨
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("Önce kütüphanene birkaç film ekle 🎬")

         # -------------------------------------------------
# 🍿 MARATON MODU
# -------------------------------------------------

st.markdown(
    "<h2 class='section-title'>🍿 Bu Akşam İçin Maraton Modu</h2>",
    unsafe_allow_html=True
)

director_groups = {}

for movie in movies:

    director = movie[2]

    if director and director != "-":
        director_groups.setdefault(director, []).append(movie)

marathons = [
    (d, films)
    for d, films in director_groups.items()
    if len(films) >= 2
]

if marathons:

    director, films = random.choice(marathons)

    st.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,0.06);
            border:1px solid rgba(255,255,255,0.12);
            border-radius:24px;
            padding:22px;
            box-shadow:0 10px 30px rgba(0,0,0,0.25);
        ">
            <div style="font-size:14px;color:#C4B5FD;letter-spacing:1px;">
                🎬 Özel Seçim
            </div>
            <div style="font-size:34px;color:white;font-weight:800;margin:6px 0 14px 0;">
                {director} Gecesi
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    marathon_cols = st.columns(min(3, len(films)))

    for col, film in zip(marathon_cols, films[:3]):

        title = film[0]
        poster = get_poster(title)

        with col:

            if poster:
                st.image(poster, use_container_width=True)

            st.markdown(f"**🎬 {title}**")

            trailer_query = urllib.parse.quote(
                f"{title} official trailer"
            )

            trailer_url = (
                f"https://www.youtube.com/results?search_query={trailer_query}"
            )

            st.link_button(
                "🎬 Fragman",
                trailer_url,
                use_container_width=True
            )

else:

    st.info(
        "Maraton önerisi için aynı yönetmenden en az 2 film eklemelisin 🍿"
    )

         # -------------------------------------------------
# 🎲 KARARSIZIM RULETİ
# -------------------------------------------------

st.markdown(
    "<h2 class='section-title'>🎲 Kararsızım, Bana Film Seç</h2>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background:rgba(255,255,255,0.06);
        border:1px solid rgba(255,255,255,0.12);
        border-radius:24px;
        padding:18px;
        text-align:center;
        color:white;
    ">
        Film seçmekte zorlanıyorsan ruleti çevir 🎬✨
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("🎲 Ruleti Çevir", use_container_width=True):

    with st.spinner("🎞️ Filmler karıştırılıyor..."):

        import time

        placeholder = st.empty()

        roulette_pool = [m[0] for m in movies]

        for _ in range(18):

            fake_pick = random.choice(roulette_pool)

            placeholder.markdown(
                f"""
                <div style="
                    background:rgba(255,255,255,0.08);
                    border:1px solid rgba(255,255,255,0.14);
                    border-radius:22px;
                    padding:22px;
                    text-align:center;
                    color:white;
                    font-size:30px;
                    font-weight:800;
                ">
                    🎬 {fake_pick}
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.08)

        final_movie = random.choice(movies)

        final_title = final_movie[0]
        final_genre = final_movie[1]
        final_director = final_movie[2]
        final_imdb = final_movie[3]

        final_poster = get_poster(final_title)

        placeholder.empty()

        st.balloons()

        st.markdown(
            "<h3 style='text-align:center;color:white;'>🌟 Bu Akşamın Filmi Seçildi!</h3>",
            unsafe_allow_html=True
        )

        c1, c2 = st.columns([1, 2])

        with c1:

            if final_poster:
                st.image(final_poster, width=240)

        with c2:

            st.markdown(f"# 🎬 {final_title}")
            st.write(f"🎭 Tür: {final_genre}")
            st.write(f"🎥 Yönetmen: {final_director}")
            st.write(f"⭐ IMDb: {final_imdb}")

            final_query = urllib.parse.quote(
                f"{final_title} official trailer"
            )

            final_url = (
                f"https://www.youtube.com/results?search_query={final_query}"
            )

            st.link_button(
                "🎬 Fragmanı İzle",
                final_url,
                use_container_width=True
            )

        st.success(
            "🍿 Patlamış mısır hazırsa film hazır!"
        )

  # -------------------------------------------------
# 📅 MARATON TAKVİMİ
# -------------------------------------------------

        st.markdown("## 📅 Film Serisi Takvimi")

director_groups = {}

for movie in movies:
    director = movie[2]

    if director and director != "-":
        director_groups.setdefault(director, []).append(movie)

series_list = [
    (d, films)
    for d, films in director_groups.items()
    if len(films) >= 2
]

if series_list:

    director, films = max(series_list, key=lambda x: len(x[1]))
    film_titles = [f[0] for f in films]

    marathon = marathon_repo.get_marathon(director)

    if marathon:
         current_day = marathon["current_day"]
    else:
        current_day = None 
        
    days = len(films)

    with st.container(border=True):

        st.markdown(f"### 🎬 {director} Serisi")
        st.write(f"Bu seri için önerilen süre: **{days} gün**")

        st.markdown("---")

    for i, film in enumerate(films, start=1):

        title = film[0]

        if current_day and i < current_day:
           status = "✅ Tamamlandı"
        elif current_day == i:
          status = "🔥 Bugün"
        else:
           status = "⏳ Sıradaki"

        st.markdown(
           f"**📅 {i}. Gün — 🎬 {title} — {status}**"
    )

    st.markdown("---")

    st.success(
            f"🍿 {days} günlük {director} maratonun hazır!"
        )

else:

    st.info(
        "Film serisi oluşturmak için aynı yönetmenden en az 2 film eklemelisin 🎬"
    )

    st.markdown("---")

if not marathon:

    if st.button(
        "🚀 Maratonu Başlat",
        use_container_width=True
    ):

        marathon_repo.start_marathon(
            director,
            film_titles
        )

        st.success("Maraton başladı! 🍿")
        st.rerun()

else:

    progress = min(current_day - 1, days)

    st.progress(progress / days)

    st.write(f"**İlerleme:** {progress} / {days}")

    c1, c2 = st.columns(2)

    with c1:

        if current_day <= days:

            if st.button(
                "✅ Bugünkü Filmi Tamamladım",
                use_container_width=True
            ):

                marathon_repo.complete_today(director)

                st.success("Harika! Bir sonraki güne geçildi 🎬")
                st.rerun()

    with c2:

        if st.button(
            "🔄 Maratonu Sıfırla",
            use_container_width=True
        ):

            marathon_repo.reset_marathon(director)

            st.info("Maraton sıfırlandı.")
            st.rerun()

    if current_day > days:

        st.success(
            f"🏆 Tebrikler! {director} maratonunu tamamladın! 🍿✨"
        )