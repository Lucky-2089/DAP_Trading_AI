import json
import os
from datetime import datetime


class MockDB:
    def __init__(self, file_name="portal_db.json"):
        # Setup path to save the JSON in the same folder as this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, file_name)

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.users = json.load(f)
        else:
            # Seed initial data for your POC
            self.users = {
                "user1": {
                    "password": "password123",
                    "name": "Laxman Telang",
                    "risk_profile": "medium",
                    "wallets": {"GBP": 50000.0, "USD": 10000.0},
                    "transactions": []
                }
            }
            self._save()

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.users, f, indent=4)

    def get_user(self, username):
        return self.users.get(username)

    def update_wallet(self, username, currency, amount, description="Transfer"):
        if username in self.users:
            user = self.users[username]

            # Initialization checks
            if "wallets" not in user:
                user["wallets"] = {"GBP": 0.0, "USD": 0.0}
            if "transactions" not in user:
                user["transactions"] = []

            current_bal = user["wallets"].get(currency, 0.0)

            # Prevent overdraft
            if current_bal + amount < 0:
                return False

            # Update logic
            user["wallets"][currency] = round(current_bal + amount, 2)

            new_tx = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": description,
                "amount": amount,
                "currency": currency,
                "status": "Settled"
            }
            user["transactions"].insert(0, new_tx)
            self._save()
            return True
        return False


# --- CRITICAL: THIS MUST BE OUTSIDE THE CLASS (NO INDENTATION) ---
db = MockDB()