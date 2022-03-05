from pydantic import Field, BaseModel
from typing import List
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from pytesseract import TesseractError
from PIL import Image
import base64
import io

from app.ocr_engine import OCREngine


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


app = FastAPI(title="OCRApp")
ocr_engine = OCREngine()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.post("/ocr", response_model=OCRResponse)
def ocr(request: OCRRequest):
    """Get text from image bytes"""
    image_bytes = base64.decodebytes(request.image)
    image_bytes = io.BytesIO(image_bytes)
    image = Image.open(image_bytes)
    try:
        text = ocr_engine.get_text(image, request.language)
    except TesseractError as e:
        if e.status == 1:
            languages = str(ocr_engine.get_languages())
            raise HTTPException(status_code=404, detail="Invalid language. Available languages: " + languages)
        else:
            raise e
    return OCRResponse(id=request.id, text=text)


@app.post("/ocr/test_file", response_model=OCRResponse)
def ocr_test_file(file: UploadFile):
    image_bytes = file.file.read()
    image_bytes = io.BytesIO(image_bytes)
    image = Image.open(image_bytes)
    text = ocr_engine.get_text(image, "pol")
    return OCRResponse(id="some_id", text=text)


@app.get("/languages", response_model=LanguagesResponse)
def get_languages():
    return LanguagesResponse(languages=ocr_engine.get_languages())
