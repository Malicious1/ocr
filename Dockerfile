FROM pytorch/pytorch

# ----------------------------------------------- Install system dependencies ------------------------------------------

RUN apt-get update && apt-get install -y \
    libsm6  \
    libxext6  \
    ffmpeg  \
    libglib2.0-0 \
    libxrender-dev \
    libgl1-mesa-dev \
    tesseract-ocr  \
    tesseract-ocr-pol \
    tesseract-ocr-ukr \
    tesseract-ocr-rus \
    git \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

# --------------------------------------------------- Create dedicated user --------------------------------------------

ARG USER_NAME="user"
RUN useradd -ms /bin/bash $USER_NAME
WORKDIR /home/$USER_NAME
USER $USER_NAME

# ------------------------------------------------------ Install Easy OCR  ---------------------------------------------

# Add LMs here, english goes well with any script
ARG LANGUAGE_MODELS_LATIN="['pl','en']"
ARG LANGUAGE_MODELS_CYRILLIC="['uk', 'ru', 'en']"

RUN git clone "https://github.com/JaidedAI/EasyOCR.git" \
    && cd EasyOCR \
    && git remote add upstream "https://github.com/JaidedAI/EasyOCR.git" \
    && git pull upstream master

# Build C extensions and pandas
RUN cd EasyOCR \
    && python setup.py build_ext --inplace -j 4 \
    && python -m pip install -e .

# ----------------------------------------------- Collect language models ----------------------------------------------


RUN python -c "import easyocr; reader = easyocr.Reader(${LANGUAGE_MODELS_LATIN}, gpu=False)"
RUN python -c "import easyocr; reader = easyocr.Reader(${LANGUAGE_MODELS_CYRILLIC}, gpu=False)"
RUN export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# --------------------------------------------------- Install project --------------------------------------------------

COPY requirements.txt .
COPY setup.py .

# Change to root so that scripts are in global
USER root
RUN pip install --upgrade -r ./requirements.txt

COPY ./app ./app
COPY ./evaluation ./evaluation
COPY ./resources ./resources
COPY ./tests ./tests

RUN pip install .

USER $USER_NAME
#
#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
