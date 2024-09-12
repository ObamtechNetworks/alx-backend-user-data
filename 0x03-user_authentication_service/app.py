#!/usr/bin/env python3
""" A simple flask app"""
from flask import jsonify, Flask, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def index():
    """return the index page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """creates a user from the post request"""
    email = request.form.get('email')

    # Validation
    if not email:
        return jsonify({"error": "email is required!"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password is required"}), 400

    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
