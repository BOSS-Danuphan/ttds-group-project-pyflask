from app.evaluation.IndexBuilder import IndexBuilder
from app.evaluation.SearchEvaluator import SearchEvaluator

## TODO: Load Tweets and Vision results for populating index
json_tuples = [("", ""), ("", "")]

## TODO: Load ideal result and query pairs
queries = [
    ("sunset on the beach", ['tweet_id_1', 'tweet_id_5']),
    ("sunrise on the beach", ['tweet_id_8', 'tweet_id_17']),
    ("calton hill at sunrise", ['tweet_id_20']),
]

builder = IndexBuilder()
index = builder.load(json_tuples)

search_eval = SearchEvaluator(index)

eval_results = []
for query in queries:
    result = search_eval.evaluate_query(queries[0], queries[1])
    eval_results.append(query[0], result)

print(eval_results)