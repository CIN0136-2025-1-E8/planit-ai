import json
from enum import Enum
from pathlib import Path

JSON_DEFINITIONS_DIR = Path(__file__).resolve().parent / "json_definitions"


class AvailableSchemas(str, Enum):
    CLASS = "class"
    SEMESTER = "semester"


SCHEMA_REGISTRY: dict[AvailableSchemas, dict] = {}


def load_schemas_into_registry():
    for schema_enum in AvailableSchemas:
        file_path = JSON_DEFINITIONS_DIR / f"{schema_enum.value}.json"
        if not file_path.exists():
            print(f"Warning: Schema file not found for {schema_enum.name} at {file_path}")
            continue

        with open(file_path, 'r') as f:
            schema_data = json.load(f)
            SCHEMA_REGISTRY[schema_enum] = schema_data
