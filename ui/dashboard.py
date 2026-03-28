import streamlit as st
import pandas as pd
import plotly.express as px
from backend.api_mock import ArchaxPublicClient


def _anim_css():
    st.markdown("""
    <style>
    /* Staggered card entrance */
    .kpi-wrap > div:nth-child(1) [data-testid="stMetric"] { animation-delay:0.05s }
    .kpi-wrap > div:nth-child(2) [data-testid="stMetric"] { animation-delay:0.12s }
    .kpi-wrap > div:nth-child(3) [data-testid="stMetric"] { animation-delay:0.19s }
    .kpi-wrap > div:nth-child(4) [data-testid="stMetric"] { animation-delay:0.26s }

    /* Section title animated underline */
    .sect-title {
        font-family:'Cormorant Garamond',serif;
        font-size:20px; font-weight:700; color:#003d2b;
        margin-bottom:0.4rem; position:relative; display:inline-block;
        animation:fadeUp 0.5s 0.2s both;
    }
    .sect-title::after {
        content:''; position:absolute; bottom:-3px; left:0; height:2px; width:0;
        background:linear-gradient(90deg,#006a4d,#c9a84c);
        animation:lineGrow 0.7s 0.5s cubic-bezier(0.16,1,0.3,1) forwards;
    }

    /* Page title */
    .dash-welcome {
        animation:fadeUp 0.6s 0s cubic-bezier(0.16,1,0.3,1) both;
    }

    /* Live pill bounce-in */
    .live-pill {
        display:inline-block; background:#d6f0e8; color:#006a4d;
        font-size:10px; font-weight:700; letter-spacing:1px; padding:3px 10px;
        border-radius:20px; text-transform:uppercase; margin-left:10px;
        animation:bouncePill 0.6s 0.5s cubic-bezier(0.16,1,0.3,1) both;
        vertical-align:middle;
    }

    /* Chart card */
    .chart-card {
        background:white; border:1px solid rgba(0,106,77,0.1); border-radius:12px;
        padding:1.2rem 1.4rem; box-shadow:0 2px 10px rgba(0,0,0,0.05);
        animation:fadeUp 0.6s 0.3s both;
        transition:box-shadow 0.3s, transform 0.3s;
    }
    .chart-card:hover { box-shadow:0 10px 36px rgba(0,0,0,0.10); transform:translateY(-2px); }

    /* Allocation + ledger fade */
    .lower-left  { animation:fadeUp 0.5s 0.35s both; }
    .lower-right { animation:fadeUp 0.5s 0.45s both; }

    @keyframes fadeUp    { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
    @keyframes lineGrow  { to{width:100%} }
    @keyframes bouncePill{ from{opacity:0;transform:scale(0.5)} to{opacity:1;transform:scale(1)} }
    </style>
    """, unsafe_allow_html=True)


def show_dashboard(user_data):
    _anim_css()
    client = ArchaxPublicClient()
    wallets = user_data.get('wallets', {})
    total_aum = sum(wallets.values())
    risk = user_data.get('risk_profile', 'low').upper()

    # ── WELCOME ──
    st.markdown(f"""
    <div class="dash-welcome" style="margin-bottom:1.8rem">
        <div style="font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;
                    color:#00a372;margin-bottom:4px">Welcome back</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:700;
                    color:#003d2b;letter-spacing:-0.5px">{user_data['name']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI METRICS ──
    st.markdown('<div class="kpi-wrap">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Compliance Status", "KYC Approved",         delta="✓ Verified")
    c2.metric("Total AUM",         f"£{total_aum:,.2f}",   delta="+0.00% today")
    c3.metric("AI Risk Profile",   risk,                    delta="Active")
    c4.metric("Active Wallets",    len(wallets),            delta=f"{len(wallets)} currencies")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # ── MARKET CHART ──
    st.markdown("""
    <div style="margin:1.4rem 0 0.8rem;display:flex;align-items:center;gap:4px">
        <span class="sect-title">📊 Market Intelligence</span>
        <span class="live-pill">Live Feed</span>
    </div>
    <p style="color:#5a6b64;font-size:13px;margin-bottom:0.6rem;animation:fadeUp 0.5s 0.25s both">
        30-Day UK Gilt Yield Trend
    </p>
    """, unsafe_allow_html=True)

    perf_data = client.get_gilt_performance_data()

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_line = px.line(perf_data, x="Date", y="Yield (%)", template="plotly_white",
                       color_discrete_sequence=["#006a4d"])
    fig_line.update_traces(line=dict(width=2.5),
                           fill='tozeroy', fillcolor='rgba(0,106,77,0.05)')
    fig_line.update_layout(
        margin=dict(t=10, b=10, l=0, r=0),
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#8a9e97")),
        yaxis=dict(gridcolor="#f0f5f3", tickfont=dict(size=11, color="#8a9e97")),
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── LOWER ROW ──
    col_left, _, col_right = st.columns([1, 0.05, 1])

    with col_left:
        st.markdown('<div class="lower-left">', unsafe_allow_html=True)
        st.markdown('<div class="sect-title" style="margin-bottom:0.8rem">💰 Asset Allocation</div>', unsafe_allow_html=True)
        if wallets:
            df_w = pd.DataFrame(list(wallets.items()), columns=['Currency', 'Balance'])
            fig_pie = px.pie(df_w, values='Balance', names='Currency', hole=0.5,
                             color_discrete_sequence=['#006a4d', '#00a372', '#c9a84c', '#81c784', '#003d2b'])
            fig_pie.update_traces(textfont=dict(size=12),
                                  hovertemplate="<b>%{label}</b><br>£%{value:,.2f}<extra></extra>")
            fig_pie.update_layout(margin=dict(t=20, b=20, l=10, r=10),
                                  paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No wallet data to display.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="lower-right">', unsafe_allow_html=True)
        st.markdown('<div class="sect-title" style="margin-bottom:0.8rem">📝 Settlement Ledger</div>', unsafe_allow_html=True)
        transactions = user_data.get('transactions', [])
        if transactions:
            df_tx = pd.DataFrame(transactions)
            st.dataframe(df_tx, column_config={
                "timestamp":   st.column_config.TextColumn("Date & Time"),
                "description": st.column_config.TextColumn("Activity"),
                "amount":      st.column_config.NumberColumn("Amount", format="£%.2f"),
                "currency":    st.column_config.TextColumn("CCY"),
                "status":      st.column_config.TextColumn("Status"),
            }, hide_index=True, use_container_width=True, height=280)
        else:
            st.info("No recent transactions. Make a deposit or investment to get started.")
        st.markdown('</div>', unsafe_allow_html=True)