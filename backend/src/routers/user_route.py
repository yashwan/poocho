from fastapi import HTTPException
from src.decorators.logger_decorator import log_route
from src.models import LoginModel, UserModel
from ..controllers import user_controller
from fastapi import APIRouter, Request, responses, Response

router = APIRouter()

@router.post("/register")
@log_route
async def create_user(request:Request, usr: UserModel):
    request_body = await request.json()
    user = UserModel(**request_body)
    response = await user_controller.create_user(user)
    return responses.JSONResponse(content=response,status_code=201)

@router.post("/login")
@log_route
async def login_user(request:Request, login: LoginModel, response: Response):
    request_body = await request.json()
    user = LoginModel(**request_body)
    controller_response = await user_controller.login_user(user)
    response.headers["Authorization"] = f'Bearer {controller_response["token"]["access_token"]}'
    response.set_cookie(
        key="Authorization",
        value=f'Bearer {controller_response["token"]["access_token"]}',
        expires=900
        )
    response.status_code = 200
    return controller_response

@router.get("/{user_id}")
@log_route
async def get_user(request:Request, user_id:str):
    user_id = request.path_params["user_id"]
    if not user_id:
        raise HTTPException(status_code=400, detail={
            "message": "User ID is required",
            "error": True
        })
    if user_id != request.state.user["sub"]:
        raise HTTPException(status_code=403, detail={
            "message": "Forbidden",
            "error": True
        })
    response = await user_controller.get_user(user_id)
    return response

@router.post("/token-refresh/{id}")
async def token_refresh(request: Request):
    user_id: str = request.path_params["id"]
    if not user_id:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "User Not Found"
            }
        )
    response = await user_controller.refresh_token(user_id)
    http_response = responses.JSONResponse(
        status_code=200,
        content={
            "message":"tokens updated successfully",
            "error": False,
            "success": True,
            "data": {
                **response
            }
        }
    )

    access_token = response["token"]["access_token"]
    http_response.set_cookie("Authorization", f"Bearer {access_token}")
    http_response.headers["Authorization"] = f'Bearer {access_token}'
    return http_response

@router.post("/logout/{id}")
async def logout(req: Request, res: Response):
    print("routr")
    user_id = req.path_params["id"]
    payload = req.state.user
    if not user_id:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "user not found",
                "error": True
            }
        )
    if user_id != payload["sub"]:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Forbidden",
                "error": True
            }
        )
    res.delete_cookie("token")
    res.status_code = 204
    return res

    