from pydantic import BaseModel, EmailStr
from src.models.base import Document

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserInDb(UserBase, Document):
    hashed_password: str
    salt: str
      