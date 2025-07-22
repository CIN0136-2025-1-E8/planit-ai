from sqlalchemy.orm import Session
from app.models import Test, Assessment  # Make sure these models exist
from app.schemas import TestCreate, TestUpdate, AssessmentCreate, AssessmentUpdate  # Make sure these schemas exist

# Test CRUD
def create_test(db: Session, test: TestCreate):
    db_test = Test(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()

def update_test(db: Session, test_id: int, test: TestUpdate):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test:
        for key, value in test.dict(exclude_unset=True).items():
            setattr(db_test, key, value)
        db.commit()
        db.refresh(db_test)
    return db_test

def delete_test(db: Session, test_id: int):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test:
        db.delete(db_test)
        db.commit()
    return db_test

# Assessment CRUD
def create_assessment(db: Session, assessment: AssessmentCreate):
    db_assessment = Assessment(**assessment.dict())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def get_assessment(db: Session, assessment_id: int):
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()

def update_assessment(db: Session, assessment_id: int, assessment: AssessmentUpdate):
    db_assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if db_assessment:
        for key, value in assessment.dict(exclude_unset=True).items():
            setattr(db_assessment, key, value)
        db.commit()
        db.refresh(db_assessment)
    return db_assessment

def delete_assessment(db: Session, assessment_id: int):
    db_assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if db_assessment:
        db.delete(db_assessment)
        db.commit()
    return db_assessment