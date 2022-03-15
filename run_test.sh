docker build . --no-cache -t ocr
docker run -t ocr bash -c "pytest app/tests"
