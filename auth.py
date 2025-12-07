import bcrypt
import jwt
import datetime
from flask import Blueprint, request, jsonify
from models import SessionLocal, User

auth_bp = Blueprint("auth", __name__)
SECRET = "CHANGE_THIS_TO_A_LONG_RANDOM_KEY"

def generate_token(user_id):
    return jwt.encode(
        {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)},
        SECRET,
        algorithm="HS256"
    )

@auth_bp.route("/register", methods=["POST"])
def register():
    db = SessionLocal()
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if db.query(User).filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User(email=email, password_hash=hashed.decode())
    db.add(new_user)
    db.commit()

    return jsonify({"message": "User created"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    db = SessionLocal()
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)
    return jsonify({"token": token}), 200
