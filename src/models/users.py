from pydantic import BaseModel, EmailStr
from src.models.base import Document

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserPublic(UserBase, Document):
    pass

class UserInDb(UserPublic):
    hashed_password: str
      