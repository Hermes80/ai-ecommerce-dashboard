import base64
import requests
from config import EBAY_APP_ID, EBAY_CERT_ID, EBAY_REDIRECT_URI

def get_authorization_header():
    auth_string = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(auth_string.encode()).decode()

def exchange_code_for_token(authorization_code):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {get_authorization_header()}"
    }

    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": EBAY_REDIRECT_URI
    }

    response = requests.post("https://api.ebay.com/identity/v1/oauth2/token",
                             headers=headers, data=data)
    return response.json()

EBAY_APP_ID = "Christop-Storepil-PRD-86e535c40-6a1b1745"        # Client ID
EBAY_CERT_ID = "PRD-6e535c40ab78-bae2-470b-a92c-6cb7"           # Client Secret
EBAY_REDIRECT_URI = "Christopher_Sau-Christop-Storep-fgsznw"    # RuName

# OAuth URLs
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_REST_URL = "https://api.ebay.com"

# You will fill this AFTER token exchange succeeds
EBAY_REFRESH_TOKEN = ""
EBAY_ACCESS_TOKEN = ""
