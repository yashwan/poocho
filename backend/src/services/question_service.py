from fastapi import HTTPException
from backend.src.models import QuestionsModel, QuestionModel
from src.utils.collections import question_collection
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from bson import ObjectId
from enum import Enum

class QuestionEnum(Enum):
    TEN = 10
    TWENTY = 20


class QuestionService:
    question_collection: AsyncIOMotorCollection = question_collection

    async def Create(self, question: QuestionsModel):
        question = question.model_dump()
        question_response = await self.question_collection.insert_one({**question})
        question["_id"] = str(question_response.inserted_id)
        return question
    
    async def get_question(self, skip=0, limit:QuestionEnum = QuestionEnum.TEN)-> List[QuestionModel]:
        response = await self.question_collection.find({}).skip(skip=skip).limit(limit=limit)
        return response
    
    async def get_question_by_id(self, qid:str):
        resp = await self.question_collection.find_one({
            "_id": ObjectId(qid)
        })
        return resp
    
    async def update_by_id(self, qid:str):
        find_question: QuestionModel = await self.get_question_by_id(qid=qid)
        if not find_question:
            raise HTTPException(
                status_code=404,
                detail= "Question not found"
            )
        resp = await self.question_collection.update_one({
            "_id": ObjectId(qid)
        }, {
            "$set": {
                "question": find_question.question
            }
        })
        return resp