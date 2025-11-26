from flask import Flask, request, jsonify
import hashlib

# ===========================
# YOUR VERIFICATION TOKEN
# ===========================
VERIFICATION_TOKEN = "hermes08_verification_token_1234567890_ABCDEF"

# ===========================
# YOUR HTTPS ENDPOINT URL
# Must EXACTLY match what you gave eBay
# ===========================
ENDPOINT_URL="Www.storepilot.online" 

app = Flask(__name__)

# ===========================
# HASHING HELPER
# ===========================
def compute_challenge_response(challenge_code):
    """
    eBay requires SHA256( challengeCode + verificationToken + endpointURL )
    """
    combined = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

# ===========================
# ENDPOINT ROUTE
# ===========================
@app.route("/deletion", methods=["GET", "POST"])
def deletion_handler():
    # Step 1 — eBay validation GET challenge
    challenge_code = request.args.get("challenge_code")
    if challenge_code:
        print(f"Received challenge_code: {challenge_code}")
        response = compute_challenge_response(challenge_code)
        return jsonify({"challengeResponse": response}), 200

    # Step 2 — Actual deletion notifications (POST)
    print("Received deletion notification:", request.json)
    return jsonify({"status": "received"}), 200

# ===========================
# RUN STANDALONE FOR TESTING
# ===========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
