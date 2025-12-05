from flask import Flask, request, jsonify
import hashlib
import base64
from config import VERIFICATION_TOKEN

app = Flask(__name__)

ENDPOINT_URL = "https://storepilot.online/deletion"

@app.get("/deletion")
def verify():
    challenge = request.args.get("challenge_code")
    if not challenge:
        return "Missing challenge_code", 400

    raw = challenge + VERIFICATION_TOKEN + ENDPOINT_URL
    hashed = base64.b64encode(hashlib.sha256(raw.encode()).digest()).decode()

    return jsonify({"challengeResponse": hashed})
