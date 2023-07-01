from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from src.models.users import UserBase, UserInDb
from src.collections.users import UsersCollection
from src.models.base import Token, TokenData
from pydantic import validate_email, EmailError
from src.security import Security
router = APIRouter()


@router.post(
    "/login",
    response_model=Token
)
async def login(login_form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        validate_email(login_form_data.username)
        user = await UsersCollection.get_by_email(login_form_data.username)
    except EmailError:
        user = await UsersCollection.get_by_username(login_form_data.username)
    print(login_form_data.password, user.hashed_password)
    
    verified = Security.verify_password(login_form_data.password, user.hashed_password)
    if verified:
        return Token(access_token=Security.generate_user_token(user))
    else:
        raise Security.Unauthorized
    
    
@router.post(
    "/signup",
    response_model=UserBase
)
async def signup(new_user: UserBase, password: str = Body()):
    hashed_password = Security.hash_password(password)
    await UsersCollection.create(new_user, hashed_password)
    return new_user


@router.get(
    "/me",
    response_model=UserBase
)
async def me(user: TokenData = Depends(Security.current_user)):
    return await UsersCollection.get(user.id)
    

@router.delete(
    "/delete_account",
    response_model=None
)
async def delete_account(user: TokenData = Depends(Security.current_user)):
    await UsersCollection.delete(user.id)
