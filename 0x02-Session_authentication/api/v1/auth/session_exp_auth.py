#!/usr/bin/env python3
"""Module Session authentication with expiration 
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration.
    """

    def __init__(self) -> None:
        """Initializes a new SessionExpAuth instance.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Function Creates a session id for the user.
        """
        sessionid = super().create_session(user_id)
        if type(sessionid) != str:
            return None
        self.user_id_by_session_id[sessionid] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return sessionid

    def user_id_for_session_id(self, session_id=None) -> str:
        """Function Retrieves the user id of the user
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            curtime = datetime.now()
            timespan = timedelta(seconds=self.session_duration)
            exptime = session_dict['created_at'] + timespan
            if exptime < curtime:
                return None
            return session_dict['user_id']
