import base64
import requests
from config import EBAY_APP_ID, EBAY_CERT_ID, EBAY_REDIRECT_URI

def get_auth_header():
    raw = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    encoded = base64.b64encode(raw.encode()).decode()
    return encoded

def exchange_code_for_token(auth_code):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {get_auth_header()}"
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": EBAY_REDIRECT_URI
    }

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers,
        data=data
    )

    print("\n🔍 eBay API Response:")
    print(response.text)
    return response.json()

if __name__ == "__main__":
    AUTH_CODE = "v^1.1#i^1#f^0#r^1#p^3#I^3#t^Ul41XzEwOjFCMUY1NjA5REJDOTM5ODQyODVERjM3Q0Y4QUFGQ0UwXzBfMSNFXjI2MA=="
    exchange_code_for_token(AUTH_CODE)
