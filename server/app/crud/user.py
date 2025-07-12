from typing import Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import hash_password, verify_password
from app.crud.base import CRUDBase
from app.models.user_model import User
from app.schemas import UserCreate, UserCreateInDB, UserUpdate

class CRUDUser(CRUDBase[User, UserCreateInDB, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_password = hash_password(obj_in.password)
        new_obj_in = UserCreateInDB(hashed_password=hashed_password, **obj_in.model_dump())
        db_obj = super().create(db, obj_in=new_obj_in)
        return db_obj

    def get_by_email(self, db: Session, email: str) -> User | None:
        query = select(self.model).filter(self.model.email == email)
        result = db.execute(query).scalars().first()
        return result

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, dict[str, Any]]) -> User:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
user_crud = CRUDUser(User)