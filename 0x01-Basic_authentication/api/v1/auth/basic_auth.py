#!/usr/bin/env python3
"""Setup the basic authentication classs
inherits from Auth class
"""
from api.v1.auth.auth import Auth

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
