from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/import/full-plan", status_code=201)
def import_full_plan(
        plan_in: schemas.FullPlanImport,
        db: Session = Depends(get_db),
):
    try:
        created_count = crud.import_plan.import_full_plan(db=db, plan_in=plan_in)
        return {
            "status": "success",
            "message": "Plano importado com sucesso!",
            "semesters_created": created_count["semesters"],
            "classes_created": created_count["classes"],
            "schedules_created": created_count["schedules"],
            "lessons_created": created_count["lessons"],
            "personal_events_created": created_count["personal_events"],
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Falha na importação do plano: {e}"
        )
