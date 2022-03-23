from evaluation.metrics import Metric, JaccardSimilarity, BuiltInMatcher
from typing import List
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class MetricResult:
    name: str
    value: float

    def __repr__(self):
        return "%s: %s" % (self.name.upper(), round(self.value, 3))


class Evaluator:

    def __init__(self, metrics: List[Metric] = None):
        if metrics is None:
            metrics = [JaccardSimilarity(), BuiltInMatcher()]
        self._metrics = metrics

    @property
    def metrics(self) -> List[Metric]:
        return self._metrics

    def evaluate(self, expected: str, predicted: str) -> List[MetricResult]:
        return [MetricResult(m.name, m.get_value(expected, predicted)) for m in self.metrics]

    @staticmethod
    def aggregate_results(evaluation_results: List[List[MetricResult]]) -> List[MetricResult]:
        # TODO: consider alternative aggregation functions\
        metric_results = defaultdict(list)
        for sample in evaluation_results:
            for metric in sample:
                metric_results[metric.name].append(metric.value)
        return [MetricResult(k, sum(v)/len(v)) for k, v in metric_results.items()]
