from fastapi import Request, responses
from starlette.middleware.base import BaseHTTPMiddleware

from src.decorators.logger_decorator import log_route


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
                print(e)
                if hasattr(e, "status_code"):
                    return responses.JSONResponse(status_code=e.status_code, content={
                         "message": e.detail,
                         "error": True
                    })
                return responses.JSONResponse(status_code=500, content={
                    "message": "Internal Server Error",
                    "error": True,
                    "debugMessage": str(e)
                })