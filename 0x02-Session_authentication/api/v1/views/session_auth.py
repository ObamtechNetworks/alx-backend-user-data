#!/usr/bin/env python3
""" Module for session views
"""
import os
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_authentication():
    """Authenticates a user session."""

    # Retrieve email and password from request
    user_email = request.form.get('email')
    if not user_email or user_email == '':
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get('password')
    if not user_pwd or user_pwd == '':
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    users = User.search({'email': user_email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Since search returns a list, we take the first user

    # Validate the password
    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    # Create a session for the user
    # Import only where necessary to avoid circular imports
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Return user data and set the session cookie
    response = jsonify(user.to_json())
    # Get the session name from environment variable
    cookie_data = os.getenv("SESSION_NAME")
    response.set_cookie(cookie_data, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Handles the user logout"""
    # Attempt to destroy the session using auth.destroy_session
    if not auth.destroy_session(request):
        # If destroy_session returns False, abort with a 404 error
        abort(404)

    # If successful, return an empty JSON dictionary with a 200 status code
    return jsonify({}), 200
