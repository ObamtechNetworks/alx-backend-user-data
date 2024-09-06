#!/usr/bin/env python3
"""Sessikon Authentication"""

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Base class for configuring session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id

        Args:
            user_id (str, optional): The user ID to create session for.
            Defaults to None.

        Returns:
            str: returns the session ID as a string
        """
        if not user_id or not isinstance(user_id, str):
            return None
        sessionId = str(uuid.uuid4())
        self.user_id_by_session_id[sessionId] = user_id
        return sessionId
