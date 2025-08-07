from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_model import User
from app.schemas import UserCreate, UserUpdate


def get_user_crud():
    return user_crud


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        query = select(self.model).filter(self.model.email == email)
        result = db.execute(query).scalars().first()
        return result


user_crud = CRUDUser(User)