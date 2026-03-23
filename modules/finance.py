import stripe
import json
from datetime import datetime, timedelta
from pathlib import Path

class FinanceManager:
    def __init__(self, api_key=None):
        if api_key:
            stripe.api_key = api_key
        self.config_path = Path.home() / ".stormy" / "finance.json"
        self.config = self.load_config()

    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "fnb_account": "",
            "african_bank_account": "",
            "reserve_balance": 0.0,
            "last_payout": None
        }

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f)

    def process_payment(self, amount_cents, currency="zar"):
        # This would be called when a user subscribes
        # For now, just a stub
        pass

    def weekly_payout(self, total_revenue):
        # total_revenue is in ZAR (or base currency)
        # Split: 40% FNB, 20% African Bank, 7% reserve, 33% operational (not paid out)
        fnb_share = total_revenue * 0.40
        african_share = total_revenue * 0.20
        reserve_share = total_revenue * 0.07
        operational = total_revenue * 0.33

        # Update reserve balance
        self.config["reserve_balance"] += reserve_share

        # Perform payouts (stubbed)
        # stripe.Transfer.create(amount=fnb_share, currency="zar", destination=self.config["fnb_account"])
        # stripe.Transfer.create(amount=african_share, currency="zar", destination=self.config["african_bank_account"])

        self.config["last_payout"] = datetime.utcnow().isoformat()
        self.save_config()

        return {
            "fnb": fnb_share,
            "african_bank": african_share,
            "reserve_added": reserve_share,
            "reserve_total": self.config["reserve_balance"],
            "operational": operational
        }
