from typing import Any, Generic, Type, TypeVar, Union, cast

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, obj_uuid: Any) -> ModelType | None:
        query = (select(self.model)
                 .filter_by(uuid=obj_uuid))
        result = db.execute(query).scalars().first()
        return result

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        query = (select(self.model)
                 .offset(skip)
                 .limit(limit))
        result = db.execute(query).scalars().all()
        return cast(list[ModelType], result)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # noinspection PyMethodMayBeStatic
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if field in update_data and update_data[field]:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, obj_uuid: str) -> ModelType | None:
        obj = db.get(self.model, obj_uuid)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
