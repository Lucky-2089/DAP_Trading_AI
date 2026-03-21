import streamlit as st
import pandas as pd
import numpy as np


def show_dashboard(user_data):
    # --- Header Section ---
    st.header(f"💼 Institutional Overview: {user_data['name']}")
    st.caption(f"Portal Access: Standard | Last Login: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

    # --- Key Metrics Row ---
    col1, col2, col3, col4 = st.columns(4)

    # 1. Calculate Total Balance (Simplified for demo)
    total_gbp = user_data['wallets'].get('GBP', 0)
    total_usd = user_data['wallets'].get('USD', 0)

    col1.metric("Risk Profile", user_data['risk_profile'].upper(), help="Based on your KYC onboarding assessment.")
    col2.metric("Base Currency", user_data['base_currency'])
    col3.metric("AI Health", "99.2%", delta="Optimal", help="Real-time Random Forest Model Accuracy.")
    col4.metric("Market Sentiment", "Bullish", delta="1.2%", help="Aggregated trend of monitored MMFs.")

    st.divider()

    # --- Portfolio Analytics Section ---
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📈 Portfolio Performance (Projected)")
        # Simulating a small growth trend for the UI feel
        chart_data = pd.DataFrame(
            np.random.randn(20, 1).cumsum() + 10,
            columns=['Portfolio Value']
        )
        st.line_chart(chart_data, height=250)
        st.caption("Trailing 20-day performance of your active tokenized assets.")

    with right_col:
        st.subheader("📊 Asset Allocation")
        # Create a small pie chart for wallet distribution
        wallet_data = pd.DataFrame({
            "Currency": list(user_data['wallets'].keys()),
            "Value": list(user_data['wallets'].values())
        })
        st.dataframe(
            wallet_data,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Value": st.column_config.NumberColumn(format="%.2f")
            }
        )

        # Quick Quick Action
        st.warning(
            f"💡 AI suggests optimizing your **{user_data['risk_profile']}** risk profile with higher yield MMFs.")

    st.divider()

    # --- Institutional News/Alerts ---
    st.subheader("🔔 Market Intelligence")

    # Simulating dynamic news based on user's portfolio
    news_col1, news_col2 = st.columns(2)
    with news_col1:
        st.info("**SONIA Rate Update**: UK Sterling Overnight Index Average remains stable at 5.20%.")
    with news_col2:
        st.success("**New Asset Alert**: Archax has listed a new BlackRock tokenized Treasury fund.")

    # --- Transaction Quick View ---
    with st.expander("🔍 View Recent System Logs"):
        if user_data.get('transactions'):
            st.table(user_data['transactions'][:3])  # Show last 3
        else:
            st.write("No system logs for this session.")