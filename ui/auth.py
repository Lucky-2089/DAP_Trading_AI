import streamlit as st
import requests
from streamlit_lottie import st_lottie
from backend.database import db


def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def login_screen():
    lottie_anim = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_6aYlH9.json")

    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>

    <style>
    :root {
        --g900:#001f14; --g800:#003d2b; --g700:#006a4d; --g500:#00a372;
        --gold:#c9a84c; --bg:#f5f6f3; --ease:cubic-bezier(0.16,1,0.3,1);
    }
    *, *::before, *::after { box-sizing:border-box; }

    .stApp {
        background: var(--bg) !important;
        background-image:
            radial-gradient(ellipse 90% 55% at 50% -5%, rgba(0,106,77,0.22) 0%, transparent 65%),
            linear-gradient(180deg, #001a0f 0%, #003322 200px, var(--bg) 520px) !important;
        font-family:'DM Sans',sans-serif !important;
        overflow:hidden;
    }
    header[data-testid="stHeader"]{ background:transparent !important; height:0 !important; }
    .stMainBlockContainer{ padding-top:0 !important; }

    /* ── FLOATING ORBS ── */
    .orb {
        position:fixed; border-radius:50%; filter:blur(80px);
        pointer-events:none; z-index:0; animation:orbFloat linear infinite;
    }
    .orb1 { width:340px; height:340px; background:rgba(0,106,77,0.22); top:-80px; left:-80px; animation-duration:18s; }
    .orb2 { width:260px; height:260px; background:rgba(201,168,76,0.12); bottom:-60px; right:-60px; animation-duration:14s; animation-direction:reverse; }
    .orb3 { width:180px; height:180px; background:rgba(0,163,114,0.14); top:40%; left:60%; animation-duration:22s; animation-delay:-6s; }

    /* ── GRID OVERLAY ── */
    .grid-bg {
        position:fixed; inset:0; z-index:0; pointer-events:none; opacity:0.06;
        background-image:
            linear-gradient(rgba(0,163,114,.8) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,163,114,.8) 1px, transparent 1px);
        background-size: 48px 48px;
        animation: gridPan 30s linear infinite;
    }

    /* ── CARD ── */
    .auth-card {
        background:rgba(255,255,255,0.96);
        backdrop-filter:blur(20px);
        border-radius:16px;
        border-top:5px solid var(--gold);
        border-left:1px solid rgba(0,106,77,0.12);
        border-right:1px solid rgba(0,106,77,0.12);
        border-bottom:1px solid rgba(0,106,77,0.08);
        padding:2.4rem 2.6rem 2rem;
        box-shadow:0 24px 72px rgba(0,0,0,0.18), 0 4px 16px rgba(0,0,0,0.08);
        margin:0 auto; max-width:440px;
        animation: cardIn 0.7s var(--ease) both;
        position:relative; overflow:hidden; z-index:1;
        margin-bottom: 50px;
    }

    /* Card shimmer */
    .auth-card::before {
        content:''; position:absolute; top:0; left:-100%; width:50%; height:100%;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.6),transparent);
        animation:shimmerCard 3.5s 1s ease-in-out infinite;
    }

    /* ── WORDMARK ── */
    .wordmark { text-align:center; margin-bottom:1.4rem; }
    .wm-main {
        font-family:'Cormorant Garamond',serif; font-size:26px; font-weight:700;
        color:var(--g800); letter-spacing:-0.5px; line-height:1.1;
    }
    .wm-main span { color:var(--gold); }
    .wm-sub {
        font-size:10px; font-weight:600; letter-spacing:2.5px; text-transform:uppercase;
        color:#8a9e97; margin-top:5px;
    }

    /* Typewriter effect on subtitle */
    .wm-sub span {
        display:inline-block; overflow:hidden; white-space:nowrap;
        border-right:2px solid var(--g500);
        animation:typewriter 2s steps(38) 0.5s both, blink 0.8s step-end infinite 2.5s;
        width:0;
    }
    .card-rule {
        height:1px; margin:1rem 0 1.4rem;
        background:linear-gradient(90deg,transparent,rgba(0,106,77,0.2),transparent);
    }

    /* ── FORM BUTTON ── */
    [data-testid="stForm"] .stButton > button {
        background:linear-gradient(135deg,var(--g700),var(--g800)) !important;
        color:white !important; border:none !important; border-radius:9px !important;
        font-weight:600 !important; font-size:14px !important;
        letter-spacing:0.5px !important; padding:0.65rem !important;
        margin-top:0.4rem !important; transition:all 0.3s var(--ease) !important;
        width:100% !important; position:relative; overflow:hidden;
    }
    [data-testid="stForm"] .stButton > button:hover {
        transform:translateY(-2px) !important;
        box-shadow:0 8px 26px rgba(0,106,77,0.38) !important;
    }

    /* ── INPUTS ── */
    .stTextInput input {
        border:1px solid rgba(0,106,77,0.18) !important; border-radius:9px !important;
        font-family:'DM Sans',sans-serif !important; font-size:14px !important;
        transition:all 0.25s !important;
    }
    .stTextInput input:focus {
        border-color:var(--g500) !important;
        box-shadow:0 0 0 3px rgba(0,163,114,0.13) !important;
    }

    /* ── SECURITY BADGES ── */
    .badges {
        display:flex; justify-content:center; gap:8px; flex-wrap:wrap;
        margin:1.2rem 0 0;
        animation: fadeUp 0.5s 0.8s both;
    }
    .badge {
        background:#f0f7f4; border:1px solid rgba(0,106,77,0.18);
        border-radius:20px; padding:3px 11px; font-size:10px;
        font-weight:600; color:var(--g700); letter-spacing:0.5px;
        transition:all 0.25s;
    }
    .badge:hover { background:var(--g100); border-color:var(--g500); transform:translateY(-1px); }

    /* ── FOOTER ── */
    .auth-footer {
        text-align:center; color:#9aada6; font-size:11px;
        margin-top:1.8rem; line-height:1.6;
        animation: fadeUp 0.5s 0.9s both;
    }
    .auth-footer strong { color:#7a9a91; }

    /* ── TOP SECURE BAR ── */
    .secure-bar {
        background:var(--g900); color:var(--gold);
        text-align:center; padding:0.5rem;
        font-size:10px; letter-spacing:2px;
        font-weight:600; text-transform:uppercase;
        animation:slideDown 0.5s var(--ease) both;
        position:relative; overflow:hidden;
    }
    .secure-bar::after {
        content:''; position:absolute; top:0; left:-100%; width:50%; height:100%;
        background:linear-gradient(90deg,transparent,rgba(201,168,76,0.15),transparent);
        animation:shimmerBar 3s 1s ease-in-out infinite;
    }

    /* ── KEYFRAMES ── */
    @keyframes cardIn    { from{opacity:0;transform:translateY(28px) scale(0.97)} to{opacity:1;transform:translateY(0) scale(1)} }
    @keyframes fadeUp    { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
    @keyframes slideDown { from{opacity:0;transform:translateY(-100%)} to{opacity:1;transform:translateY(0)} }
    @keyframes orbFloat  { 0%{transform:translate(0,0) rotate(0deg)} 33%{transform:translate(30px,-20px) rotate(120deg)} 66%{transform:translate(-20px,20px) rotate(240deg)} 100%{transform:translate(0,0) rotate(360deg)} }
    @keyframes gridPan   { from{background-position:0 0} to{background-position:48px 48px} }
    @keyframes shimmerCard{ 0%{left:-100%} 60%{left:150%} 100%{left:150%} }
    @keyframes shimmerBar { 0%{left:-100%} 50%{left:120%} 100%{left:120%} }
    @keyframes typewriter { from{width:0} to{width:100%} }
    @keyframes blink      { 50%{border-color:transparent} }
    </style>

    <!-- Animated background elements -->
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>
    <div class="grid-bg"></div>
    """, unsafe_allow_html=True)

    # Secure top bar
    st.markdown("""
    <div class="secure-bar">
        🔒 &nbsp; Encrypted Institutional Access &nbsp;·&nbsp; FCA Regulated &nbsp;·&nbsp; ISO 27001
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.8, 1])

    with col:
        # Lottie animation above card
        if lottie_anim:
            st_lottie(lottie_anim, height=85, key="lock_anim")
        else:
            st.markdown(
                "<div class='animate__animated animate__bounceIn' "
                "style='text-align:center;font-size:40px;margin-bottom:0.5rem'>🏦</div>",
                unsafe_allow_html=True
            )
        st.markdown("""
        <div class="auth-card">
        <div class="wordmark">
            <div class="wm-main">DIGITAL ASSET <span>PORTAL</span></div>
            <div class="wm-sub"><span>Bank Technology Centre · Gateway</span></div>
        </div>
        <div class="card-rule"></div>
        """, unsafe_allow_html=True)

        with st.form("secure_gateway", clear_on_submit=False):
            username = st.text_input("User ID", placeholder="e.g. user1")
            password = st.text_input("Passphrase", type="password", placeholder="••••••••")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Secure Sign In →", use_container_width=True)

            if submit:
                if not username or not password:
                    st.warning("Please enter both User ID and passphrase.")
                else:
                    user = db.get_user(username)
                    if user and user.get("password") == password:
                        st.session_state.authenticated = True
                        st.session_state.user_id = username
                        st.rerun()
                    else:
                        st.error("Access Denied: Invalid credentials.")

        st.markdown("""
        <div class="badges">
            <span class="badge">256-bit TLS</span>
            <span class="badge">MFA Ready</span>
            <span class="badge">KYC Verified</span>
            <span class="badge">FCA Regulated</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="auth-footer">
            <strong>Institutional Access Only</strong><br>
            Unauthorised access is prohibited and monitored.<br>
            © 2026 Bank Banking Group · Archax DApp Project
        </div>
        """, unsafe_allow_html=True)