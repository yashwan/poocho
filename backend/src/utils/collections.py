from .mongodb import db

user_collection = db["users"]
question_collection = db["questions"]
answer_collection = db["answers"]