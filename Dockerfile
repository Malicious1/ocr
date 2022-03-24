FROM python:3.10.2
RUN apt-get update && apt-get install -y \
    libsm6  \
    libxext6  \
    ffmpeg  \
    tesseract-ocr  \
    tesseract-ocr-pol \
    tesseract-ocr-ukr \
    tesseract-ocr-rus

ARG USER_NAME="user"
RUN useradd -ms /bin/bash $USER_NAME
USER $USER_NAME

WORKDIR /home/$USER_NAME

COPY requirements.txt .
COPY setup.py .

RUN pip install --upgrade -r ./requirements.txt

COPY ./app ./app
COPY ./evaluation ./evaluation
COPY ./resources ./resources
COPY ./tests ./tests

RUN pip install .
RUN export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
