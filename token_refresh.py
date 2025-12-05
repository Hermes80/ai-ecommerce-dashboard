import time
import base64
import requests
from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_REFRESH_TOKEN,
    EBAY_REDIRECT_URI,
    EBAY_OAUTH_URL
)

# -------------------------
# Build Basic Auth Header
# -------------------------
def get_basic_auth_header():
    pair = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(pair.encode()).decode()


# -------------------------
# Refresh Token Function
# -------------------------
def refresh_access_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {get_basic_auth_header()}"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    print("🔄 Refreshing eBay token…")

    r = requests.post(EBAY_OAUTH_URL, headers=headers, data=data)

    if r.status_code != 200:
        print("❌ Token refresh failed:", r.text)
        return None

    result = r.json()
    new_access = result.get("access_token")

    if new_access:
        print("✅ Token refreshed successfully")

        # Write new access token to config.py
        update_config(new_access)

    return new_access


# -------------------------
# Write new token into config.py
# -------------------------
def update_config(new_access_token):
    path = "/home/ubuntu/ai-ecommerce-dashboard/config.py"

    with open(path, "r") as f:
        lines = f.readlines()

    with open(path, "w") as f:
        for line in lines:
            if line.startswith("EBAY_ACCESS_TOKEN"):
                f.write(f'EBAY_ACCESS_TOKEN = "{new_access_token}"\n')
            else:
                f.write(line)

    print("💾 config.py updated with new token")


# -------------------------
# Automatic Refresh Loop (forever)
# -------------------------
if __name__ == "__main__":
    while True:
        refresh_access_token()
        print("⏳ Sleeping 45 minutes...\n")
        time.sleep(45 * 60)
