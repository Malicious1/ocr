from pydantic import Field, BaseModel
from typing import List


class OCRRequest(BaseModel):
    id: str = Field(title="External ID. For tracking. Response will be returned with the same ID")
    language: str = Field("pol", title="Language of OCR, see /languages for available languages")
    image: bytes = Field(title="Base64 encoded image string")


class LanguagesResponse(BaseModel):
    languages: List[str] = Field(title="Available languages")


class OCRResponse(BaseModel):
    id: str = Field(title="External ID, the same as in the corresponding request")
    text: str = Field(title="Text extracted from the image")


class OCRFileTestResponse(BaseModel):
    text: str
