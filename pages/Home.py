import streamlit as st

st.set_page_config(
    page_title="CineMind Ana Sayfa",
    page_icon="🏠",
    layout="wide"
)

# Büyülü tema
st.markdown(
    """
    <style>

    .stApp {
        background: radial-gradient(circle at top, #1b1033 0%, #0a0a16 45%, #000000 100%);
        color: white;
    }

    .hero {
        text-align: center;
        padding: 5rem 2rem;
        border-radius: 30px;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 0 40px rgba(155, 92, 255, 0.35);
        margin-bottom: 2rem;
    }

    .hero h1 {
        font-size: 4rem;
        color: #f5f3ff;
        text-shadow: 0 0 20px #a855f7;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.2rem;
        color: #d8d4ff;
    }

    .feature {
        background: rgba(255,255,255,0.04);
        padding: 1.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 180px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .feature:hover {
        transform: translateY(-6px);
        box-shadow: 0 0 24px rgba(168,85,247,0.35);
    }

    .feature h3 {
        color: #f5f3ff;
    }

    .feature p {
        color: #d1d5db;
    }

    .quote {
        text-align: center;
        font-size: 1.1rem;
        font-style: italic;
        color: #c4b5fd;
        margin-top: 2rem;
    }

    .sparkles {
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.18;
        background-image:
            radial-gradient(circle, #ffffff 1px, transparent 1px),
            radial-gradient(circle, #c084fc 1px, transparent 1px),
            radial-gradient(circle, #ffffff 1px, transparent 1px);
        background-size: 120px 120px, 180px 180px, 260px 260px;
        animation: drift 30s linear infinite;
    }

    @keyframes drift {
        from { transform: translateY(0px); }
        to { transform: translateY(-120px); }
    }

    </style>

    <div class="sparkles"></div>

    <div class="hero">
        <h1>✨ CineMind ✨</h1>
        <p>
            Film dünyasının büyülü kapısı. Ruh halini keşfet, hikâyelerin içinde kaybol,
            sana özel önerilerle yeni favorilerini bul.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### 🌌 Bugün hangi dünyaya yolculuk etmek istersin?")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="feature">
            <h3>🎭 Ruh Hali Rehberi</h3>
            <p>Mutlu, duygusal, heyecanlı ya da gizemli... O anki ruh haline göre film keşfet.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="feature">
            <h3>🤖 Akıllı Öneriler</h3>
            <p>İzlediğin filmleri analiz ederek yönetmen, oyuncu ve konu benzerliklerinden yeni öneriler üretir.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="feature">
            <h3>📚 Kişisel Arşiv</h3>
            <p>Favorilerini kaydet, puan ver, izlenme tarihlerini tut ve kendi sinema evrenini oluştur.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.markdown("### 🔮 Bu gece için bir seçim")

b1, b2, b3 = st.columns(3)

with b1:
    st.button("🌙 Duygusal Bir Film", use_container_width=True)

with b2:
    st.button("🚀 Bilim Kurgu Macerası", use_container_width=True)

with b3:
    st.button("🕯️ Gizemli Bir Hikâye", use_container_width=True)

st.markdown(
    """
    <div class="quote">
        “Bazı filmler izlenmez, yaşanır.”
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown(
    """
    ### 🌠 CineMind Evrenine Hoş Geldin

    Burada amaç sadece film bulmak değil; seni etkileyecek hikâyeleri keşfetmek.
    Her öneri yeni bir karakter, yeni bir dünya ve yeni bir duygu demek.
    Işıkları azalt, kulaklığını tak ve büyünün başlamasına izin ver. ✨
    """
)