docker build . --no-cache -t ocr
docker run -p 8000:8000 -t ocr bash -c "uvicorn app.app:app --host 0.0.0.0 --port 8000"
