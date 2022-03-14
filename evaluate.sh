docker build . --no-cache -t ocr
docker run -t ocr bash -c "python app/evaluation/test_image_to_str.py"
