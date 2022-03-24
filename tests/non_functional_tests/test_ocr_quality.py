from evaluation.test_executor import TestExecutor
import argparse
from pathlib import Path

# TODO: add storing results to file, remember about docker volume

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--silent", help="Do not print results", action='store_true')
    parser.add_argument("--postprocess_expected", help="Should expected text be post-processed", action='store_true')
    parser.add_argument("--annotations_path", help="path to jsonlines file with annotations", type=Path)
    parser.add_argument("--images_path", help="path to directory with images", type=Path)
    parser.add_argument("--results_path", help="path to jsonlines file where test report should be saved", type=Path)
    parser.add_argument("--preprocessed_images_path", help="path to directory to save pre-processed images", type=Path)
    args = parser.parse_args()

    if args.images_path is None or args.annotations_path is None:
        print("\n !!! Path to annotations/images not provided, defaulting to base_pol_eng_rus dataset !!! \n")
        dataset_path = Path(__file__).parent.parent.parent / "resources/datasets" / "base_pol_eng_rus"
        args.annotations_path = dataset_path / "annotations.jsonlines"
        args.images_path = dataset_path / "images"

    runner = TestExecutor(
        annotations_path=args.annotations_path,
        images_path=args.images_path,
        results_path=args.results_path,
        preprocessd_images_path=args.preprocessed_images_path,
        silent=args.silent,
        postprocess_expected=args.postprocess_expected
    )
    results = runner.run_test()
