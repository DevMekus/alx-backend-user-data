#!/usr/bin/env python3
"""Module for Session authentication
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Function Creates a session id for the user.
        """
        if type(user_id) is str:
            sessionid = str(uuid4())
            self.user_id_by_session_id[sessionid] = user_id
            return sessionid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """function to Retrieves the user id 
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Function Retrieves the user 
        associated with the request.
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Function Destroys an authenticated session.
        """
        sessionid = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sessionid)
        if (request is None or sessionid is None) or user_id is None:
            return False
        if sessionid in self.user_id_by_session_id:
            del self.user_id_by_session_id[sessionid]
        return True