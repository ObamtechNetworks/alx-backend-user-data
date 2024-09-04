#!/usr/bin/env python3
"""Setup the basic authentication classs
inherits from Auth class
"""
from typing import TypeVar
import base64
from api.v1.auth.auth import Auth
from models.base import DATA
from models.user import User


class BasicAuth(Auth):
    """Class for implementing basic authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns a base64 part of the Authorization header
        for Basic Authentication

        Args:
            authorization_header (str): The authorization header

        Returns:
            str: The authorization header string
        """
        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        # Otherwise, return the value after Basic (after the space)
        return authorization_header.split('Basic ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decodes a base64 authorization header string

        Args:
            base64_authorization_header (str): the authorization str
            from header

        Returns:
            str: the decoded string
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header,
                                             validate=True)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extracts users credentials,
        email and password from base64 decoded value

        Args:
            decoded_base64_authorization_header(str):
            the decoded authorization header to extract credentials from

        Returns:
            A tuple of str, email and password
        """
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd:
                                     str) -> TypeVar('User'):
        """Returns the user instace based on his email and password

        Args:
            user_email (str): The user email address
            user_pwd (str): the user password

        Returns:
            User (class): The User Object
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # check database file
        if DATA is not None:
            user_list = User.search({"email": user_email})
            if user_list:
                # Assuming emails are unique, get the first match
                user = user_list[0]
                # check if the password is correct
                if user.is_valid_password(user_pwd):
                    return user
        # Return None if any check fails
        return None
