import streamlit as st
import requests
from streamlit_lottie import st_lottie
from backend.database import db


def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None


def login_screen():
    # Load professional security animation
    lottie_security = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_6aYlH9.json")

    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <style>
        /* 1. Page Background */
        .stApp {
background-color: #f4f4f4 !important;
background-image: linear-gradient(180deg, #004d40 0%, #f4f4f4 400px) !important;
        }

        /* 2. Centered Card with Reduced Padding */
        .auth-card {
            background: #ffffff !important;
            border-top: 6px solid #006a4d; /* Lloyds Green */
            border-radius: 4px;
            padding: 25px 35px; /* Reduced internal padding */
            width: 100%;
            max-width: 450px;
            margin: auto;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        /* 3. Header Styling */
        .header-box {
            text-align: center;
            margin-bottom: 15px;
        }

        .brand-header {
            font-family: 'Times New Roman', serif;
            font-size: 26px;
            font-weight: 700;
            color: #006a4d;
            margin: 0;
        }

        .portal-sub {
            color: #666;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 2px;
            margin-top: 5px;
            font-weight: 600;
        }

        /* 4. Animated Button Hover */
        div.stForm submit_button > button {
            background-color: #006a4d !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }

        div.stForm submit_button > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 106, 77, 0.3);
            background-color: #004a36 !important;
        }

        /* 5. Footer */
        .footer-note {
            text-align: center;
            color: #888;
            font-size: 11px;
            margin-top: 20px;
            line-height: 1.5;
        }
    </style>
    """, unsafe_allow_html=True)

    # UI Layout
    _, col, _ = st.columns([1, 2, 1])

    with col:
        # 1. Start the Animation Wrapper AND the Auth Card
        # We keep the <div> open so the white background wraps everything below it.
        st.markdown("""
            <div class="animate__animated animate__fadeInUp">
        """, unsafe_allow_html=True)

        # 2. Security Icon (Now strictly inside the white card)
        if lottie_security:
            st_lottie(lottie_security, height=70, key="security_icon")

        # 3. Header Box (Now strictly inside the white card)
        st.markdown("""
        <div class="auth-card">
            <div class="header-box">
                <div class="brand-header">DIGITAL ASSET PORTAL</div>
                <div class="portal-sub">Lloyds Technology Center Gateway</div>
            </div>
        """, unsafe_allow_html=True)

        # 4. The Form (Streamlit nests this inside the current open <div>)
        with st.form("secure_gateway", clear_on_submit=False):
            username = st.text_input("User ID", placeholder="e.g. user1")
            password = st.text_input("Password", type="password", placeholder="••••••••")

            submit = st.form_submit_button("Secure Sign In", use_container_width=True)

            if submit:
                user = db.get_user(username)
                if user and user["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_id = username
                    st.rerun()
                else:
                    st.error("Access Denied: Check credentials.")

        # 5. CLOSE the Auth Card and the Animation Wrapper
        # This </div></div> ensures the white background and animation end here.
        st.markdown('</div></div>', unsafe_allow_html=True)

        # 6. Footer (Sits outside on the grey background)
        st.markdown("""
            <div class="footer-note">
                <strong>Logon Security:</strong> Institutional Access Only.<br>
                © 2026 JPMORGAN CHASE & CO. | ARCHAX DAPP PROJECT
            </div>
        """, unsafe_allow_html=True)