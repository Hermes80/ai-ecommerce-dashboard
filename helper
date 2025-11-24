import base64
from config import EBAY_APP_ID, EBAY_CERT_ID

def base64_credentials():
    raw = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(raw.encode()).decode()
