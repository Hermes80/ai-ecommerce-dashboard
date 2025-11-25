import os
import base64
import requests

# ==========================================================
# eBay Production Credentials (update with your own values)
# ==========================================================
EBAY_APP_ID = "Christop-Storepil-PRD-86e535c40-6a1b1745"
EBAY_CERT_ID = "YOUR_CERT_ID"
EBAY_REDIRECT_URI = "https://auth.ebay.com/oauth2/redirect"
EBAY_REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_REST_URL = "https://api.ebay.com"

# ==========================================================
# Helper to encode credentials for OAuth
# ==========================================================
def base64_credentials():
    creds = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(creds.encode()).decode()

# ==========================================================
# Get new OAuth Access Token using Refresh Token
# ==========================================================
def get_access_token():
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64_credentials()
    }
    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ eBay Token Refresh Failed:", response.text)
        return None

EBAY_ACCESS_TOKEN = get_access_token()
