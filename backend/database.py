import json
import os
from datetime import datetime


class MockDB:
    def __init__(self, file_name="portal_db.json"):
        # This ensures the database file is always created in the 'backend' folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, file_name)

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.users = json.load(f)
        else:
            # Initializing with the 'transactions' list for the ledger
            self.users = {
                f"user{i}": {
                    "password": "password123",
                    "name": f"Customer 00{i}",
                    "risk_profile": "low" if i < 4 else ("medium" if i < 8 else "high"),
                    "base_currency": "GBP" if i % 2 == 0 else "USD",
                    "wallets": {"GBP": 10000.0, "USD": 10000.0},
                    "transactions": []  # CRITICAL: Added for the audit trail
                } for i in range(1, 11)
            }
            self._save()

    def _save(self):
        """Persists the current state to the JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(self.users, f, indent=4)

    def get_user(self, username):
        return self.users.get(username)

    def update_wallet(self, username, currency, amount, description="Transfer"):
        """
        Updates balance and records the event in the ledger.
        Accepts 'description' to fix the TypeError.
        """
        if username in self.users:
            user = self.users[username]
            current_bal = user["wallets"].get(currency, 0)

            # Prevent negative balance for realism
            if current_bal + amount < 0:
                return False

            # 1. Update Balance
            user["wallets"][currency] = round(current_bal + amount, 2)

            # 2. Record Transaction to the Ledger (for the UI table)
            user["transactions"].insert(0, {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": description,
                "amount": amount,
                "currency": currency,
                "status": "Settled"
            })

            # 3. Save to file
            self._save()
            return True
        return False


# Create the single global instance
db = MockDB()