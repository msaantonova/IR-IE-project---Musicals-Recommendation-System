from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        if syn.pos() == 'n':
            for lemma in syn.lemmas():
                synonym = lemma.name().lower().replace('_', ' ')
                synonyms.add(synonym)
    return synonyms

class TfidfSearcher:
    def __init__(self, docs, doc_ids):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(docs)
        self.doc_ids = doc_ids

    def expand_query_with_synonyms(self, query):
        terms = [part.strip().lower() for part in query.split(",")]
        expanded = set()
        for term in terms:
            expanded.add(term)
            expanded.update(get_synonyms(term))
        return " ".join(expanded)

    def search(self, query, top_k=5):
        expanded_query = self.expand_query_with_synonyms(query)
        query_vec = self.vectorizer.transform([expanded_query])
        scores = (self.tfidf_matrix * query_vec.T).toarray().flatten()
        ranked_docs = sorted(zip(self.doc_ids, scores), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, score in ranked_docs[:top_k]]

# from sklearn.feature_extraction.text import TfidfVectorizer

# class TfidfSearcher:
#     def __init__(self, docs, doc_ids):
#         self.vectorizer = TfidfVectorizer()
#         self.tfidf_matrix = self.vectorizer.fit_transform(docs)
#         self.doc_ids = doc_ids

#     def search(self, query, top_k=5):
#         query_vec = self.vectorizer.transform([query])
#         scores = (self.tfidf_matrix * query_vec.T).toarray().flatten()
#         ranked_docs = sorted(zip(self.doc_ids, scores), key=lambda x: x[1], reverse=True)
#         return [doc_id for doc_id, score in ranked_docs[:top_k]]


def tfidf_query(graph, query):
    docs = []
    doc_ids = []

    for node in graph.nodes:
        if graph.nodes[node].get("type") != "musical":
            continue

        text_parts = []

        for neighbor in graph.neighbors(node):
            neighbor_data = graph.nodes[neighbor]
            if neighbor_data.get("type") in ["plot", "quote"] and "text" in neighbor_data:
                text_parts.append(neighbor_data["text"])
            elif neighbor_data.get("type") in ["genre", "country", "location", "character", "actor", "director"]:
                text_parts.append(str(neighbor))
        
        doc_text = " ".join(text_parts).lower()
        docs.append(doc_text)
        doc_ids.append(node)

    searcher = TfidfSearcher(docs, doc_ids)
    return searcher.search(query)

