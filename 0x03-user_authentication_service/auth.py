#!/usr/bin/env python3
"""Manages user authentication"""

import bcrypt


from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user to the database

        Args:
            email (str): user email
            password (str): user password

        Returns:
            User: return the registered user
        """
        # check if user with email exists
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # hash the passwrod
            hashed_pwd = _hash_password(password)
            # create the user with details
            user = User(email=email, hashed_password=hashed_pwd)
            # save user to the db
            self._db.save(user)
            # commit changes to the databases
            self._db.commit()
            # return user
            return user
        except InvalidRequestError:
            raise ValueError("email and password is required")


def _hash_password(password: str) -> bytes:
    """Hashes given password

    Args:
        password (str): given password to hash

    Returns:
        bytes: returns the password in bytes
    """
    password_to_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_to_bytes, salt=bcrypt.gensalt())
