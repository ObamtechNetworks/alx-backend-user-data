#!/usr/bin/env python3
"""Manages user authentication"""

import bcrypt


from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union

from db import DB
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

    def valid_login(self, email: str, password: str) -> bool:
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)

            if user:
                # Hash the provided password using bcrypt
                hash_pwd = str.encode(password)  # User-supplied password
                # Compare it with the stored hashed password (already bytes)
                if bcrypt.checkpw(hash_pwd, user.hashed_password):
                    return True
                else:
                    return False
            return False

        except Exception as e:
            # print(f"An error occurred: {str(e)}")
            return False

    def create_session(self, email: str) -> str:
        try:
            user = self._db.find_user_by(email=email)
            # if user is found,
            if user:
                # generate uuid
                session_id = _generate_uuid()
                # update user with id in the database with the session_id prop
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            return None
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Finds a user by sessionID

        Args:
            session_id (str): the session id to find

        Returns:
            User | None: returns the user or none
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None
        except Exception:
            return None


def _generate_uuid() -> str:
    """returns a string repr of a new UUID

    Returns:
        uuid: string reprensentation of a UUID
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hashes given password

    Args:
        password (str): given password to hash

    Returns:
        bytes: returns the password in bytes
    """
    password_to_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_to_bytes, salt=bcrypt.gensalt())
