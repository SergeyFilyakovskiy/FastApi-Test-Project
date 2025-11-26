from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from ..models import Users
from ..database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import Field, BaseModel
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
SECRET_KEY = '8cfc0934f5819c2d0a097de4f2447ef8cbe655daf19c47f083e39cdc58fcff97'
ALGORITHM = 'HS256'

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


bcrypt_context =  CryptContext(schemes=['bcrypt'], deprecated = 'auto')
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code= status.HTTP_200_OK)
async def get_information_about_user(user: user_dependecy, 
                                     db: db_dependecy
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code= status.HTTP_204_NO_CONTENT)
async def change_user_password(user: user_dependecy,
                               db: db_dependecy,
                               user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_info = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_info.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_info.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_info)
    db.commit()

@router.put("/phonenumber/{phone_number}", status_code= status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependecy,
    db: db_dependecy,
    phone_number: str
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_info = db.query(Users).filter(Users.id == user.get('id')).first()
    user_info.phone_number = phone_number
    db.add(user_info)
    db.commit()