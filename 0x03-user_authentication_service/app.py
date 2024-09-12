#!/usr/bin/env python3
""" A simple flask app"""
from flask import (jsonify, Flask, request,
                   abort, make_response, redirect, url_for)
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


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """responds to the sessions route
    """
    email = request.form.get('email')
    # Validation
    if not email:
        abort(401)
    password = request.form.get('password')
    if not password:
        abort(401)

    if AUTH.valid_login(email, password):
        user_session = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", user_session)
        return resp
    abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Logs out a user via session"""
    user_session = request.session_id
    user = AUTH.get_user_from_session_id(user_session)

    if user:
        AUTH.destroy_session(user.id)
        redirect(url_for('index'))
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
