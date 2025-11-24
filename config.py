import os
from dotenv import load_dotenv

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_REST_URL = "https://api.ebay.com"
