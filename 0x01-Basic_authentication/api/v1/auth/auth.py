#!/usr/bin/env python3
"""Module for Authentication.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method Checks if a 
            path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for exclusionPath in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusionPath[-1] == '*':
                    pattern = '{}.*'.format(exclusionPath[0:-1])
                elif exclusionPath[-1] == '/':
                    pattern = '{}/*'.format(exclusionPath[0:-1])
                else:
                    pattern = '{}/*'.format(exclusionPath)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method Gets the authorization 
            header field.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method Gets the current 
            user from the request.
        """
        return None