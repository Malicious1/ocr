import json
from pathlib import Path
from typing import List
from pydantic import BaseModel
from PIL import Image
import io
from dataclasses import dataclass

from app.ocr_engine import OCREngine
from evaluation.evaluator import Evaluator, MetricResult
from evaluation.metrics import BuiltInMatcher, JaccardSimilarity


class Annotation(BaseModel):

    file_name: str
    language: str
    text: str


@dataclass
class SampleEvaluationResults:
    file_name: str
    expected_text: str
    predicted_text: str
    metric_results: List[MetricResult]

    def __repr__(self):
        metrics_text = ""
        for m in self.metric_results:
            metrics_text += str(m) + "\n"

        return "FILE: %s" % self.file_name + "\n\n" + \
               "EXPECTED_TEXT: %s" % self.expected_text + "\n\n" + \
               "PREDICTED_TEXT: %s" % self.predicted_text + "\n\n" + \
               metrics_text + "_" * 90


class TestExecutor:

    def __init__(self, images_path: str, annotations_path: str, evaluator: Evaluator = None,
                 postprocess_expected: bool = True, silent: bool = False):
        self.images_path = images_path
        self.annotations_path = annotations_path
        self.ocr_engine = OCREngine()
        self.silent = silent
        self.postprocess_expected = postprocess_expected
        if evaluator is None:
            self.evaluator = Evaluator(metrics=[JaccardSimilarity(), BuiltInMatcher()])

    def read_annotations(self) -> List[Annotation]:
        with open(self.annotations_path) as f:
            annotations = [Annotation.parse_obj(json.loads(l)) for l in f.readlines()]
        return annotations

    def read_image(self, file_name: str) -> Image:
        with open(self.images_path / file_name, "rb") as f:
            image = Image.open(io.BytesIO(f.read()))
            return image

    def evaluate_sample(self, annotation: Annotation) -> SampleEvaluationResults:
        image = self.read_image(annotation.file_name)
        text = self.ocr_engine.get_text(image, annotation.language)
        if self.postprocess_expected:
            annotation.text = self.ocr_engine.postprocess_text(annotation.text)
        results = SampleEvaluationResults(
            annotation.file_name, annotation.text, text, self.evaluator.evaluate(annotation.text, text))
        if not self.silent:
            print(results)
        return results

    def run_test(self):
        annotations = self.read_annotations()
        all_results = [self.evaluate_sample(a) for a in annotations]
        aggregated_results = self.evaluator.aggregate_results([r.metric_results for r in all_results])
        if not self.silent:
            print("\n" + "AGGREGATED: " + str(aggregated_results))
        return all_results, aggregated_results
