import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from backend.api_mock import ArchaxPublicClient
from backend.ai_engine import RecommenderAPI


def show_investment(user_data):
    st.header("🤖 AI Institutional Advisor")
    client, engine = ArchaxPublicClient(), RecommenderAPI()

    # 1. Data Context
    wallets = user_data.get('wallets', {})
    if not wallets:
        st.warning("Please add funds to your wallet to enable AI advisory.")
        return

    sel_cur = st.selectbox("Funding Wallet", list(wallets.keys()))
    balance, risk = wallets[sel_cur], user_data.get('risk_profile', 'low')

    # 2. AI Inference
    with st.spinner("AI Model scanning Archax Digital Assets..."):
        raw_funds = client.get_public_funds()
        df_recs = engine.get_recommendations(risk, balance, raw_funds)

    # 3. Visualizations: Donut & Bar Charts
    st.subheader("💧 Liquidity Profile")
    st.plotly_chart(px.pie(df_recs, values='liquidity_score', names='name', hole=0.5,
                           color_discrete_sequence=px.colors.sequential.Greens_r), use_container_width=True)

    st.subheader("⚖️ Risk-Reward Comparison")
    fig_bar = go.Figure(data=[
        go.Bar(name='Yield (%)', x=df_recs['name'], y=df_recs['yield'], marker_color='#006a4d'),
        go.Bar(name='Volatility', x=df_recs['name'], y=df_recs['volatility'], marker_color='#a5d6a7')
    ])
    fig_bar.update_layout(barmode='group', margin=dict(t=20, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # 4. Top Pick Section with LARGE Centered Gauge
    top_fund = df_recs.iloc[0]
    st.success(f"🏆 AI TOP RECOMMENDATION: {top_fund['name']}")

    col_info, col_gauge = st.columns([1, 1])

    with col_info:
        st.markdown("### Selection Reasoning")
        st.write(f"**ML Confidence:** {top_fund['ai_score']}%")
        st.write(f"**Asset ISIN:** {top_fund['isin']}")
        st.write(f"**Yield:** {top_fund['yield']}%")
        st.info(
            f"The Random Forest model identified this as the optimal match for a **{risk.upper()}** risk profile with a balance of **{sel_cur} {balance:,.2f}**.")

        if st.button("Subscribe to Fund", use_container_width=True):
            st.balloons()
            st.toast("Subscription request sent to Archax Ledger", icon="🏦")

    with col_gauge:
        # Centering and sizing the Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=top_fund['ai_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "AI Match Quality", 'font': {'size': 20, 'color': "#006a4d"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#006a4d"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#eeeeee",
                'steps': [
                    {'range': [0, 50], 'color': '#f1f8e9'},
                    {'range': [50, 85], 'color': '#c8e6c9'},
                    {'range': [85, 100], 'color': '#81c784'}
                ],
                'threshold': {
                    'line': {'color': "orange", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}
            }
        ))

        fig_gauge.update_layout(
            height=350,  # Larger height for visibility
            margin=dict(t=60, b=20, l=30, r=30),
            paper_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

    # 5. Stress Test Section
    st.divider()
    st.subheader("🛡️ Institutional Risk Stress Test")
    st.caption("How will your portfolio recover if the market drops today?")

    crash = st.select_slider("Simulate Market Shock %", options=[0, 10, 20, 30], value=0)
    if crash > 0:
        stressed = engine.simulate_stress_test(df_recs.to_dict('records'), crash)
        st.plotly_chart(px.area(stressed, x="name", y="recovery_months",
                                title=f"Estimated Recovery Time ({crash}% Crash Scenario)",
                                labels={"recovery_months": "Months to Par", "name": "Fund Asset"},
                                color_discrete_sequence=["#e57373"]), use_container_width=True)
    else:
        st.info("Select a percentage above to run the market simulation.")