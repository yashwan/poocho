from dataclasses import dataclass
from src.services import question_service

@dataclass
class QuestionController:
    service = question_service

    async def create_question(self, data):
        question = await self.service.Create(data)
        return question
    
    async def get_questions(self, id = None, skip=None, limit= None, s_param =None):
        questions = {}
        if id:
            questions = await self.service.get_question_by_id(id)
        else:
            if limit > 100:
                return {}
            questions = await self.service.get_question(skip=skip, limit=limit, key=s_param)
        return questions
    
    async def update_questions(self, id, question):
        question = await self.service.update_by_id(id, question=question)
        return question
    
    async def delete_question(self, id):
        question = self.service.delete_by_id(id)
        return question
