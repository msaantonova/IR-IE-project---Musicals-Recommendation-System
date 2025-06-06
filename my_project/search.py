from nltk.corpus import wordnet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        if syn.pos() == 'n':  
            for lemma in syn.lemmas():
                synonym = lemma.name().lower().replace('_', ' ')
                synonyms.add(synonym)
    return synonyms

def sort_musicals_query(graph, query):
    query_parts = [part.strip().lower() for part in query.split(",")]
    results = []

    for node in graph.nodes:
        if graph.nodes[node].get('type') != 'musical':
            continue

        score = 0
        total_parts = len(query_parts)

        for part in query_parts:
            part_synonyms = get_synonyms(part)
            part_synonyms.add(part)
            part_matched = False

            for neighbor in graph.neighbors(node):
                neighbor_data = graph.nodes[neighbor]
                neighbor_text = str(neighbor).lower()

                if neighbor_text in part_synonyms:
                    part_matched = True
                    break

                if neighbor_data.get('type') in ['genre', 'country', 'location', 'character', 'actor', 'director']:
                    if neighbor_text in part_synonyms:
                        part_matched = True
                        break

                if neighbor_data.get('type') in ['plot', 'quote'] and 'text' in neighbor_data:
                    if any(syn in neighbor_data['text'].lower() for syn in part_synonyms):
                        part_matched = True
                        break

            if part_matched:
                score += 1

        if score > 0:
            results.append((node, score / total_parts))  

    results.sort(key=lambda x: x[1], reverse=True)

    return [node for node, score in results]


# def sort_musicals_query(graph, query):
#     query_parts = [part.strip().lower() for part in query.split(",")]
#     results = []

#     for node in graph.nodes:
#         if graph.nodes[node].get('type') != 'musical':
#             continue

#         score = 0
#         total_parts = len(query_parts)

#         for part in query_parts:
#             part_matched = False

#             for neighbor in graph.neighbors(node):
#                 neighbor_data = graph.nodes[neighbor]
#                 neighbor_text = str(neighbor).lower()

#                 if neighbor_text == part:
#                     part_matched = True
#                     break

#                 if neighbor_data.get('type') in ['genre', 'country', 'location', 'character', 'actor', 'director']:
#                     if neighbor_text == part:
#                         part_matched = True
#                         break

#                 if neighbor_data.get('type') in ['plot', 'quote'] and 'text' in neighbor_data:
#                     if part in neighbor_data['text'].lower():
#                         part_matched = True
#                         break

#             if part_matched:
#                 score += 1

#         if score > 0:
#             results.append((node, score / total_parts))  

#     results.sort(key=lambda x: x[1], reverse=True)
#     return [node for node, score in results]
