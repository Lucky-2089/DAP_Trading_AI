import streamlit as st
import pandas as pd
from backend.database import db


def _anim_css():
    st.markdown("""
    <style>
    .wallet-header { animation:fadeUp 0.5s 0s cubic-bezier(0.16,1,0.3,1) both; }

    /* Balance metric stagger */
    [data-testid="column"]:nth-child(1) [data-testid="stMetric"] { animation-delay:0.06s }
    [data-testid="column"]:nth-child(2) [data-testid="stMetric"] { animation-delay:0.13s }
    [data-testid="column"]:nth-child(3) [data-testid="stMetric"] { animation-delay:0.20s }

    /* Deposit form card */
    .deposit-card {
        animation:fadeUp 0.5s 0.15s both;
    }

    /* Account status card hover */
    .acct-card {
        background:#f7f8f6; border:1px solid rgba(0,106,77,0.12);
        border-radius:12px; padding:1.4rem; margin-top:0.3rem;
        animation:fadeUp 0.5s 0.2s both;
        transition:all 0.35s cubic-bezier(0.16,1,0.3,1);
    }
    .acct-card:hover { box-shadow:0 10px 32px rgba(0,0,0,0.09); transform:translateY(-2px); }

    /* Ledger section */
    .ledger-section { animation:fadeUp 0.6s 0.3s both; }

    /* Empty state */
    .empty-state {
        background:#f7f8f6; border:1.5px dashed rgba(0,106,77,0.2);
        border-radius:12px; padding:2rem; text-align:center; color:#8a9e97;
        font-size:14px; animation:fadeUp 0.5s 0.35s both;
    }

    /* Stat row inside account card */
    .stat-row {
        display:flex; justify-content:space-between; align-items:center;
        padding:0.55rem 0.8rem; background:white; border-radius:8px;
        border:1px solid rgba(0,106,77,0.08); margin-bottom:6px;
        transition:all 0.25s;
    }
    .stat-row:hover { border-color:rgba(0,106,77,0.25); transform:translateX(3px); }
    .stat-label { font-size:11px; font-weight:600; color:#5a6b64; text-transform:uppercase; letter-spacing:0.8px; }
    .stat-value { font-size:14px; font-weight:700; color:#003d2b; }

    /* Badges */
    .pill-green { background:#d6f0e8; color:#006a4d; font-size:12px; font-weight:700; padding:2px 10px; border-radius:20px; }
    .pill-gold  { background:#fff8e1; color:#c9a84c; font-size:12px; font-weight:700; padding:2px 10px; border-radius:20px; }
    .pill-red   { background:#fdecea; color:#c0392b; font-size:12px; font-weight:700; padding:2px 10px; border-radius:20px; }

    /* Section title */
    .sect-title {
        font-family:'Cormorant Garamond',serif; font-size:19px; font-weight:700;
        color:#003d2b; margin-bottom:0.3rem; position:relative; display:inline-block;
    }
    .sect-title::after {
        content:''; position:absolute; bottom:-3px; left:0; height:2px; width:0;
        background:linear-gradient(90deg,#006a4d,#c9a84c);
        animation:lineGrow 0.7s 0.4s cubic-bezier(0.16,1,0.3,1) forwards;
    }

    @keyframes fadeUp   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
    @keyframes lineGrow { to{width:100%} }
    </style>
    """, unsafe_allow_html=True)


def show_wallet(user_id, user_data):
    _anim_css()

    # ── PAGE HEADER ──
    st.markdown("""
    <div class="wallet-header" style="margin-bottom:1.8rem">
        <div style="font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;
                    color:#00a372;margin-bottom:4px">Asset Management</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:700;
                    color:#003d2b;letter-spacing:-0.5px">Wallet Management</div>
    </div>
    """, unsafe_allow_html=True)

    wallets = user_data.get('wallets', {})

    # ── BALANCE METRICS ──
    if not wallets:
        st.info("No active wallets found. Create one using the deposit form below.")
    else:
        st.markdown('<span class="sect-title">Your Liquidity</span>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        cols = st.columns(len(wallets))
        for i, (curr, bal) in enumerate(wallets.items()):
            cols[i].metric(
                label=f"{curr} Account",
                value=f"£{bal:,.2f}" if curr == "GBP" else f"{curr} {bal:,.2f}",
                delta="Live Balance"
            )

    st.divider()

    # ── DEPOSIT + ACCOUNT ──
    col1, _, col2 = st.columns([1, 0.08, 1])

    with col1:
        st.markdown('<div class="deposit-card">', unsafe_allow_html=True)
        st.markdown('<span class="sect-title">📥 Add Funds</span>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#5a6b64;font-size:13px;margin:0.6rem 0 0.9rem">
            Transfer from your external bank account to your digital wallet.
        </p>""", unsafe_allow_html=True)

        currency = st.selectbox("Select Currency", ["GBP", "USD"], key="deposit_curr")
        amount   = st.number_input("Amount to Deposit", min_value=100.0, step=500.0, format="%.2f", key="deposit_amt")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("Confirm Deposit →", use_container_width=True):
            success = db.update_wallet(user_id, currency, amount, description="Manual Deposit (External Bank)")
            if success:
                st.toast(f"✅ Deposited {currency} {amount:,.2f} successfully!", icon="💳")
                st.rerun()
            else:
                st.error("Deposit failed. Please contact support.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        risk = user_data.get('risk_profile', 'low')
        pill_class = {"low": "pill-green", "medium": "pill-gold", "high": "pill-red"}.get(risk, "pill-green")

        st.markdown('<span class="sect-title">📊 Account Status</span>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="acct-card">
            <div class="stat-row">
                <span class="stat-label">Account Holder</span>
                <span class="stat-value">{user_data['name']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">KYC Status</span>
                <span class="{pill_class}">✓ Verified</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Risk Profile</span>
                <span class="{pill_class}">{risk.upper()}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Total AUM</span>
                <span class="stat-value">£{sum(wallets.values()):,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── TRANSACTION LEDGER ──
    st.markdown('<div class="ledger-section">', unsafe_allow_html=True)
    st.markdown('<span class="sect-title">📜 Transaction Ledger</span>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#5a6b64;font-size:13px;margin:0.6rem 0 0.8rem">
        Real-time audit trail of all wallet and investment activities.
    </p>""", unsafe_allow_html=True)

    transactions = user_data.get('transactions', [])
    if transactions:
        df_tx = pd.DataFrame(transactions)
        if not df_tx.empty:
            st.dataframe(df_tx, column_config={
                "timestamp":   st.column_config.TextColumn("Date & Time"),
                "description": st.column_config.TextColumn("Activity"),
                "amount":      st.column_config.NumberColumn("Amount", format="%.2f"),
                "currency":    st.column_config.TextColumn("CCY"),
                "status":      st.column_config.TextColumn("Status"),
            }, hide_index=True, use_container_width=True, height=320)
        else:
            st.info("No activity recorded yet.")
    else:
        st.markdown("""
        <div class="empty-state">
            No recent transactions found.<br>
            <span style="font-size:12px">Start by depositing funds or making an investment.</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)