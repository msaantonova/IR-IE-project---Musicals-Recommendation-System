# graph_utils.py
def get_text_for_film(graph, film_node):
    texts = []
    
    if 'title' in graph.nodes[film_node]:
        texts.append(graph.nodes[film_node]['title'].lower())
    else:
        texts.append(str(film_node).lower())
    
    for neighbor in graph.neighbors(film_node):
        neighbor_data = graph.nodes[neighbor]
        ntype = neighbor_data.get('type', '')
        
        if ntype in ['genre', 'country', 'location', 'character', 'actor', 'director']:
            texts.append(str(neighbor).lower())
        elif ntype in ['plot', 'quote']:
            if 'text' in neighbor_data:
                texts.append(neighbor_data['text'].lower())
    
    return " ".join(texts)
