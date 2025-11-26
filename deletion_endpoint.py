from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Your verification token (must be in quotes!)
VERIFICATION_TOKEN = "hermes08_verification_token_1234567890_ABCDEF"

# Your full HTTPS endpoint URL  
# Replace with your real domain once SSL is active
ENDPOINT_URL = "https://storepilot.online"

@app.route("/deletion", methods=["GET"])
def verify_endpoint():
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return jsonify({"error": "Missing challenge_code"}), 400

    # Hash: challengeCode + verificationToken + endpoint URL
    combined = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
    challenge_response = hashlib.sha256(combined.encode()).hexdigest()

    return jsonify({"challengeResponse": challenge_response}), 200


@app.route("/deletion", methods=["POST"])
def receive_deletion_notification():
    data = request.json
    print("Received deletion notification:", data)
    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
