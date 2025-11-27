"""
Central config for eBay + AI dashboard.
Fill in ACCESS and REFRESH tokens from your successful curl response.
"""

# ====== eBay APP CREDENTIALS (PRODUCTION) ======
# These are from your eBay Developer "Production" keys page.
EBAY_APP_ID = "Christop-Storepil-PRD-86e535c40-6a1b1745"      # Client ID
EBAY_CERT_ID = "PRD-6e535c40ab78-bae2-470b-a92c-6cb7"         # Client Secret
EBAY_REDIRECT_URI = "Christopher_Sau-Christop-Storep-fgsznw"  # RuName

# ====== eBay ENDPOINTS ======
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_REST_URL = "https://api.ebay.com"

# ====== TOKENS (FILL THESE FROM YOUR CURL RESPONSE) ======
# From the *successful* curl you just ran:
#   "access_token": "v^1.1#i^1#f^0#I^3#r^0#p^3#t^H4sIAAAAAAAA/..."
#   "refresh_token": "v^1.1#i^1#p^3#f^0#I^3#r^1#t^Ul4xMF85OkU3RDI1..."

EBAY_ACCESS_TOKEN = "v^1.1#i^1#f^0#I^3#r^0#p^3#t^H4sIAAAAAAAA/..."
EBAY_REFRESH_TOKEN = "v^1.1#i^1#p^3#f^0#I^3#r^1#t^Ul4xMF85OkU3RDI1..."
# (Keep the full token strings exactly as returned by eBay, inside quotes)
