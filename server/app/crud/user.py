from typing import Any, Union
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.crud.base import CRUDBase
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
  

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = self.model(
            name=obj_in.name,
            nickname=obj_in.nickname,
            email=obj_in.email,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(self.model).filter(self.model.email == email).first()

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        return super().update(db, db_obj=db_obj, obj_in=update_data)

user_crud = CRUDUser(User)
