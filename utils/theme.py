
import streamlit as st

def apply_magic_theme():

    st.markdown(
        """
        <style>

        .stApp {
            background: radial-gradient(circle at top, #1b1033 0%, #0a0a16 45%, #000000 100%);
            color: white;
        }

        h1,h2,h3,h4,p,label,span {
            color: white !important;
        }

        div[data-testid="stButton"] button{
            width:100%;
            height:52px;
            border-radius:16px;
            border:none;
            font-size:16px;
            font-weight:700;
            color:white;
            background:linear-gradient(135deg,#7C3AED,#A855F7,#C084FC);
            box-shadow:0 6px 16px rgba(124,58,237,0.35);
            transition:all .2s ease;
        }

        div[data-testid="stButton"] button:hover{
            transform:translateY(-2px);
            box-shadow:0 0 18px rgba(192,132,252,0.55);
        }

        div[data-testid="stMetric"]{
            background:rgba(255,255,255,0.06);
            border:1px solid rgba(255,255,255,0.10);
            padding:18px;
            border-radius:20px;
            backdrop-filter: blur(10px);
        }

        .magic-card{
            background: rgba(255,255,255,0.04);
            padding: 1.5rem;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar'ı otomatik kapat
st.markdown(
    """
    <script>
    const closeSidebar = () => {
        const btn = window.parent.document.querySelector(
            '[data-testid="collapsedControl"]'
        );

        if (btn) {
            btn.click();
        }
    };

    setTimeout(closeSidebar, 300);
    </script>
    """,
    unsafe_allow_html=True
)

