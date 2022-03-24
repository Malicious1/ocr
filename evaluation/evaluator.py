from evaluation.metrics import Metric, JaccardSimilarity, BuiltInMatcher
from typing import List
from pydantic import BaseModel
from collections import defaultdict


class MetricResult(BaseModel):
    name: str
    value: float

    def __str__(self):
        return "%s: %s" % (self.name.upper(), round(self.value, 3))


class Evaluator:

    def __init__(self, metrics: List[Metric] = None):
        self._metrics = [JaccardSimilarity(), BuiltInMatcher()] if metrics is None else metrics

    @property
    def metrics(self) -> List[Metric]:
        return self._metrics

    def evaluate(self, expected: str, predicted: str) -> List[MetricResult]:
        return [MetricResult(name=m.name, value=m.get_value(expected, predicted)) for m in self.metrics]

    @staticmethod
    def aggregate_results(evaluation_results: List[List[MetricResult]]) -> List[MetricResult]:
        # TODO: consider alternative aggregation functions\
        metric_results = defaultdict(list)
        for sample in evaluation_results:
            for metric in sample:
                metric_results[metric.name].append(metric.value)
        return [MetricResult(name=k, value=sum(v)/len(v)) for k, v in metric_results.items()]
