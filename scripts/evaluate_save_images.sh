# Hating on bash, someone could clean this...

HOST_PREPROCESSED_IMAGES=$(pwd)"/resources/preprocessed_images"
IMAGE_PREPROCESSED_IMAGES=/home/ocr/resources/preprocessed_images

docker build . -t ocr
docker run -v "$HOST_PREPROCESSED_IMAGES":"$IMAGE_PREPROCESSED_IMAGES" -t ocr bash -c \
 "python tests/non_functional_tests/test_ocr_quality.py --postprocess_expected --preprocessed_images_path=$IMAGE_PREPROCESSED_IMAGES"
