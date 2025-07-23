from typing import Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime, date, timedelta

from app.crud.base import CRUDBase
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate, EventUpdate

class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def create(self, db: Session, *, obj_in: EventCreate, owner_uuid: str) -> Event:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(
            **obj_in_data,
            owner_uuid=owner_uuid
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_event(self, db: Session, uuid: str) -> Event | None:
        query = select(self.model).filter(self.model.uuid == uuid)
        result = db.execute(query).scalars().first()
        return result

    def get_events_by_owner(
        self,
        db: Session,
        owner_uuid: str,
        start_date: date | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[Event]:
        """
        Obtém todos os eventos associados a um usuário específico,
        para os 7 próximos dias (incluindo a start_date fornecida),
        com opções de paginação.
        """
        filters = [self.model.owner_uuid == owner_uuid]

        if start_date:
            # Calcular a data de fim (7 dias a partir de start_date, incluindo-a)
            # Para incluir o dia inteiro, o end_datetime final seria o último milissegundo do 7º dia
            calculated_end_date = start_date + timedelta(days=6)
            
            # Converter datas para strings no formato ISO 8601 para comparação com o DB
            start_datetime_str = datetime.combine(start_date, datetime.min.time()).isoformat() # Início do dia
            end_datetime_str = datetime.combine(calculated_end_date, datetime.max.time()).isoformat() # Fim do 7º dia

            filters.append(self.model.end_datetime >= start_datetime_str)
            filters.append(self.model.start_datetime <= end_datetime_str)
            
        query = select(self.model).filter(and_(*filters)).offset(skip).limit(limit)
        return list(db.execute(query).scalars().all())

    def update(self, db: Session, *, db_obj: Event, obj_in: Union[EventUpdate, dict[str, Any]]) -> Event:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # Converta datetime para string ISO 8601 para o modelo do DB (que usa String)
        if 'start_datetime' in update_data and update_data['start_datetime'] is not None:
            update_data['start_datetime'] = update_data['start_datetime'].isoformat()
        if 'end_datetime' in update_data and update_data['end_datetime'] is not None:
            update_data['end_datetime'] = update_data['end_datetime'].isoformat()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, uuid: str) -> Event | None:
        return super().remove(db, id=uuid)
event_crud = CRUDEvent(Event)
