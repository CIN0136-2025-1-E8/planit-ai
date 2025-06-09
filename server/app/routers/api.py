from fastapi import APIRouter

from . import semesters, classes, schedules, lessons, schedule_overrides, personal_events, import_plan

api_router = APIRouter()
api_router.include_router(classes.router, prefix="/classes", tags=["Turmas"])
api_router.include_router(import_plan.router, prefix="/import-plan", tags=["Importar Plano"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["Aulas"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["Horários"])
api_router.include_router(schedule_overrides.router, prefix="/schedule-overrides", tags=["Exceções de Horário"])
api_router.include_router(semesters.router, prefix="/semesters", tags=["Semestres"])
api_router.include_router(personal_events.router, prefix="/personal-events", tags=["Eventos Pessoais"])
