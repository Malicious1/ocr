docker build . --no-cache -t ocr
docker run -t ocr bash -c "python app/tests/test_image_to_str.py"
