#!/usr/bin/env python3
"""Modeule for Basic authentication
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """FUnction Extracts the Base64 part of the header
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            fieldMatch = re.fullmatch(pattern, authorization_header.strip())
            if fieldMatch is not None:
                return fieldMatch.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """FUnction to Decodes a base64-encoded authorization header.
        """
        if type(base64_authorization_header) == str:
            try:
                resp = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return resp.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """FUnction Extracts user credentials from a base64-decoded authorization
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            fieldMatch = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if fieldMatch is not None:
                user = fieldMatch.group('user')
                password = fieldMatch.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Function Retrieves a user based on 
            the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Function Retrieves the user from a request.
        """
        authHeader = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(authHeader)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)