import time
import base64
import requests
from typing import Any, Dict, List, Optional

from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_OAUTH_URL,
    EBAY_REST_URL,
    EBAY_REFRESH_TOKEN,
)

# --------------------------------------------------------------------
# TOKEN MANAGEMENT
# --------------------------------------------------------------------

_access_token: Optional[str] = None
_access_token_expires_at: float = 0.0  # epoch seconds


def _base64_credentials() -> str:
    """
    Build Base64(<client_id>:<client_secret>) for OAuth Authorization header.
    """
    creds = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(creds.encode("utf-8")).decode("utf-8")


def get_access_token() -> str:
    """
    Get a valid OAuth access token using the long-lived refresh token.

    - Reuses a cached token until it is close to expiring.
    - If expired/missing, calls eBay OAuth endpoint with grant_type=refresh_token.
    """
    global _access_token, _access_token_expires_at

    now = time.time()
    # If we already have a token and it expires in > 60 seconds, reuse it
    if _access_token and now < _access_token_expires_at - 60:
        return _access_token

    if not EBAY_REFRESH_TOKEN:
        raise RuntimeError(
            "EBAY_REFRESH_TOKEN is not set. Put it in your .env file as EBAY_REFRESH_TOKEN="
        )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {_base64_credentials()}",
    }

    # Scopes can be adjusted; using generic selling scope as example
    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope",
    }

    resp = requests.post(EBAY_OAUTH_URL, headers=headers, data=data, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to refresh eBay access token. Status={resp.status_code}, Body={resp.text}"
        )

    payload = resp.json()
    token = payload.get("access_token")
    expires_in = payload.get("expires_in", 3600)

    if not token:
        raise RuntimeError(
            f"Did not receive access_token from eBay OAuth. Response={payload}"
        )

    _access_token = token
    _access_token_expires_at = now + int(expires_in)
    return _access_token


# --------------------------------------------------------------------
# LOW-LEVEL HTTP HELPERS
# --------------------------------------------------------------------

def _auth_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Build Authorization header + optional extras.
    """
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if extra:
        headers.update(extra)
    return headers


def ebay_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Generic GET helper for eBay REST APIs.
    `path` should start with '/sell/...' or '/buy/...'
    """
    url = EBAY_REST_URL.rstrip("/") + path
    resp = requests.get(url, headers=_auth_headers(), params=params, timeout=30)
    # Raise for non-2xx to surface problems quickly
    if not resp.ok:
        raise RuntimeError(
            f"eBay GET {url} failed. Status={resp.status_code}, Body={resp.text}"
        )
    try:
        return resp.json()
    except ValueError:
        return {}


def ebay_post(
    path: str, body: Dict[str, Any], params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generic POST helper.
    """
    url = EBAY_REST_URL.rstrip("/") + path
    resp = requests.post(
        url, headers=_auth_headers(), json=body, params=params, timeout=30
    )
    if not resp.ok:
        raise RuntimeError(
            f"eBay POST {url} failed. Status={resp.status_code}, Body={resp.text}"
        )
    try:
        return resp.json()
    except ValueError:
        return {}


# --------------------------------------------------------------------
# HIGH-LEVEL HELPERS USED BY YOUR APP
# --------------------------------------------------------------------

def get_active_listings(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Example: Fetch active offers via the Sell Inventory API.
    Adjust endpoint/params depending on your actual design.
    """
    # /sell/inventory/v1/offer?limit=...
    data = ebay_get("/sell/inventory/v1/offer", params={"limit": limit})
    offers = data.get("offers", [])
    return offers


def get_orders(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Example: Fetch recent orders via the Sell Fulfillment API.
    """
    # /sell/fulfillment/v1/order?limit=...
    data = ebay_get("/sell/fulfillment/v1/order", params={"limit": limit})
    orders = data.get("orders", [])
    return orders
