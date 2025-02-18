import jwt
from fastapi import HTTPException
from src.utils.logger import logger

from .token_service import create_token, decode_token
from ..utils.collections import user_collection
from ..models import LoginModel, UserModel
from bson import ObjectId

class UserService:
    def __init__(self):
        self.user_collection = user_collection
    
    async def is_email_exist(self, email):
        email = await self.user_collection.find_one({"email": email})
        return True if email else False 

    async def create_user(self, user: UserModel):
        if await self.is_email_exist(user.email):
            raise HTTPException(status_code=400, detail="Email already exist")
        user_dict = user.model_dump()
        id = await self.user_collection.insert_one(user_dict)
        user_dict["_id"] = str(id.inserted_id)
        token_encode = create_token({
            "sub": user_dict["_id"]
        })
        user_dict["token"] = token_encode
        return user_dict
    
    async def get_user(self, user_id):
        try:
            id = ObjectId(user_id)
            user = await self.user_collection.find_one({"_id": id})
            if user:
                return user
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def login_user(self, user: LoginModel):
        user__dict = await self.user_collection.find_one({
            "email": user.email
        }, {"password": 1, "email": 1, "_id": 1})
        if not user__dict:
            raise HTTPException(status_code=404, detail="User not found")
        is_password_match = user.compare_password(user__dict.get("password"))
        if not is_password_match:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        _id = user__dict["_id"]
        user__dict["_id"] = str(user__dict["_id"])
        token_encode = create_token({
            "sub": user__dict["_id"]
        })
        await self.user_collection.update_one({
            "email": user.email
        }, {
            "$set":{
                "refreshToken": token_encode["refresh_token"]
            }
        })
        user__dict["token"] = token_encode
        return user__dict
    
    async def refresh_token(self, user_id):
        logger.info("Service")
        try:
            token = await self.user_collection.find_one({
            "_id": ObjectId(user_id)
            }, {
                "refreshToken": 1
            })
            token = token["refreshToken"]
            if not token:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "message": "User not found",
                        "error": True
                    }
                )
            
            verify_token = decode_token(token=token)
            if verify_token["sub"] != user_id:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "Message": "forbidden",
                        "error": True
                    }
                )
            generate_token = create_token({
                "sub": user_id
            })
            await self.user_collection.update_one({
                "_id": ObjectId(user_id)
            }, {
                "$set":{
                    "refreshToken": generate_token["refresh_token"]
                }
            })
            return {
                "token": generate_token
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

