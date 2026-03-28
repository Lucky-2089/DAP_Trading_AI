import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from backend.api_mock import ArchaxPublicClient
from backend.ai_engine import RecommenderAPI


def _anim_css():
    st.markdown("""
    <style>
    .inv-header  { animation:fadeUp 0.5s 0s   cubic-bezier(0.16,1,0.3,1) both }
    .ctx-banner  { animation:fadeUp 0.5s 0.1s cubic-bezier(0.16,1,0.3,1) both }
    .chart-left  { animation:fadeUp 0.5s 0.2s cubic-bezier(0.16,1,0.3,1) both }
    .chart-right { animation:fadeUp 0.5s 0.28s cubic-bezier(0.16,1,0.3,1) both }
    .top-pick    { animation:fadeUp 0.5s 0.32s cubic-bezier(0.16,1,0.3,1) both }
    .stress-sec  { animation:fadeUp 0.5s 0.4s cubic-bezier(0.16,1,0.3,1) both }

    /* Context banner */
    .ctx-banner-inner {
        background:linear-gradient(135deg,#001f14,#006a4d);
        border-radius:12px; padding:1rem 1.4rem;
        margin:0.8rem 0 1.4rem;
        display:flex; align-items:center; justify-content:space-between;
        flex-wrap:wrap; gap:8px;
        box-shadow:0 6px 24px rgba(0,106,77,0.25);
        position:relative; overflow:hidden;
    }
    .ctx-banner-inner::before {
        content:''; position:absolute; top:0; left:-80%; width:50%; height:100%;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);
        animation:shimmer 3s 1s ease-in-out infinite;
    }
    .ctx-fund-count {
        background:rgba(201,168,76,0.18); border:1px solid #c9a84c;
        border-radius:6px; padding:4px 14px; color:#c9a84c;
        font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase;
        animation:bouncePill 0.5s 0.4s cubic-bezier(0.16,1,0.3,1) both;
    }

    /* Chart cards */
    .chart-card {
        background:white; border:1px solid rgba(0,106,77,0.1); border-radius:12px;
        padding:1rem 1.2rem; box-shadow:0 2px 10px rgba(0,0,0,0.05);
        transition:all 0.35s cubic-bezier(0.16,1,0.3,1);
    }
    .chart-card:hover { box-shadow:0 12px 36px rgba(0,0,0,0.10); transform:translateY(-3px); }

    /* Section title */
    .sect-title {
        font-family:'Cormorant Garamond',serif; font-size:18px; font-weight:700;
        color:#003d2b; margin-bottom:0.5rem; position:relative; display:inline-block;
    }
    .sect-title::after {
        content:''; position:absolute; bottom:-3px; left:0; height:2px; width:0;
        background:linear-gradient(90deg,#006a4d,#c9a84c);
        animation:lineGrow 0.7s 0.4s cubic-bezier(0.16,1,0.3,1) forwards;
    }

    /* Top pick banner */
    .top-pick-banner {
        background:linear-gradient(135deg,#f0faf6,#e4f5ee);
        border:1px solid #00a372; border-left:5px solid #006a4d;
        border-radius:12px; padding:1rem 1.4rem; margin-bottom:1.2rem;
        transition:all 0.3s; cursor:default;
    }
    .top-pick-banner:hover { box-shadow:0 8px 28px rgba(0,106,77,0.15); transform:translateY(-1px); }

    /* Stat pills */
    .stat-pill {
        display:flex; justify-content:space-between; align-items:center;
        padding:0.55rem 0.85rem; background:#f7f8f6; border-radius:9px;
        border:1px solid rgba(0,106,77,0.09); margin-bottom:7px;
        transition:all 0.25s cubic-bezier(0.16,1,0.3,1);
    }
    .stat-pill:hover { background:#edf6f2; border-color:rgba(0,106,77,0.28); transform:translateX(4px); }
    .pill-label { font-size:11px; font-weight:600; color:#5a6b64; text-transform:uppercase; letter-spacing:0.8px; }
    .pill-value { font-size:14px; font-weight:700; color:#003d2b; }

    /* AI reasoning box */
    .ai-reason {
        background:#f0faf6; border-radius:9px; padding:0.85rem 1rem;
        margin:0.8rem 0; font-size:13px; color:#3a5a50;
        border:1px solid rgba(0,106,77,0.12);
        animation:fadeUp 0.5s 0.5s both;
    }

    /* Gauge glow pulse */
    .gauge-wrap {
        animation:fadeUp 0.5s 0.45s both;
        position:relative;
    }
    .gauge-wrap::after {
        content:''; position:absolute; bottom:0; left:20%; right:20%; height:20px;
        background:rgba(0,106,77,0.12); filter:blur(12px); border-radius:50%;
        animation:glowPulse 2.5s ease-in-out infinite;
    }

    /* Stress test */
    .stress-empty {
        background:#f7f8f6; border:1.5px dashed rgba(0,106,77,0.2);
        border-radius:12px; padding:1.8rem; text-align:center;
        color:#8a9e97; font-size:14px;
    }

    /* KEYFRAMES */
    @keyframes fadeUp    { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
    @keyframes lineGrow  { to{width:100%} }
    @keyframes shimmer   { 0%{left:-80%} 50%{left:130%} 100%{left:130%} }
    @keyframes bouncePill{ from{opacity:0;transform:scale(0.6)} to{opacity:1;transform:scale(1)} }
    @keyframes glowPulse { 0%,100%{opacity:0.6;transform:scaleX(1)} 50%{opacity:1;transform:scaleX(1.15)} }
    </style>
    """, unsafe_allow_html=True)


