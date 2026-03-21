import streamlit as st
import pandas as pd
from backend.database import db


def show_wallet(user_id, user_data):
    st.header("💳 Wallet Management")

    # 1. Display Current Balances with modern metrics
    if not user_data.get('wallets'):
        st.info("No active wallets found. Please create one below.")
    else:
        st.subheader("Your Liquidity")
        cols = st.columns(len(user_data['wallets']))
        for i, (curr, bal) in enumerate(user_data['wallets'].items()):
            cols[i].metric(
                label=f"{curr} Account",
                value=f"{curr} {bal:,.2f}",
                delta="Live Balance"
            )

    st.divider()

    # 2. Add Funds Section
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📥 Add Funds")
        st.caption("Transfer funds from your external bank account to your digital wallet.")

        currency = st.selectbox("Select Currency", ["GBP", "USD"], key="deposit_curr")
        amount = st.number_input("Amount to Deposit", min_value=100, step=500, key="deposit_amt")

        if st.button("Confirm Deposit", use_container_width=True):
            # Using the logic we built: adding a description for the ledger
            success = db.update_wallet(
                user_id,
                currency,
                amount,
                description="Manual Deposit (External Bank)"
            )
            if success:
                st.toast(f"Successfully deposited {amount} {currency}!", icon="✅")
                st.rerun()

    with col2:
        st.subheader("📊 Account Status")
        st.info(f"Account Holder: **{user_data['name']}** \n"
                f"KYC Status: **Verified** \n"
                f"Risk Profile: **{user_data['risk_profile'].upper()}**")

    st.divider()

    # 3. Professional Transaction Ledger
    st.subheader("📜 Transaction Ledger")
    st.caption("Real-time audit trail of all wallet and investment activities.")

    # Safely check for transaction history
    transactions = user_data.get('transactions', [])

    if transactions:
        df_tx = pd.DataFrame(transactions)

        # Format the dataframe for a cleaner look
        # Note: If 'timestamp' or 'amount' keys vary in your database.py, update them here
        if not df_tx.empty:
            # We use st.dataframe for a scrollable, sortable professional table
            st.dataframe(
                df_tx,
                column_config={
                    "timestamp": "Date & Time",
                    "description": "Activity",
                    "amount": st.column_config.NumberColumn("Amount", format="%.2f"),
                    "currency": "CCY",
                    "status": st.column_config.TextColumn("Status")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No activity recorded yet.")
    else:
        st.info("No recent transactions found. Start by depositing funds or making an investment.")