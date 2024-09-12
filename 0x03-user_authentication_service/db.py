#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from typing import TypeVar
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds user to the database

        Args:
            email (str): the user email
            hashed_password: the hashed user password

        Returns:
            The created user
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self.save(new_user)
            self.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        # return the newly created user object
        return new_user

    # save user to database
    def save(self, instance):
        """saves instance to the session

        Args:
            instance (obj): instance to save
        """
        self._session.add(instance)

    def commit(self):
        """commit chanes to the database
        """
        self._session.commit()

    def find_user_by(self, **kwargs):
        """Takes arbitrary keyword arguments

        Returns:
            The first row found in the users table
            as filtered by the method's input arguments
        """
        if not kwargs:
            raise InvalidRequestError
        
        user_found = self._session.query(User).filter_by(**kwargs).first()

        if user_found:
            return user_found
        else:
            raise NoResultFound
        
