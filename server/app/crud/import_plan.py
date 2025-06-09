from sqlalchemy.orm import Session

from app import models, schemas


class CRUDImportPlan:
    def import_full_plan(self, db: Session, *, plan_in: schemas.FullPlanImport):
        created_count = {"semesters": 0, "classes": 0, "schedules": 0, "lessons": 0, "personal_events": 0}

        try:
            for semester_data in plan_in.semesters:
                db_semester = models.Semester(
                    name=semester_data.name,
                    start_date=semester_data.start_date,
                    end_date=semester_data.end_date,
                )
                db.add(db_semester)
                created_count["semesters"] += 1

                for event_data in semester_data.personal_events:
                    db_event = models.PersonalEvent(
                        title=event_data.title,
                        description=event_data.description,
                        event_type=event_data.event_type,
                        start_date=event_data.start_date,
                        end_date=event_data.end_date,
                        semester=db_semester
                    )
                    db.add(db_event)
                    created_count["personal_events"] += 1

                for class_data in semester_data.classes:
                    db_class = models.Class(
                        class_title=class_data.class_title,
                        class_code=class_data.class_code,
                        professor_name=class_data.professor_name,
                        semester=db_semester,
                    )
                    db.add(db_class)
                    created_count["classes"] += 1

                    for schedule_data in class_data.schedules:
                        db_schedule = models.Schedule(
                            day_of_week=schedule_data.day_of_week,
                            start_time=schedule_data.start_time,
                            end_time=schedule_data.end_time,
                            location=schedule_data.location,
                            class_=db_class,
                        )
                        db.add(db_schedule)
                        created_count["schedules"] += 1

                    for lesson_data in class_data.lessons:
                        reading_materials_str = None
                        if lesson_data.reading_materials:
                            reading_materials_str = "\n".join(lesson_data.reading_materials)

                        db_lesson = models.Lesson(
                            date=lesson_data.date,
                            topic=lesson_data.topic,
                            summary=lesson_data.summary,
                            reading_materials=reading_materials_str,
                            class_=db_class
                        )
                        db.add(db_lesson)
                        created_count["lessons"] += 1

            for event_data in plan_in.general_personal_events:
                db_event = models.PersonalEvent(
                    title=event_data.title,
                    description=event_data.description,
                    event_type=event_data.event_type,
                    start_date=event_data.start_date,
                    end_date=event_data.end_date,
                    semester_id=None
                )
                db.add(db_event)
                created_count["personal_events"] += 1

            db.commit()

        except Exception as e:
            print(f"ERRO DURANTE A IMPORTAÇÃO, FAZENDO ROLLBACK: {e}")
            db.rollback()
            raise e

        return created_count


import_plan = CRUDImportPlan()
