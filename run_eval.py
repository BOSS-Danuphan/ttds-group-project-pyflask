from app.evaluation.IndexBuilder import IndexBuilder
from app.evaluation.SearchEvaluator import SearchEvaluator
from app.twitter.AnalysedTweet import AnalysedTweet
from collections import namedtuple
from collections import defaultdict
import json, os, math

class EvalParams:    
    def __init__(self, test_label, use_google=True, use_ms=True, use_stopping=True, use_stemming=True, ms_confidence=0.5, google_confidence=0.5):
        self.label = test_label
        self.use_stemming = use_stemming
        self.use_stopping = use_stopping
        self.use_google = use_google
        self.use_ms = use_ms
        self.google_confidence = google_confidence
        self.ms_confidence = ms_confidence

# Load test set
with open(os.getcwd() + r"\app\evaluation\extended_test_set_with_noise.json", "r") as json_file:
    test_json = json_file.read()
    test_set = json.loads(test_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))

# Read labelled queries
queries = {}
for result in test_set.results:
    tweetID = result.retweeted_status.id if hasattr(result, "retweeted_status") else result.id
    for field in result.labels._fields:        
        if field not in queries:
            queries[field] = []        
        if tweetID not in queries[field]:
            queries[field].append(tweetID)

# Configure tests
tests = [
    EvalParams("Default Settings"),
    EvalParams("No stemming", use_stemming=False),
    EvalParams("No stopping", use_stopping=False),
    EvalParams("No stemming or stopping", use_stemming=False, use_stopping=False),
    EvalParams("No vision results", use_ms=False, use_google=False),
    EvalParams("Google vision only", use_ms=False),
    EvalParams("MS vision only", use_google=False),
    EvalParams("Vision confidence 20%", ms_confidence=0.2, google_confidence=0.2),
    EvalParams("Vision confidence 40%", ms_confidence=0.4, google_confidence=0.4),
    EvalParams("Vision confidence 60%", ms_confidence=0.6, google_confidence=0.6),
    EvalParams("Vision confidence 80%", ms_confidence=0.8, google_confidence=0.8),
]

result_file = open(os.getcwd() + r"\app\evaluation\results.txt", "w")
test_maps = {}

# Run tests
for test in tests:
    builder = IndexBuilder(
        use_google=test.use_google, 
        use_ms=test.use_ms, 
        google_confidence=test.google_confidence, 
        ms_confidence=test.ms_confidence, 
        use_stemming=test.use_stemming, 
        use_stopping=test.use_stopping)

    index = builder.load(test_set.results)
    search_eval = SearchEvaluator(index, use_stopping=test.use_stopping, use_stemming=test.use_stemming)
    eval_results = []

    result_file.write ("\n\n{0}\n".format(test.label))
    result_file.write("{0:>9} | {1:>9} |  {2:>9} | {3:>9} | {4:>13} |  {5:>9} |  {6:>9}\n".format(
            "", "Precision", "Recall", "RPrecision", "Avg Precision", "nDCG @ 10", "nDCG @ 20"
        ))

    avg_precisions = []
    for query in queries:
        result = search_eval.evaluate_query(query, queries[query])
        eval_results.append((query, result))

        result_file.write("{0:>9} | {1:9.2f} |  {2:9.2f} |  {3:9.2f} | {4:13.2f} |  {5:9.2f} |  {6:9.2f}\n".format(
            query, result.Precision, result.Recall, result.RPrecision, result.AveragePrecision, result.nDCGat10, result.nDCGat20
        ))

        avg_precisions.append(result.AveragePrecision)
    mean_avg_prec = float(sum(avg_precisions))/max(len(avg_precisions),1)
    test_maps[test.label] = mean_avg_prec
    print("{0:<25} | {1:.4f}".format(test.label, mean_avg_prec))
    
result_file.write("\n\n{0:<25} | Mean Average Precision\n".format("Test"))
for test_label in test_maps:
    result_file.write("{0:<25} | {1:.4f}\n".format(test_label, test_maps[test_label]))

result_file.close()