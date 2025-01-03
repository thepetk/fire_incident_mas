import os
from typing import Any, Dict, List, Optional, Type

from crewai_tools import BaseTool
from pydantic import BaseModel
from .schemas import MdxAnalyzerSchema

MDX_FILE = os.getenv("MDX_FILE", "emergency_02.mdx")
MAPPINGS = {
    "fire_type": "* **Fire Type:**",
    "number_of_injured_people": "* **Number of Injured People:**",
    "fire_severity": "* **Fire Severity:**",
    "fire_size": "* **Estimated Fire Size:**",
    "fire_spread": "* **Fire Spread:**",
    "coordinates": "(X, Y Coordinates)",
}


class MdxAnalyzerTool(BaseTool):
    name: str = "MdxAnalyzerTool"
    description: str = (
        "A tool that reads an mdx file and returns the most important information"
    )
    args_schema: Type[BaseModel] = MdxAnalyzerSchema
    mdx_path: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, mdx_path: str = MDX_FILE, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.mdx_path = mdx_path

    def _read_mdx(self) -> str:
        f = open(self.mdx_path)
        return [line.strip() for line in f]

    def _run(self, *args: Any, **kwargs: Any) -> Dict[str, str]:
        lines = self._read_mdx()
        return self._analyze_mdx(lines)

    def _analyze_mdx(
        self,
        lines: List[str],
    ) -> List[str, str]:
        analysis: Dict[str, str] = {}
        for line in lines:
            for key in MAPPINGS.keys():
                q = MAPPINGS[key]
                if q in line:
                    analysis[key] = line.replace(q, "").strip()
        return analysis
