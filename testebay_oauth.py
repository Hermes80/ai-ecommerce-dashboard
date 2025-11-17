from config import EBAY_APP_ID, EBAY_CERT_ID, EBAY_REDIRECT_URI
import requests
import base64

print("Testing eBay OAuth connection...\n")

creds = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
auth_header = base64.b64encode(creds.encode()).decode()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {auth_header}"
}

data = {
    "grant_type": "client_credentials",
    "redirect_uri": EBAY_REDIRECT_URI,
    "scope": "https://api.ebay.com/oauth/api_scope"
}

response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
