import re
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from src.services.token_service import decode_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if((re.match(r"^/.*/user/.*", request.url.path) and request.method != "POST") or re.match(r"/user/logout/*", request.url.path) or re.match(r"^/.*/q/.*", request.url.path)):
            token = request.headers.get("Authorization") or request.cookies.get("Authorization")
            if token is None:
                raise HTTPException(status_code=401, detail="Unauthorized")
            try:
                token = token.split(" ")[1]
                payload = decode_token(token=token)
                request.state.user = payload
                print(payload)
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
        return await call_next(request)
