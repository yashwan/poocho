from fastapi import responses

def error_handler(e):
        if hasattr(e, "status_code"):
            return responses.JSONResponse(status_code=e.status_code, content=e.detail)
        return responses.JSONResponse(status_code=500, content={
            "message": "Internal Server Error",
            "error": True
        })