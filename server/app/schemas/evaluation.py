from pydantic import BaseModel, ConfigDict


class EvaluationBase(BaseModel):
    pass


class EvaluationCreate(EvaluationBase):
    course_uuid: str


class EvaluationUpdate(BaseModel):
    pass


class Evaluation(EvaluationBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)
