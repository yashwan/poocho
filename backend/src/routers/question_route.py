from src.decorators.logger_decorator import log_route
from src.controllers import question_controller
from fastapi import APIRouter, Request, Response, HTTPException
q_router = APIRouter()



@q_router.get("/")
@log_route
async def get_all_questions(request:Request, res: Response):
    skip = request.query_params.get("skip")
    skip = int(skip) if skip else 0
    limit = request.query_params.get("limit")
    limit = int(limit) if limit else 10
    s_param = int(request.query_params.get('asc', -1))
    if s_param > 1 or s_param == 0 or s_param < -1:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "sort param is not valid, sort must be in 0 or 1 or -1"
            }
        )
    response = await question_controller.get_questions(skip=skip, limit=limit, s_param=s_param)
    res.status_code = 200
    return response

@q_router.get("/{id}")
@log_route
async def get_question_by_id(request:Request, res: Response):
    qid = request.path_params["id"]
    if not qid:
        raise HTTPException(
            status_code=200,
            detail={
                "message": "quesiton not found",
                "success": True
            }
        )
    resp = await question_controller.get_questions(qid)
    res.status_code = 200
    return resp

@q_router.post("/")
@log_route
async def create_question(request:Request, res: Response):
    data = await request.json()
    resp = await question_controller.create_question(data)
    res.status_code = 201
    return resp

@q_router.put("/{id}")
@log_route
async def update_question(request:Request, res: Response):
    qid = request.path_params.get("id")
    data = await request.json()
    user_id = data.get("user_id")
    sub = request.state.user.get("sub")
    if sub != user_id:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "forbidden",
                "error": True
            }
        )
    question = data.get("question")
    response_obj = await question_controller.update_questions(qid, question=question)
    res.status_code = 200
    return response_obj

@q_router.delete("/{id}")
@log_route
async def delete_question(request:Request, res: Response):
    qid = request.path_params.id
    resp = question_controller.delete_question(qid)
    res.status_code = 204
    return resp
