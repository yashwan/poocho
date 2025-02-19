import datetime
from fastapi import HTTPException
from src.models import QuestionsModel, QuestionModel
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
        question = QuestionsModel(**question).model_dump()
        question_response = await self.question_collection.insert_one({**question, "created_at": datetime.datetime.utcnow(), "updated_at": datetime.datetime.utcnow()})
        question["_id"] = str(question_response.inserted_id)
        return question
    
    async def get_question(self, skip=0, limit:QuestionEnum = QuestionEnum.TEN.value, key=-1)-> List[QuestionModel]:
        all_q = await self.question_collection.count_documents({})
        response = await self.question_collection.find({}).sort({"updated_at": key}).skip(skip=skip).limit(limit=limit).to_list(length=None)
        for doc in response:
            doc["_id"] = str(doc["_id"])
        return {
            "data": response
            , "count": all_q}
    
    async def get_question_by_id(self, qid:str) -> QuestionModel:
        resp = await self.question_collection.find_one({
            "_id": ObjectId(qid)
        })
        resp["_id"] = str(resp["_id"])
        return resp
    
    async def update_by_id(self, qid:str, question:str) -> QuestionModel:
        find_question: QuestionModel = await self.get_question_by_id(qid=qid)
        if not find_question:
            raise HTTPException(
                status_code=404,
                detail= "Question not found"
            )

        await self.question_collection.update_one({
            "_id": ObjectId(qid)
        }, {
            "$set": {
                "question": question,
                "updated_at": datetime.datetime.utcnow()
            }
        })
        resp = await self.question_collection.find_one({"_id": ObjectId(qid)})
        resp["_id"] = str(resp["_id"])
        return resp
    
    async def delete_by_id(self, qid: str):
        qid = ObjectId(qid)
        find_question = await self.question_collection.find_one({
            "_id": qid
        })
        if not find_question:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Question Not Found",
                    "success": False,
                }
            )
        await self.question_collection.delete_one({
            "_id":qid
        })
        return {
            "message": "Question Deleted successfully",
            "success": True
        }