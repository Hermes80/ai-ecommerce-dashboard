from dotenv import load_dotenv
import os

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID")
EBAY_REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI")


# These are optional but recommended
EBAY_SCOPE = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory"
