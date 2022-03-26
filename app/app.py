from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from PIL import Image
import base64
import io

from app.ocr_engine import OCREngine
from app.rest_models import OCRRequest, OCRResponse, LanguagesResponse, OCRFileTestResponse
from app.ocr_backend import EasyOCRBackend
from app.exceptions import InvalidLanguageError
from app.language import AvailableLanguages


# TODO: move ocr_engine to request parameters

app = FastAPI(title="OCRApp")
languages = AvailableLanguages()
ocr_engine = OCREngine(EasyOCRBackend())


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
        text = ocr_engine.get_text(image, languages.get_langs(request.language.split("+")))
    except InvalidLanguageError:
        raise HTTPException(
            status_code=404, detail="Invalid language. Available languages: " + str(ocr_engine.available_languages))
    return OCRResponse(id=request.id, text=text)


@app.post("/ocr/test_file", response_model=OCRFileTestResponse)
def ocr_test_file(file: UploadFile):
    image_bytes = file.file.read()
    image_bytes = io.BytesIO(image_bytes)
    image = Image.open(image_bytes)
    text = ocr_engine.get_text(image, languages.polish)
    return OCRFileTestResponse(text=text)


@app.get("/languages", response_model=LanguagesResponse)
def get_languages():
    return LanguagesResponse(languages=ocr_engine.available_languages.langs_abbr_3)
