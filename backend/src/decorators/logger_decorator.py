from functools import wraps
from fastapi import Request
from src.utils.logger import logger


def log_route(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        logger.info(f"Request: {request.method} {request.url}")
        response = await func(*args, **kwargs)
        logger.info(f"Response: {response}")
        return response
    return wrapper
