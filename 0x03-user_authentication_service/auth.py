#!/usr/bin/env python3
"""Manages user authentication"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes given password

    Args:
        password (str): given password to hash

    Returns:
        bytes: returns the password in bytes
    """
    password_to_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_to_bytes, salt=bcrypt.gensalt())
