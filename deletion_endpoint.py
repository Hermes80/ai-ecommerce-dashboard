import hashlib
from flask import Blueprint, request, jsonify

deletion_bp = Blueprint('deletion_bp', __name__)

# Your exact settings — MUST MATCH eBay portal
ENDPOINT_URL = "https://storepilot.online/deletion"
VERIFICATION_TOKEN = "YOUR_VERIFICATION_TOKEN"

@deletion_bp.route("/deletion", methods=["GET"])
def deletion_verification():
    challenge_code = request.args.get("challenge_code", "")

    if not challenge_code:
        return jsonify({"error": "challenge_code missing"}), 400

    # Concatenate EXACT order:
    # challengeCode + verificationToken + endpointURL
    raw_string = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL

    # Generate SHA-256
    hashed = hashlib.sha256(raw_string.encode()).hexdigest()

    return jsonify({"challengeResponse": hashed}), 200
