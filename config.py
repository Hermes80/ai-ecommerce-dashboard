from dotenv import load_dotenv
import os

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID")
EBAY_REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI")

EBAY_OAUTH_URL = os.getenv("EBAY_OAUTH_URL", "https://api.ebay.com/identity/v1/oauth2/token")
EBAY_REST_URL = os.getenv("EBAY_REST_URL", "https://api.ebay.com")

# These are optional but recommended
EBAY_SCOPE = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory"
