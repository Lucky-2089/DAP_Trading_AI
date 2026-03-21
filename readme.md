# 🏦 Institutional Digital Asset Portal (DApp POC)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-006a4d.svg)](https://www.python.org/)

## 📝 Overview
This **Digital Asset Portal** is a high-fidelity Proof of Concept (POC) designed for institutional users within the ** Technology Center** ecosystem. It provides a secure gateway for managing digital assets, funding wallets, and performing asset swaps via the **Archax Exchange** and **Canton Blockchain**.

The UI is strictly engineered to follow ** Bank Institutional Branding**, utilizing a custom **Sandstone and Racing Green** color palette with smooth CSS3 animations for a premium user experience.

---

## 🛠 Tech Stack
| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python-based Web Framework) |
| **Styling** | Custom CSS3, Animate.css (v4.1.1) |
| **Animations** | Lottie (LottieFiles) & `streamlit-lottie` |
| **Backend** | Python Modular Architecture |
| **AI Engine** | Gemini AI (Ready for Guarantee Text Vetting) |
| **Blockchain** | Canton Network / Archax Exchange Integration Logic |

---

## 📂 Project Structure
```text
dap_trading_ai/
├── requirements.txt      # Dependencies: streamlit, requests, streamlit-lottie
├── .streamlit/           # Streamlit configuration and secrets
├── backend/
│   └── database.py       # Mock DB & Auth Logic (Module Lead: Quality Engineering)
└── ui/
    ├── app.py            # Main Entry Point (Navigation & Global CSS)
    ├── auth.py           # Animated Login (Institutional Gateway)
    ├── dashboard.py      # Portfolio & Performance Overview
    ├── wallet.py         # Digital Wallet & Tokenization Logic
    └── investment.py     # AI-Driven Investment Portal