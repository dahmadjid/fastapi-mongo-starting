from src.config import settings
from fastapi import status
from motor import motor_asyncio
import asyncio
from pydantic import MongoDsn
from src.models.users import UserBase, UserInDb
from src.models.base import PyObjectId, HTTPBaseException

class UsersCollection:
    coll: motor_asyncio.AsyncIOMotorCollection
    
    class UserNotFound(HTTPBaseException):
        code = status.HTTP_404_NOT_FOUND
        message = "User not found"

    class UsernameAlreadyInUse(HTTPBaseException):
        code = status.HTTP_409_CONFLICT
        message = "Username already in use"

    class EmailAlreadyInUse(HTTPBaseException):
        code = status.HTTP_409_CONFLICT
        message = "Email address already in use"
    
    @staticmethod
    def init_dbconn():
        db_uri = MongoDsn.build(
            scheme="mongodb",
            user=settings.MONGO_USER,
            password=settings.MONGO_PASS,
            host="mongo_db",
            port="27017",
            path=f"/mongo_db?authSource=admin",
        )
        db_client = motor_asyncio.AsyncIOMotorClient(db_uri, io_loop=asyncio.get_running_loop())
        UsersCollection.coll = db_client["storage"]["users"]
    
    @staticmethod
    async def create(new_user: UserBase, hashed_password: str) -> UserInDb:
        user = UserInDb(
            hashed_password=hashed_password,
            **new_user.dict(),
        )
        user_document = await UsersCollection.coll.find_one({"email": new_user.email})
        if user_document:
            raise UsersCollection.EmailAlreadyInUse
        user_document = await UsersCollection.coll.find_one({"username": new_user.username})
        if user_document:
            raise UsersCollection.UsernameAlreadyInUse
        
        res = await UsersCollection.coll.insert_one(user.dict())
        user.id = res.inserted_id
        return user
    
    @staticmethod
    async def get(id: PyObjectId) -> UserInDb:
        user_document = await UsersCollection.coll.find_one({"_id": id})
        if user_document is None:
            raise UsersCollection.UserNotFound
        return UserInDb(**user_document)
    
    @staticmethod
    async def get_by_email(email: str) -> UserInDb:
        user_document = await UsersCollection.coll.find_one({"email": email})
        if user_document is None:
            raise UsersCollection.UserNotFound
        return UserInDb(**user_document)
    
    @staticmethod
    async def get_by_username(username: str) -> UserInDb:
        user_document = await UsersCollection.coll.find_one({"username": username})
        if user_document is None:
            raise UsersCollection.UserNotFound
        return UserInDb(**user_document)
    
    @staticmethod
    async def delete(id: PyObjectId) -> None:
        res = await UsersCollection.coll.delete_one({"_id": id})
        if not res.deleted_count:
            raise UsersCollection.UserNotFound        