docker build . -t ocr
docker run -t ocr bash -c "python tests/non_functional_tests/test_ocr_quality.py --postprocess_expected"
