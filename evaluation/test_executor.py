import json
from pathlib import Path
from typing import List
from pydantic import BaseModel
from PIL import Image
import io

from app.ocr_engine import OCREngine
from evaluation.evaluator import Evaluator, MetricResult
from evaluation.metrics import BuiltInMatcher, JaccardSimilarity


class Annotation(BaseModel):
    file_name: str
    language: str
    text: str


class SampleEvaluationResults(BaseModel):
    file_name: str
    expected_text: str
    predicted_text: str
    metric_results: List[MetricResult]

    def __str__(self):
        metrics_text = ""
        for m in self.metric_results:
            metrics_text += str(m) + "\n"

        return "FILE: %s" % self.file_name + "\n\n" + \
               "EXPECTED_TEXT: %s" % self.expected_text + "\n\n" + \
               "PREDICTED_TEXT: %s" % self.predicted_text + "\n\n" + \
               metrics_text + "_" * 90


class TestReport(BaseModel):
    results_per_sample: List[SampleEvaluationResults]
    summary: List[MetricResult]


class TestExecutor:

    def __init__(self, images_path: Path, annotations_path: Path, results_path: Path = None,
                 preprocessd_images_path: Path = None, evaluator: Evaluator = None, postprocess_expected: bool = True,
                 silent: bool = False):
        self.images_path = images_path
        self.annotations_path = annotations_path
        self.results_path = results_path
        self.preprocessed_images_path = preprocessd_images_path
        self.ocr_engine = OCREngine()
        self.silent = silent
        self.postprocess_expected = postprocess_expected
        self.evaluator = Evaluator(metrics=[JaccardSimilarity(), BuiltInMatcher()]) if evaluator is None else evaluator

    def read_annotations(self) -> List[Annotation]:
        with open(self.annotations_path) as f:
            annotations = [Annotation.parse_obj(json.loads(l)) for l in f.readlines()]
        return annotations

    def read_image(self, file_name: str) -> Image:
        with open(self.images_path / file_name, "rb") as f:
            image = Image.open(io.BytesIO(f.read()))
            return image

    def save_preprocessed_image(self, image: Image, file_name: str):
        with open(self.preprocessed_images_path / file_name, "wb") as f:
            image.save(f)

    def save_test_report(self, report: TestReport):
        with open(self.results_path, "a") as f:
            f.write(report.json()+"\n")

    def evaluate_sample(self, annotation: Annotation) -> SampleEvaluationResults:
        image = self.read_image(annotation.file_name)
        text = self.ocr_engine.get_text(image, annotation.language)
        if self.postprocess_expected:
            annotation.text = self.ocr_engine.postprocess_text(annotation.text)
        if self.preprocessed_images_path is not None:
            preprocessed_image = self.ocr_engine.preprocess_image(image)
            self.save_preprocessed_image(preprocessed_image, annotation.file_name)
        results = SampleEvaluationResults(
            file_name=annotation.file_name, expected_text=annotation.text, predicted_text=text,
            metric_results=self.evaluator.evaluate(annotation.text, text))
        if not self.silent:
            print(results)
        return results

    def run_test(self):
        annotations = self.read_annotations()
        all_results = [self.evaluate_sample(a) for a in annotations]
        aggregated_results = self.evaluator.aggregate_results([r.metric_results for r in all_results])
        report = TestReport(results_per_sample=all_results, summary=aggregated_results)
        if not self.silent:
            print("\n" + "AGGREGATED: ")
            for m in aggregated_results:
                print(m)
        if self.results_path is not None:
            self.save_test_report(report)
        return report
