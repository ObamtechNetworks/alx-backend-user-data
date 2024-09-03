#!/usr/bin/env python3
"""Auth Class to Manage Basic Authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth Class for basic authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that defines path tha requires authentication

        Args:
            path (str): path that require authentication
            excluded_paths (List[str]): Paths that are excluded

        Returns:
            bool: Returns a boolean
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Manages authrization header

        Args:
            request (object, optional): http request object. Defaults to None.

        Returns:
            str: returns the authorization header as string
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user session

        Args:
            request (object, optional): http request objet. Defaults to None.

        Returns:
            User: returns the user object
        """
        return None
