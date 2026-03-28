import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import db
from auth import login_screen
from dashboard import show_dashboard
from wallet import show_wallet
from investment import show_investment

st.set_page_config(
    page_title="LBG | Digital Asset Portal",
    layout="wide",
    page_icon="🏦",
    initial_sidebar_state="expanded"
)


def apply_global_css():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>

    <style>
    :root {
    --bg-secondary: #f5f6f3;    /* secondary surfaces */
    --card: #ffffff;

    --text: #1a1f1c;
    --muted: #5a6b64;

    /* ✅ FIXED: previously missing variables */
    --g900: #00291c;
    --g800: #003d2b;
    --g700: #006a4d;
    --g500: #00a372;
    --gold: #c9a84c;

    --bdr: rgba(0,106,77,0.12);

    --sh1: 0 2px 10px rgba(0,0,0,0.06);
    --sh2: 0 12px 40px rgba(0,0,0,0.13);

    --r: 12px;
    --ease: cubic-bezier(0.16,1,0.3,1);
    }

    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: var(--bg) !important;
        font-family: 'DM Sans', sans-serif !important;
        overflow-x: hidden;
    }

    header[data-testid="stHeader"] { background:transparent !important; height:0 !important; }
    .stMainBlockContainer { padding-top:0 !important; padding-bottom:3rem !important; max-width:1400px; }

    /* ── PARTICLE CANVAS ── */
    #ptc { position:fixed; top:0; left:0; width:100%; height:100%;
           pointer-events:none; z-index:0; opacity:0.3; }

    /* ── TOP BAR ── */
    .portal-topbar {
        background: linear-gradient(90deg, var(--g900) 0%, #003322 60%, var(--g900) 100%);
        color:white; padding:0.55rem 2rem;
        display:flex; align-items:center; justify-content:space-between;
        font-size:11px; letter-spacing:1.5px; text-transform:uppercase; font-weight:500;
        position:relative; overflow:hidden;
        animation: slideDown 0.6s var(--ease) both;
    }
    .portal-topbar::after {
        content:''; position:absolute; top:0; left:-120%; width:60%; height:100%;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.07),transparent);
        animation: shimmerBar 4s ease-in-out infinite;
    }
    .portal-topbar .brand { color:var(--gold); font-weight:700; }
    .live-dot {
        display:inline-block; width:7px; height:7px; background:#00e676;
        border-radius:50%; margin-right:5px;
        animation: pulseDot 1.8s ease-in-out infinite;
    }

    /* ── MAIN HEADER ── */
    .main-header {
        font-family:'Cormorant Garamond',serif;
        font-size:clamp(24px,3.5vw,42px); color:var(--g800);
        font-weight:700; padding:1.6rem 0 0.6rem;
        margin-bottom:2rem; letter-spacing:-0.8px;
        animation: fadeUp 0.7s 0.1s var(--ease) both;
        border-bottom:none; position:relative;
    }
    .main-header span { color:var(--g500); }
    .main-header::after {
        content:''; position:absolute; bottom:0; left:0; height:2px; width:0;
        background:linear-gradient(90deg,var(--g700),var(--gold));
        animation: lineGrow 0.9s 0.4s var(--ease) forwards;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background:linear-gradient(175deg,var(--g900) 0%,#00291c 100%) !important;
        border-right:1px solid rgba(0,163,114,0.15) !important;
        animation: sidebarIn 0.6s var(--ease) both;
    }
    [data-testid="stSidebar"] * { color:#dde8e4 !important; }

    .sb-logo {
        width:46px; height:46px;
        background:linear-gradient(135deg,var(--g700),var(--g500));
        border-radius:12px; display:flex; align-items:center; justify-content:center;
        font-size:22px; margin-bottom:0.4rem; position:relative;
        animation: fadeUp 0.5s 0.1s both;
    }
    .sb-logo::before {
        content:''; position:absolute; inset:-4px; border-radius:15px;
        border:1.5px solid var(--g500); opacity:0.4;
        animation: ringPulse 2.5s ease-in-out infinite;
    }

    .sb-brand {
        font-family:'Cormorant Garamond',serif; font-size:22px; font-weight:700;
        color:#fff !important; padding:0.2rem 0; letter-spacing:-0.3px;
        animation: fadeUp 0.5s 0.2s both;
    }
    .sb-brand span { color:var(--gold) !important; }

    .session-badge {
        background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);
        border-radius:8px; padding:0.55rem 0.9rem; font-size:12px;
        color:#b0c8be !important; margin:0.6rem 0;
        animation:fadeUp 0.5s 0.3s both;
        transition: background 0.3s, border-color 0.3s;
    }
    .session-badge:hover { background:rgba(0,163,114,0.1); border-color:var(--g500); }
    .session-badge strong { color:var(--gold) !important; }

    [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,0.08) !important; margin:0.8rem 0 !important; }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background:rgba(255,255,255,0.04) !important;
        border:1px solid rgba(255,255,255,0.07) !important;
        border-radius:9px !important; padding:0.55rem 0.9rem !important;
        margin-bottom:5px !important; font-weight:500 !important; font-size:14px !important;
        transition: all 0.3s var(--ease) !important;
        animation: fadeUp 0.4s both;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:nth-child(1){animation-delay:0.35s}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:nth-child(2){animation-delay:0.42s}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:nth-child(3){animation-delay:0.49s}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background:rgba(0,163,114,0.18) !important;
        border-color:var(--g500) !important;
        transform:translateX(5px) !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background:rgba(201,168,76,0.12) !important;
        border:1px solid var(--gold) !important; color:var(--gold) !important;
        font-weight:600 !important; border-radius:9px !important; font-size:13px !important;
        transition:all 0.3s var(--ease) !important;
        animation:fadeUp 0.5s 0.55s both;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background:var(--gold) !important; color:var(--g900) !important;
        transform:translateY(-2px) !important;
        box-shadow:0 6px 20px rgba(201,168,76,0.3) !important;
    }

    /* ── METRIC CARDS ── */
    [data-testid="stMetric"] {
        background:var(--card); border:1px solid var(--bdr); border-radius:var(--r);
        padding:1.2rem 1.4rem !important; box-shadow:var(--sh1);
        transition:all 0.35s var(--ease); animation:fadeUp 0.5s both;
        position:relative; overflow:hidden;
    }
    [data-testid="stMetric"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:3px;
        background:linear-gradient(90deg,var(--g700),var(--g500));
        transform:scaleX(0); transform-origin:left;
        transition:transform 0.4s var(--ease);
    }
    [data-testid="stMetric"]:hover {
        box-shadow:var(--sh2); transform:translateY(-4px); border-color:var(--g500);
    }
    [data-testid="stMetric"]:hover::before { transform:scaleX(1); }
    [data-testid="stMetricLabel"] {
        font-size:10px !important; letter-spacing:1.5px; text-transform:uppercase;
        color:var(--muted) !important; font-weight:600 !important;
    }
    [data-testid="stMetricValue"] {
        font-family:'Cormorant Garamond',serif !important;
        font-size:28px !important; color:var(--g800) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background:linear-gradient(135deg,var(--g700),var(--g800)) !important;
        color:white !important; border:none !important; border-radius:9px !important;
        font-weight:600 !important; font-size:14px !important;
        padding:0.6rem 1.4rem !important; transition:all 0.3s var(--ease) !important;
        position:relative; overflow:hidden;
    }
    .stButton > button:hover {
        transform:translateY(-2px) !important;
        box-shadow:0 8px 24px rgba(0,106,77,0.35) !important;
    }
    .stButton > button:active { transform:translateY(0) !important; }

    /* ── INPUTS ── */
    .stTextInput input, .stNumberInput input {
        border:1px solid var(--bdr) !important; border-radius:9px !important;
        background:white !important; font-family:'DM Sans',sans-serif !important;
        transition:all 0.25s !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color:var(--g500) !important;
        box-shadow:0 0 0 3px rgba(0,163,114,0.14) !important;
    }

    /* ── DATAFRAME ── */
    [data-testid="stDataFrame"] {
        border:1px solid var(--bdr) !important; border-radius:var(--r) !important;
        overflow:hidden !important; animation:fadeUp 0.6s 0.2s both;
    }

    h2,h3 { font-family:'Cormorant Garamond',serif !important; color:var(--g800) !important; font-weight:700 !important; }

    hr { border:none !important; height:1px !important;
         background:linear-gradient(90deg,transparent,var(--bdr),transparent) !important;
         margin:1.8rem 0 !important; }

    /* ── KEYFRAMES ── */
    @keyframes fadeUp   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
    @keyframes slideDown{ from{opacity:0;transform:translateY(-100%)} to{opacity:1;transform:translateY(0)} }
    @keyframes sidebarIn{ from{opacity:0;transform:translateX(-30px)} to{opacity:1;transform:translateX(0)} }
    @keyframes lineGrow { to{width:100%} }
    @keyframes shimmerBar{ 0%{left:-120%} 50%{left:120%} 100%{left:120%} }
    @keyframes pulseDot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.7)} }
    @keyframes ringPulse{ 0%,100%{transform:scale(1);opacity:0.4} 50%{transform:scale(1.12);opacity:0.15} }

    @media(max-width:768px){
        .portal-topbar{font-size:9px;padding:0.5rem 1rem;}
        .main-header{font-size:20px;padding-top:1rem;}
    }
    </style>

    <canvas id="ptc"></canvas>
    <script>
    (function(){
        const c=document.getElementById('ptc');
        if(!c)return;
        const x=c.getContext('2d');
        let W,H,P=[];
        function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
        resize(); window.addEventListener('resize',resize);
        class Dot{
            constructor(){this.reset();}
            reset(){
                this.x=Math.random()*W; this.y=Math.random()*H;
                this.r=Math.random()*1.6+0.4;
                this.vx=(Math.random()-.5)*.28; this.vy=(Math.random()-.5)*.28;
                this.a=Math.random()*.45+.1;
                this.col=Math.random()>.65?'#c9a84c':'#006a4d';
            }
            update(){this.x+=this.vx;this.y+=this.vy;
                if(this.x<0||this.x>W||this.y<0||this.y>H)this.reset();}
            draw(){x.beginPath();x.arc(this.x,this.y,this.r,0,Math.PI*2);
                x.fillStyle=this.col;x.globalAlpha=this.a;x.fill();}
        }
        for(let i=0;i<90;i++)P.push(new Dot());
        function lines(){
            for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++){
                const dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);
                if(d<110){x.beginPath();x.moveTo(P[i].x,P[i].y);x.lineTo(P[j].x,P[j].y);
                    x.strokeStyle='#006a4d';x.globalAlpha=(1-d/110)*.07;x.lineWidth=.5;x.stroke();}
            }
        }
        function loop(){x.clearRect(0,0,W,H);P.forEach(p=>{p.update();p.draw();});lines();requestAnimationFrame(loop);}
        loop();
    })();
    </script>
    """, unsafe_allow_html=True)


apply_global_css()

st.markdown("""
<div class="portal-topbar">
    <span><span class="brand">LBG</span> &nbsp;·&nbsp; Institutional Digital Asset Portal</span>
    <span><span class="live-dot"></span>Live &nbsp;·&nbsp; FCA Regulated &nbsp;·&nbsp; ISO 27001 &nbsp;·&nbsp; 256-bit TLS</span>
</div>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None

if not st.session_state.authenticated:
    login_screen()
else:
    st.markdown('<h1 class="main-header">Institutional Digital Asset <span>Portal</span></h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="sb-logo">🏦</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-brand">LBG <span>Gateway</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="session-badge">
            <div style="font-size:10px;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px;opacity:.7">Active Session</div>
            <strong>{st.session_state.user_id}</strong>
        </div>""", unsafe_allow_html=True)
        st.divider()

        menu = st.radio("Navigation", ["🏠  Dashboard", "💳  My Wallets", "📈  AI Investment Portal"], label_visibility="collapsed")
        st.divider()

        if st.button("🔒  Secure Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.rerun()

    user_data = db.get_user(st.session_state.user_id)

    if   menu == "🏠  Dashboard":              show_dashboard(user_data)
    elif menu == "💳  My Wallets":             show_wallet(st.session_state.user_id, user_data)
    elif menu == "📈  AI Investment Portal":   show_investment(user_data)