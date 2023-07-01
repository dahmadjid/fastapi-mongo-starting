from fastapi import status
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.json import ENCODERS_BY_TYPE
import json
class HTTPBaseException(Exception):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unexpected server error"


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    
       
class PyObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return PyObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


ENCODERS_BY_TYPE[
    PyObjectId
] = str  # it is a workaround to force pydantic make json schema for this field

         
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        print("ak temshi")
        if isinstance(o, PyObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
    
class Document(BaseModel):
    """
    A class you can inherit from to add ObjectID to its model. 
    handles messy stuff like alias _id and other stuff i dont really understand.
    copied from internet
    https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    def dict(self, **kwargs):
        kwargs.update({"by_alias": True})
        return super().dict(**kwargs)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class Token(BaseModel):
    access_token: str


class TokenData(Document):
    """Inherits Document to add id to its schema"""
    username: str | None = None


