from typing import Dict


class CantonSimulator:
    @staticmethod
    def buy_asset(wallet: Dict, fund_name: str, nav: float, amount: float) -> Dict:
        if amount > wallet['wallet_balance']:
            return {"status": "Failed", "message": "Insufficient funds for DvP"}

        tokens = amount / nav
        return {
            "status": "Success",
            "message": f"DvP Locked: Swapped {amount} {wallet['currency']} for {tokens:.2f} tokens of {fund_name}.",
            "tokens": tokens,
            "cost": amount
        }