#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password

    Args:
        password (str): Password string to hash

    Returns:
        ByteString: Returns a salted hashed password byte string
    """
    password_to_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()  # automatically generate salt
    hash_passwd = bcrypt.hashpw(password_to_bytes, salt)
    return hash_passwd
