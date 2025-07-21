from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(db: Session = Depends(get_db)) -> User:
    from app.crud.user import user_crud
    from app.schemas import UserCreate
    test_user = user_crud.get_by_email(db=db, email="teste@planit.ai")
    if not test_user:
        user_in = UserCreate(
            name="user",
            email="teste@planit.ai",
            password="password")
        test_user = user_crud.create(db=db, obj_in=user_in)
    return test_user
