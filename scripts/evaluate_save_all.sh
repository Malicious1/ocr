# Hating on bash, someone could clean this...

HOST_REPORTS=$(pwd)"/resources/evaluation_reports"
IMAGE_REPORTS=/home/ocr/resources/evaluation_reports
HOST_PREPROCESSED_IMAGES=$(pwd)"/resources/preprocessed_images"
IMAGE_PREPROCESSED_IMAGES=/home/ocr/resources/preprocessed_images


docker build . -t ocr
docker run -v "$HOST_REPORTS":"$IMAGE_REPORTS" -v "$HOST_PREPROCESSED_IMAGES":"$IMAGE_PREPROCESSED_IMAGES" -t ocr bash -c \
 "python tests/non_functional_tests/test_ocr_quality.py --postprocess_expected --results_path=$IMAGE_REPORTS/reports.jsonlines --preprocessed_images_path=$IMAGE_PREPROCESSED_IMAGES"
