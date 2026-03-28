import numpy as np
import requests
import pandas as pd
from datetime import datetime, timedelta

class ArchaxPublicClient:
    def __init__(self):
        self.base_url = "https://ace.archax.com/api/3.0/rest-gateway"

    def get_public_funds(self):
        """Fetches public asset metadata from Third Party with a robust fallback."""
        try:
            response = requests.get(f"{self.base_url}/assets", timeout=5)
            if response.status_code == 200:
                all_assets = response.json().get('data', [])
                funds = [a for a in all_assets if a.get('assetClass') == 'FUND']
                if funds: return funds
        except Exception:
            pass
        return self._get_fallback_funds()

    def get_gilt_performance_data(self):
        """Generates 30 days of synthetic Gilt yield data for the AI POC."""
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
        dates.reverse()
        trend = np.linspace(0, 0.5, 30)
        yields = (np.random.uniform(4.5, 4.8, size=30) + trend).tolist()
        return pd.DataFrame({"Date": dates, "Yield (%)": yields, "Asset": "UK Gilt 2024"})

    def _get_fallback_funds(self):
        return [
            {"name": "abrdn Sterling MMF", "isin": "GB00B4W3Q943", "assetTicker": "ABRDN.STG", "yield": 5.25},
            {"name": "BlackRock ICS US Treasury", "isin": "IE00B1S75308", "assetTicker": "BLK.UST", "yield": 5.10},
            {"name": "Fidelity Inst. Liquidity", "isin": "IE0003323537", "assetTicker": "FID.LQD", "yield": 5.15}
        ]