import requests
from config import EBAY_REFRESH_TOKEN, EBAY_OAUTH_URL
from helper import base64_credentials

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

    if response.status_code != 200:
        print("ERROR GETTING ACCESS TOKEN:", response.text)

    return response.json().get("access_token")
