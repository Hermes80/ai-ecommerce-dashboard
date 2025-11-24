from dotenv import load_dotenv
import os

# Load .env file from project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

# Core eBay OAuth app credentials
EBAY_APP_ID = os.getenv("EBAY_APP_ID")          # aka Client ID
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID")        # aka Client Secret

# Redirect URI registered in eBay Dev Portal
EBAY_REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI")

# Long-lived refresh token you got after user consent
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

# OAuth + API endpoints (prod by default)
EBAY_OAUTH_URL = os.getenv(
    "EBAY_OAUTH_URL",
    "https://api.ebay.com/identity/v1/oauth2/token"
)

EBAY_REST_URL = os.getenv(
    "EBAY_REST_URL",
    "https://api.ebay.com"
)

# Optional: basic sanity checks (won't crash, just warn)
def _warn_if_missing(name, value):
    if not value:
        print(f"[CONFIG WARNING] {name} is not set. Check your .env file.")

_warn_if_missing("EBAY_APP_ID", EBAY_APP_ID)
_warn_if_missing("EBAY_CERT_ID", EBAY_CERT_ID)
_warn_if_missing("EBAY_REDIRECT_URI", EBAY_REDIRECT_URI)
_warn_if_missing("EBAY_REFRESH_TOKEN", EBAY_REFRESH_TOKEN)
