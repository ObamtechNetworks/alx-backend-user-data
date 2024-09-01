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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a provided password matches the hashed password

    Args:
        hashed_password (bytes): The hashed password
        password (str): password to validate

    Returns:
        bool: returns true or false
    """
    given_passwd_to_bytes = password.encode('utf-8')

    # check password
    result = bcrypt.checkpw(given_passwd_to_bytes, hashed_password)
    return result
