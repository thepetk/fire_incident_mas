from pydantic import BaseModel, Field


class RouteDistanceSchema(BaseModel):
    """Input for the RouteDistanceTool."""

    x_origin: "float" = Field(..., description="X coordinate of the origin location.")
    y_origin: "float" = Field(..., description="Y coordinate of the origin location.")
    x_destination: "float" = Field(
        ..., description="X coordinate of the destination location."
    )
    y_destination: "float" = Field(
        ..., description="Y coordinate of the destination location."
    )


class MdxAnalyzerSchema(BaseModel):
    """Input for the MdxAnalyzerTool."""

    mdx_path: "str" = Field(..., description="The path to fire report mdx file")


class JSONReaderSchema(BaseModel):
    """Input for the JSONReaderTool."""

    json_file_type: "str" = Field(
        ..., description="The type of the json file loaded [hospitals or firetrucks]"
    )
