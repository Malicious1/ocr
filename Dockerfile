FROM python:3.10.2
RUN apt-get update && apt-get install -y \
    libsm6  \
    libxext6  \
    ffmpeg  \
    tesseract-ocr  \
    tesseract-ocr-pol \
    tesseract-ocr-ukr \
    tesseract-ocr-rus

WORKDIR /code

COPY requirements.txt .
COPY setup.py .

RUN pip install --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./evaluation /code/evaluation
COPY ./resources /code/resources
COPY ./tests /code/tests

RUN pip install /code/
RUN export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
