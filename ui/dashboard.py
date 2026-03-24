import streamlit as st
import pandas as pd
import plotly.express as px
from backend.api_mock import ArchaxPublicClient

def show_dashboard(user_data):
    st.title(f"Institutional Portal: {user_data['name']}")
    client = ArchaxPublicClient()

    c1, c2, c3 = st.columns(3)
    c1.metric("Compliance", "KYC Approved", delta="Verified")
    wallets = user_data.get('wallets', {})
    c2.metric("Total AUM", f"GBP {sum(wallets.values()):,.2f}")
    c3.metric("AI Risk Profile", user_data.get('risk_profile', 'low').upper())

    st.subheader("📊 Market Intelligence: 30-Day Gilt Yield Trend")
    perf_data = client.get_gilt_performance_data()
    fig_line = px.line(perf_data, x="Date", y="Yield (%)", template="plotly_white", color_discrete_sequence=["#006a4d"])
    st.plotly_chart(fig_line, use_container_width=True)

    col_chart, col_ledger = st.columns([1, 1])
    with col_chart:
        st.subheader("💰 Asset Allocation")
        df_wallets = pd.DataFrame(list(wallets.items()), columns=['Currency', 'Balance'])
        fig_pie = px.pie(df_wallets, values='Balance', names='Currency', hole=0.4, color_discrete_sequence=['#006a4d', '#81c784'])
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_ledger:
        st.subheader("📝 Settlement Ledger")
        st.dataframe(pd.DataFrame(user_data.get('transactions', [])), hide_index=True, use_container_width=True, height=250)