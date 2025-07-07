import json

from schemas import CourseBase

if __name__ == "__main__":
    with open("json_schemas/CourseBase_schema.json", "w") as f:
        f.write(json.dumps(CourseBase.model_json_schema(), indent=2))