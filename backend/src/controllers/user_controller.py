from fastapi import HTTPException
from ..services import user_service


class UserController:
    user_service = user_service

    async def create_user(self, user):
        try:
            user = await self.user_service.create_user(user)
            return user
        except Exception as e:
            raise HTTPException(status_code=e.status_code, detail={
                "message": e.detail,
                "error": True
            })


    # @log_route
    async def get_user(self, user_id):
        try:
            user = await self.user_service.get_user(user_id)
            user["_id"] = str(user["_id"])
            return user
        except Exception as e:
            print(e, "controller")
            raise HTTPException(status_code=e.status_code, detail={
                "message": e.detail,
                "error": True
            })
    
    async def login_user(self, user):
        user_response = await self.user_service.login_user(user)
        return user_response
    
    async def refresh_token(self, user_id):
        print("Controller")
        response = await self.user_service.refresh_token(user_id)
        return response
