FROM python:latest
RUN apt-get update -y
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install tesseract-ocr
RUN apt-get -y install tesseract-ocr-pol
RUN apt-get -y install tesseract-ocr-ukr
RUN apt-get -y install tesseract-ocr-rus
WORKDIR /code
COPY ./app /code/app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
