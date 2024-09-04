#!/usr/bin/env python3
"""Setup the basic authentication classs
inherits from Auth class
"""
from api.v1.auth.auth import Auth
import base64

"""Basic authentication module"""


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
