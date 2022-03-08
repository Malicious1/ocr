FROM python:latest
RUN apt-get update -y
RUN apt-get -y install libsm6 libxext6 ffmpeg
RUN apt-get -y install tesseract-ocr
RUN apt-get -y install tesseract-ocr-pol
RUN apt-get -y install tesseract-ocr-ukr
RUN apt-get -y install tesseract-ocr-rus
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
RUN export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
