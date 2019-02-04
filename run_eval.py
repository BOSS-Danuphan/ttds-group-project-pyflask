from app.evaluation.IndexBuilder import IndexBuilder
from app.evaluation.SearchEvaluator import SearchEvaluator
from app.twitter.AnalysedTweet import AnalysedTweet
from collections import namedtuple
import json, os

builder = IndexBuilder()

with open(os.getcwd() + r"\app\evaluation\labelled_structure.json", "r") as json_file:
    test_json = json_file.read()
    test_set = json.loads(test_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))
    index = builder.load(test_set.results)

## TODO: Load ideal result and query pairs
queries = [
    ("water", [1091419055788052480, 1091419075052355584]),
    ("pizza", [1091419084049268738]),
    ("cat", [1091419084049268738]),
]

search_eval = SearchEvaluator(index)
eval_results = []
for query in queries:
    result = search_eval.evaluate_query(query[0], query[1])
    eval_results.append((query[0], result))

