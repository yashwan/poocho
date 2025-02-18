import datetime
from ..configs import config
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


schema = OAuth2PasswordBearer(tokenUrl="token")
def create_token(data: dict) -> str:
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    access_token = jwt.encode(algorithm="HS256", key=config["JWT_SECRET_KEY"], payload=data)
    data["exp"] = datetime.datetime.now() + datetime.timedelta(days=15)
    refresh_token = jwt.encode(algorithm="HS256", key=config["JWT_SECRET_KEY"], payload=data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

def decode_token(token: str = Depends(schema)) -> dict:
    return jwt.decode(token, key=config["JWT_SECRET_KEY"], algorithms=["HS256"])