import requests, base64, json, time
from config import EBAY_APP_ID, EBAY_CERT_ID, EBAY_REFRESH_TOKEN, EBAY_OAUTH_URL

def refresh_token():
    auth = base64.b64encode(f"{EBAY_APP_ID}:{EBAY_CERT_ID}".encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth}"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    r = requests.post(EBAY_OAUTH_URL, headers=headers, data=data).json()

    if "access_token" in r:
        with open("tokens/token.json", "w") as f:
            json.dump(r, f)
        print("🔄 New token saved.")
        return r["access_token"]
    else:
        print("❌ Token refresh failed:", r)
        return None
