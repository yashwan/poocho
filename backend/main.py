import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.utils.logger import logger
from src.middlewares.error_handler_middleware import ErrorHandlingMiddleware
from src.middlewares.auth_middleware import AuthMiddleware
from src.routers import router
from src.utils.mongodb import client



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

statuses = {
    "mongoDBConnection": False
}

async def connect():
    try:
        await client.server_info()
        statuses["mongodbConnection"] = True
        logger.info("DB Connected Successfully")
    except Exception as e:
        logger.error(f"DB Connection Unsuccessful {e}")
        return HTTPException(status_code=500, detail="Database connection failed")


@app.get("/status")
async def status() -> dict:
    return {
        "mongodbConnection": statuses["mongodbConnection"],
        "pid": os.getpid()
    }

app.add_middleware(AuthMiddleware)


app.include_router(router, prefix="/v1", tags=["v1"])
app.add_event_handler("startup", connect)


app.add_middleware(ErrorHandlingMiddleware)