# Hating on bash, someone could clean this...

HOST_REPORTS=$(pwd)"/resources/evaluation_reports"
IMAGE_REPORTS=/home/ocr/resources/evaluation_reports

docker build . -t ocr
docker run -v "$HOST_REPORTS":"$IMAGE_REPORTS" -t ocr bash -c \
 "python tests/non_functional_tests/test_ocr_quality.py --postprocess_expected --results_path=$IMAGE_REPORTS/reports.jsonlines"
