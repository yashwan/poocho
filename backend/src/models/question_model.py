from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class Questions(BaseModel):
    user_id: str = Field(...)
    question: str = Field(...)
    title: str = Field(...)
    topic_id: Optional[str] = None
    

class Question(Questions):
    _id: ObjectId = None