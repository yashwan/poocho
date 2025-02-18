from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import bcrypt

class Login(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(min_length=8)

    def compare_password(self, password:str):
        return bcrypt.checkpw(self.password.encode('utf-8'), password.encode('utf-8'))

class User(Login):
    username: str = Field(...,min_length=3, max_length=50)
    bio: Optional[str] = Field(max_length=100)
    image: Optional[str] = None
    refreshToken: str = None

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, value: str):
        return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')