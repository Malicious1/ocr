FROM pytorch/pytorch

ARG gh_username=JaidedAI
ARG language_models_latin="['pl','en']"
ARG language_models_cyrillic="['uk', 'ru']"

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

ARG USER_NAME="user"
RUN useradd -ms /bin/bash $USER_NAME
USER $USER_NAME

WORKDIR /home/$USER_NAME

RUN git clone "https://github.com/$gh_username/EasyOCR.git" \
    && cd EasyOCR \
    && git remote add upstream "https://github.com/JaidedAI/EasyOCR.git" \
    && git pull upstream master

RUN pwd
RUN ls
# Build C extensions and pandas
RUN cd EasyOCR \
    && python setup.py build_ext --inplace -j 4 \
    && python -m pip install -e .

# Downloads models into container stored inside the ~/.EasyOCR/model directory'
# >> Also implicitly checks no errors on import
RUN python -c "import easyocr; reader = easyocr.Reader(${language_models_latin}, gpu=False)"
RUN python -c "import easyocr; reader = easyocr.Reader(${language_models_cyrillic}, gpu=False)"

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
