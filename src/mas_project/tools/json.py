import json
from typing import Any, Literal, Optional, Type

from crewai_tools import BaseTool
from pydantic import BaseModel

from .schemas import JSONReaderSchema

FIRE_UNITS_JSON_FILE = "firetrucks.json"
MEDICAL_UNITS_JSON_FILE = "hospitals.json"


class JSONReaderTool(BaseTool):
    name: "str" = "JSONReaderTool"
    description: "str" = "A tool that reads a json file with fire truck units"
    args_schema: "Type[BaseModel]" = JSONReaderSchema
    json_file_path: "Optional[str]" = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        json_file_type: "Literal['firetrucks', 'hospitals']" = "firetrucks",
        **kwargs: "Any",
    ):
        super().__init__(**kwargs)
        if json_file_type not in ["firetrucks", "hospitals"]:
            raise Exception(
                "json_file_type error:: should be one of 'hospitals' or 'firetrucks'"
            )
        elif json_file_type == "hospitals":
            self.json_file_path = MEDICAL_UNITS_JSON_FILE
        else:
            self.json_file_path = FIRE_UNITS_JSON_FILE

    def _read_json(self) -> "dict[str, str | int]":
        f = open(self.json_file_path)
        return json.load(f)  # type: ignore

    def _run(self, *args: "Any", **kwargs: "Any") -> "dict[str, str | int]":
        return self._read_json()
