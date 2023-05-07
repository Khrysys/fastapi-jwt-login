import typing as t
from random import choice
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response
from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from jose import jwt
from datetime import timedelta

class JWTLogin:
    def __init__(self, secret_key: str, cookie_name: str = 'x-jwt-login-token', algorithm: str = 'HS256'):
        self.cookie_name = cookie_name
        self.secret = secret_key
        self.algorithm = algorithm
        
    def set_token_header(self, response: Response, data: dict[str, t.Any]):
        if data is not None:
            encoded_token = jwt.encode(data, self.secret, self.algorithm)
            response.set_cookie(self.cookie_name, encoded_token, httponly=True, expires=timedelta(days=90))
        else:
            response.set_cookie(self.cookie_name, '', expires=timedelta(seconds=1))
        
    def get_jwt_in_cookies(self, request: Request):
        cookie = request.cookies.get(self.cookie_name)
        return jwt.decode(cookie, self.secret, self.algorithm)