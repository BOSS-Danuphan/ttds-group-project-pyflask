from app.evaluation.IndexBuilder import IndexBuilder
from app.evaluation.SearchEvaluator import SearchEvaluator
from app.twitter.AnalysedTweet import AnalysedTweet
from collections import namedtuple
from collections import defaultdict
import json, os

builder = IndexBuilder()

with open(os.getcwd() + r"\app\evaluation\test_set.json", "r") as json_file:
    test_json = json_file.read()
    test_set = json.loads(test_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))
    index = builder.load(test_set.results)

queries = {}
for result in test_set.results:
    for field in result.labels._fields:
        if field in queries.keys():
            queries[field].append(result.id)
        else:
            queries[field] = [result.id]

search_eval = SearchEvaluator(index)
eval_results = []

print("\n\n{0:>9} | {1:>9} |  {2:>9} | {3:>9} | {4:>13} |  {5:>9} |  {6:>9}".format(
        "", "Precision", "Recall", "RPrecision", "Avg Precision", "nDCG @ 10", "nDCG @ 20"
    ))

for query in queries:
    result = search_eval.evaluate_query(query, queries[query])
    eval_results.append((query, result))

    print("{0:>9} | {1:9.2f} |  {2:9.2f} |  {3:9.2f} | {4:13.2f} |  {5:9.2f} |  {6:9.2f}".format(
        query, result.Precision, result.Recall, result.RPrecision, result.AveragePrecision, result.nDCGat10, result.nDCGat20
    ))