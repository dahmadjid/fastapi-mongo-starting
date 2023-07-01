from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from src.models.base import HTTPBaseException, TokenData, Token
from src.models.users import UserInDb
from src.config import settings
import bcrypt
import json

class Security:
    class Unauthorized(HTTPBaseException):
        code = status.HTTP_401_UNAUTHORIZED
        message = "Invalid Authorization Token"
        
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
    
    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return Security.pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return Security.pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_user_token(
        user: UserInDb,
    ) -> str:

        token_data = TokenData(
            id=str(user.id),
            username=user.username,
        )

        token = jwt.encode(
            claims=json.loads(token_data.json()),
            key=settings.JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return token

    @staticmethod
    def decode_user_token(token: str) -> TokenData:

        try:
            token_data = jwt.decode(
                token=token,
                key=settings.JWT_SECRET_KEY,
                algorithms="HS256",
            )

            return TokenData(**token_data)

        except (JWTError, ValidationError):
            raise Security.Unauthorized

    @staticmethod
    def current_user(user_token: str = Depends(oauth2_scheme)) -> TokenData:
        return Security.decode_user_token(user_token)
    