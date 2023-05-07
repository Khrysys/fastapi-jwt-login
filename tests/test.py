from fastapi import FastAPI, Request, Depends, Response
from fastapi_jwt_login import JWTLogin
import os
from uvicorn import Config, Server
from json import dumps

data = {
    'username': '',
    'password_hash': '',
    'email': '',
}

app = FastAPI()
jwt = JWTLogin(os.urandom(24).hex())

@app.route('/jwt')
def jwt_route(request: Request = Depends()):
    response = Response()
    jwt.set_token_header(response, data)
    return response

@app.route('/protected')
def protected(request: Request = Depends()):
    data = jwt.get_jwt_in_cookies(request)
    return Response(dumps(data))

Server(Config(app)).run()