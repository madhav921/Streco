# auth.py

import os
import pickle
from neo_api_client import NeoAPI
from kotak_config import CONSUMER_KEY, MOBILE_NUMBER, UCC, TOTP, MPIN

SESSION_FILE = "kotak_session.pkl"


class KotakSession:
    _client = None   # Singleton instance

    def __init__(self):
        self.client = NeoAPI(
            environment="prod",
            consumer_key=CONSUMER_KEY,
            access_token=None,
            neo_fin_key=None
        )

    # -------------------------
    # Save session tokens
    # -------------------------
    def _save_session(self):
        with open(SESSION_FILE, "wb") as f:
            pickle.dump(self.client, f)

    # -------------------------
    # Load session tokens
    # -------------------------
    def _load_session(self):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "rb") as f:
                self.client = pickle.load(f)
            print("✅ Loaded saved Kotak session")
            return True
        return False

    # -------------------------
    # Login function
    # -------------------------
    def login(self, force=False):
        if KotakSession._client and not force:
            return KotakSession._client

        # Try loading saved session
        if not force and self._load_session():
            KotakSession._client = self.client
            return self.client

        try:
            print("🔐 Logging in to Kotak Neo (TOTP)...")

            self.client.totp_login(
                mobile_number=MOBILE_NUMBER,
                ucc=UCC,
                totp=TOTP
            )

            self.client.totp_validate(mpin=MPIN)

            print("✅ Kotak Neo login successful")
            self._save_session()

            KotakSession._client = self.client
            return self.client

        except Exception as e:
            print("❌ Kotak Neo login failed:", e)
            return None

    # -------------------------
    # Auto reconnect if session expired
    # -------------------------
    def get_client(self):
        if not KotakSession._client:
            return self.login()

        try:
            # Test call (any lightweight API)
            KotakSession._client.get_profile()
            return KotakSession._client
        except Exception:
            print("⚠️ Session expired. Re-logging...")
            return self.login(force=True)