def show_investment(user_data):
    _anim_css()

    # ── PAGE HEADER ──
    st.markdown("""
    <div class="inv-header" style="margin-bottom:1.8rem">
        <div style="font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;
                    color:#00a372;margin-bottom:4px">Powered by Machine Learning</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:700;
                    color:#003d2b;letter-spacing:-0.5px">AI Institutional Advisor</div>
    </div>
    """, unsafe_allow_html=True)

    client = ArchaxPublicClient()
    engine = RecommenderAPI()

    wallets = user_data.get('wallets', {})
    if not wallets:
        st.warning("Please add funds to your wallet to enable AI advisory services.")
        return

    col_sel, _ = st.columns([1, 2])
    with col_sel:
        sel_cur = st.selectbox("Funding Wallet", list(wallets.keys()))

    balance = wallets[sel_cur]
    risk    = user_data.get('risk_profile', 'low')

    # ── AI INFERENCE ──
    with st.spinner("🤖 AI Model scanning ThirdParty Digital Assets..."):
        raw_funds = client.get_public_funds()
        df_recs   = engine.get_recommendations(risk, balance, raw_funds)

    # ── CONTEXT BANNER ──
    st.markdown(f"""
    <div class="ctx-banner">
    <div class="ctx-banner-inner">
        <div>
            <div style="color:rgba(255,255,255,0.6);font-size:10px;font-weight:600;
                        letter-spacing:1.5px;text-transform:uppercase">Analysis Context</div>
            <div style="color:white;font-size:15px;font-weight:600;margin-top:3px">
                {sel_cur} &nbsp;·&nbsp; £{balance:,.2f} &nbsp;·&nbsp; Risk: {risk.upper()}
            </div>
        </div>
        <div class="ctx-fund-count">{len(df_recs)} Funds Analysed</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CHARTS ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-left"><div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<span class="sect-title">💧 Liquidity Profile</span>', unsafe_allow_html=True)
        fig_pie = px.pie(df_recs, values='liquidity_score', names='name', hole=0.52,
                         color_discrete_sequence=px.colors.sequential.Greens_r)
        fig_pie.update_traces(textfont=dict(size=11))
        fig_pie.update_layout(margin=dict(t=20,b=10,l=10,r=10),
                               paper_bgcolor="rgba(0,0,0,0)",
                               legend=dict(font=dict(size=11)))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-right"><div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<span class="sect-title">⚖️ Risk-Reward</span>', unsafe_allow_html=True)
        fig_bar = go.Figure(data=[
            go.Bar(name='Yield (%)',  x=df_recs['name'], y=df_recs['yield'],
                   marker_color='#006a4d', marker_line_width=0),
            go.Bar(name='Volatility', x=df_recs['name'], y=df_recs['volatility'],
                   marker_color='#c9a84c', marker_line_width=0)
        ])
        fig_bar.update_layout(barmode='group', margin=dict(t=10,b=10,l=0,r=0),
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white",
                               yaxis=dict(gridcolor="#f0f5f3"),
                               legend=dict(font=dict(size=11)),
                               font=dict(family="DM Sans"))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.divider()

    # ── TOP PICK ──
    top_fund = df_recs.iloc[0]

    st.markdown(f"""
    <div class="top-pick">
    <div class="top-pick-banner">
        <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;color:#00a372;
                    text-transform:uppercase;margin-bottom:4px">🏆 AI Top Recommendation</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:700;
                    color:#003d2b">{top_fund['name']}</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_gauge = st.columns([1, 1])

    with col_info:
        st.markdown('<span class="sect-title">Selection Reasoning</span>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        for label, val in [
            ("ML Confidence", f"{top_fund['ai_score']}%"),
            ("Asset ISIN",    top_fund['isin']),
            ("Yield",         f"{top_fund['yield']}%"),
        ]:
            st.markdown(f"""
            <div class="stat-pill">
                <span class="pill-label">{label}</span>
                <span class="pill-value">{val}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ai-reason">
            The Random Forest model identified this as the optimal match for a
            <strong>{risk.upper()}</strong> risk profile with a balance of
            <strong>{sel_cur} {balance:,.2f}</strong>.
        </div>""", unsafe_allow_html=True)

        if st.button("Subscribe to Fund →", use_container_width=True):
            st.balloons()
            st.toast("Subscription request sent to Third Party Ledger", icon="🏦")

    with col_gauge:
        st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=top_fund['ai_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "AI Match Quality", 'font': {'size': 16, 'color': "#003d2b", 'family': "DM Sans"}},
            number={'font': {'size': 44, 'color': "#006a4d", 'family': "Cormorant Garamond"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8a9e97"},
                'bar':  {'color': "#006a4d", 'thickness': 0.25},
                'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "#e8eeec",
                'steps': [
                    {'range': [0,  50], 'color': '#f0faf6'},
                    {'range': [50, 80], 'color': '#c8e6c9'},
                    {'range': [80,100], 'color': '#81c784'},
                ],
                'threshold': {'line': {'color': "#c9a84c", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ))
        fig_gauge.update_layout(height=320, margin=dict(t=50,b=10,l=20,r=20),
                                 paper_bgcolor="rgba(0,0,0,0)",
                                 font=dict(family="DM Sans"))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── STRESS TEST ──
    st.markdown("""
    <div class="stress-sec">
        <span class="sect-title">🛡️ Institutional Risk Stress Test</span>
        <p style="color:#5a6b64;font-size:13px;margin:0.6rem 0 0.8rem">
            Model portfolio recovery if markets dropped today.
        </p>
    </div>
    """, unsafe_allow_html=True)

    crash = st.select_slider(
        "Simulate Market Shock",
        options=[0, 10, 20, 30], value=0,
        format_func=lambda x: f"{x}% Shock" if x else "No Shock"
    )

    if crash > 0:
        stressed = engine.simulate_stress_test(df_recs.to_dict('records'), crash)
        fig_area = px.area(stressed, x="name", y="recovery_months",
                           title=f"Estimated Recovery Time — {crash}% Crash Scenario",
                           labels={"recovery_months": "Months to Par", "name": "Fund Asset"},
                           color_discrete_sequence=["#e57373"])
        fig_area.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white",
                                yaxis=dict(gridcolor="#fde8e8"), font=dict(family="DM Sans"))
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.markdown("""
        <div class="stress-empty">
            Select a market shock percentage above to run the simulation.
        </div>""", unsafe_allow_html=True)