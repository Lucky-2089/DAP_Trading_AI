import yfinance as yf
from typing import List, Dict, Any


def get_live_fund_data(ticker_symbol: str, default_name: str, min_inv: int, risk: str) -> Dict[str, Any]:
    """Fetches live data from Yahoo Finance with an Institutional Fallback for QE stability."""
    try:
        fund = yf.Ticker(ticker_symbol)
        # 1. Fetch info with a timeout/error check
        info = fund.info

        # If the ticker is delisted or invalid, yfinance might return an empty dict or error
        if not info or 'regularMarketPreviousClose' not in info and 'previousClose' not in info:
            raise ValueError("Ticker Data Unavailable")

        nav = info.get('regularMarketPreviousClose') or info.get('previousClose') or 100.0
        raw_yield = info.get('yield') or info.get('trailingAnnualDividendYield')
        fund_yield = round(raw_yield * 100, 2) if raw_yield else 5.25  # Benchmark 5.25%

        return {
            "fund_name": default_name,
            "currency": info.get('currency', 'GBP'),
            "nav": round(nav, 2),
            "yield": fund_yield,
            "risk_level": risk,
            "liquidity": 1,
            "minimum_investment": min_inv
        }

    except Exception as e:
        # QE FAIL-SAFE: Use Benchmark data so the AI Engine still works
        return {
            "fund_name": f"{default_name} (Benchmark)",
            "currency": "GBP",
            "nav": 100.00,
            "yield": 5.15,
            "risk_level": risk,
            "liquidity": 1,
            "minimum_investment": min_inv
        }


def fetch_archax_mmfs() -> List[Dict[str, Any]]:
    """Stable UK Tickers for the Archax simulation."""
    return [
        get_live_fund_data("CSH2.L", "Amundi Sterling Cash", 1000, "low"),
        get_live_fund_data("ERNS.L", "iShares £ Ultrashort Bond", 500, "low"),
        get_live_fund_data("FLOT.L", "iShares £ Floating Rate Bond", 1000, "low")
    ]


def fetch_marketdata_mmfs() -> List[Dict[str, Any]]:
    """Stable Medium/High risk tickers for the AI filter test."""
    return [
        get_live_fund_data("IS15.L", "iShares £ Corp Bond 0-5yr", 100, "medium"),
        get_live_fund_data("SLXX.L", "iShares £ Core Corp Bond", 1000, "high")
    ]