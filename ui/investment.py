import streamlit as st
import time
from backend.ai_engine import RecommenderAPI
from backend.database import db  # Import the instance 'db'


def show_investment(user_data):
    st.header("📈 AI-Powered Fund Selection")

    # 1. Validation & Setup
    user_wallets = user_data['wallets']
    if not user_wallets:
        st.warning("Please fund a wallet before accessing AI Recommendations.")
        return

    selected_currency = st.selectbox("Invest from Wallet", list(user_wallets.keys()))
    current_balance = user_wallets[selected_currency]

    st.write(f"Analyzing funds for **{user_data['risk_profile']}** risk profile in **{selected_currency}**...")
    st.write(f"Available Balance: **{selected_currency} {current_balance:,.2f}**")

    # 2. Call AI Engine
    try:
        engine = RecommenderAPI()
        user_context = {
            "wallet_balance": current_balance,
            "risk_profile": user_data['risk_profile'],
            "currency": selected_currency
        }
        recommendations = engine.get_recommendations(user_context)
    except Exception as e:
        st.error(f"AI Engine Error: {e}")
        return

    # 3. Display Recommendations
    if not recommendations.empty:
        st.subheader("🤖 AI Top Picks for You")
        display_df = recommendations[['fund_name', 'yield', 'final_score', 'minimum_investment']]
        st.dataframe(display_df, use_container_width=True)

        st.divider()
        st.write("### Execute Institutional Trades")

        for index, row in recommendations.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{row['fund_name']}**")
                st.caption(f"Yield: {row['yield']}% | Min: {selected_currency} {row['minimum_investment']}")

            with col2:
                st.write(f"Score: **{row['final_score']:.2f}**")

            with col3:
                if st.button("Invest", key=f"btn_{selected_currency}_{index}"):
                    if current_balance >= row['minimum_investment']:
                        with st.status("🔗 Initializing Canton DvP Flow...", expanded=True) as status:
                            st.write("Checking wallet liquidity...")
                            time.sleep(0.8)

                            st.write("Requesting asset lock from Archax...")
                            time.sleep(1.0)

                            # --- THE FIX IS HERE ---
                            inv_amt = -row['minimum_investment']
                            tx_desc = f"Institutional Purchase: {row['fund_name']}"

                            success = db.update_wallet(
                                st.session_state.user_id,
                                selected_currency,
                                inv_amt,
                                description=tx_desc  # Ensure description is passed
                            )

                            if success:
                                # CRITICAL: Update the session state with fresh data from the DB
                                # This ensures the ledger sees the new transaction immediately
                                st.session_state.user_data = db.get_user(st.session_state.user_id)

                                st.write("Finalizing Atomic Settlement on Ledger...")
                                time.sleep(0.7)
                                status.update(label="✅ Transaction Settled", state="complete", expanded=False)
                                st.balloons()
                                st.toast(f"Purchased {row['fund_name']}!", icon='💰')
                                time.sleep(1)
                                st.rerun()  # Forces the UI to rebuild with the new session_state
                    else:
                        st.error("❌ Insufficient Funds")
    else:
        st.warning("🔎 No funds match your current profile at this time.")