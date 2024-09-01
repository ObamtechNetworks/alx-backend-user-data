#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """Hashes a password

    Args:
        password (str): Password string to hash

    Returns:
        ByteString: Returns a salted hashed password byte string
    """
    password_to_bytes = password.encode()
    hash_passwd = bcrypt.hashpw(password_to_bytes, bcrypt.gensalt())
    return hash_passwd
