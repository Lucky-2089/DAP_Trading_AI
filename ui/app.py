import streamlit as st
import sys
import os

# --- PATH FIX ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import db
from auth import login_screen
from dashboard import show_dashboard
from wallet import show_wallet
from investment import show_investment

# 1. MUST BE FIRST
st.set_page_config(page_title="Institutional Digital Asset Portal", layout="wide")


def apply_custom_css():
    st.markdown("""
    <style>
        /* 1. Eliminate Streamlit Header & Top Padding Gap */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Targets the main container to remove top white space */
        .stMainBlockContainer {
            padding-top: 0rem !important;
            padding-bottom: 1rem !important;
            animation: fadeIn 0.8s ease-in;
        }

        /* 2. Global Application Background (Sandstone Professional) */
        .stApp {
            background-color: #f9f9f7 !important;
            background-image: linear-gradient(180deg, #e3e3de 0%, #f9f9f7 400px) !important;
            background-attachment: fixed;
        }

        /* 3. Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.4) !important;
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(0, 106, 77, 0.1);
        }

        /* 4. Main Header Styling (Institutional Lloyds Style) */
        .main-header {
            font-family: 'Times New Roman', serif;
            color: #006a4d; /* Using LBG Green for readability on Sandstone */
            font-weight: 700;
            padding-top: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #006a4d;
            margin-bottom: 2rem;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(5px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* 5. Customizing Sidebar Buttons */
        [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
            color: #006a4d !important;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)


# 2. Inject CSS
apply_custom_css()

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None

# Logic Flow
if not st.session_state.authenticated:
    login_screen()
else:
    # Main Header
    st.markdown('<h1 class="main-header">Institutional Digital Asset Portal</h1>', unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.markdown("### 🏦 **LBG Gateway**")
    st.sidebar.write(f"Active Session: `{st.session_state.user_id}`")
    st.sidebar.divider()

    menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "💳 My Wallets", "📈 AI Investment Portal"])

    st.sidebar.divider()
    if st.sidebar.button("🔒 Secure Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.rerun()

    user_data = db.get_user(st.session_state.user_id)

    if menu == "🏠 Dashboard":
        show_dashboard(user_data)
    elif menu == "💳 My Wallets":
        show_wallet(st.session_state.user_id, user_data)
    elif menu == "📈 AI Investment Portal":
        show_investment(user_data)