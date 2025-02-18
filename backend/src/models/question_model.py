from pydantic import BaseModel, Field
from bson import ObjectId

class Questions(BaseModel):
    user_id: str = Field(...)
    question: str = Field(...)

class Question(Questions):
    _id: ObjectId = None