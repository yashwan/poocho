from .user_route import router as user_router
from .question_route import q_router
from fastapi import APIRouter
router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(q_router, prefix="/q", tags=["questions"])