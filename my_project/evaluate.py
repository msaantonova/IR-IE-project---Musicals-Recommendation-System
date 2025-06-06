import json
import pickle
import math
from search import sort_musicals_query  # boolean search
from tfidf_search import tfidf_query  #  TF-IDF 

def dcg(relevances):
    return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(relevances))

def ndcg_at_k(retrieved, relevant_dict, k=5):
    relevances = [relevant_dict.get(title, 0) for title in retrieved[:k]]
    ideal_relevances = sorted(relevant_dict.values(), reverse=True)[:k]
    dcg_score = dcg(relevances)
    idcg_score = dcg(ideal_relevances)
    return dcg_score / idcg_score if idcg_score != 0 else 0.0

def evaluate_method(graph, queries, retrieval_func, method_name):
    print(f"\nEvaluation: {method_name}\n{'-'*30}")
    total_score = 0
    for item in queries:
        query = item["query"]
        relevant = item["relevant"]
        predicted = retrieval_func(graph, query)
        ndcg_score = ndcg_at_k(predicted, relevant, k=5)
        print(f"Query: {query} → nDCG@5 = {ndcg_score:.4f}")
        total_score += ndcg_score
    average = total_score / len(queries)
    print(f"\n📊 Average nDCG@5 for {method_name}: {average:.4f}")
    return average

def main():
    with open("output/musical_graph.gpickle", "rb") as f:
        graph = pickle.load(f)

    with open("data/golden_dataset.json", "r") as f:
        evaluation_queries = json.load(f)

    evaluate_method(graph, evaluation_queries, sort_musicals_query, "Boolean Search (sort_musicals_query)")

    evaluate_method(graph, evaluation_queries, tfidf_query, "TF-IDF Search")

if __name__ == "__main__":
    main()
