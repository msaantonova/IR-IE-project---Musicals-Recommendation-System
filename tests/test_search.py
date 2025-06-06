import networkx as nx
from my_project.graph_builder import load_musicals_to_graph  
from my_project.search import sort_musicals_query  

def main():
    import pickle
    with open("output/musical_graph.gpickle", "rb") as f:
        G = pickle.load(f)

    
    query = "monster"
    results = sort_musicals_query(G, query)
    print("Recommended musicals:", results)

if __name__ == "__main__":
    main()


def sort_musicals_query(graph, query):
    query_parts = [part.strip().lower() for part in query.split(",")]
    results = []

    for node in graph.nodes:
        if graph.nodes[node].get('type') != 'musical':
            continue

        matched_all = True

        for part in query_parts:
            part_matched = False

            for neighbor in graph.neighbors(node):
                neighbor_data = graph.nodes[neighbor]
                if part == str(neighbor).lower():
                    part_matched = True
                    break

                if neighbor_data.get('type') in ['genre', 'country', 'location', 'character', 'actor', 'director']:
                    if part == str(neighbor).lower():
                        part_matched = True
                        break

                if neighbor_data.get('type') in ['plot', 'quote']:
                    if 'text' in neighbor_data and part in neighbor_data['text'].lower():
                        part_matched = True
                        break

            if not part_matched:
                matched_all = False
                break

        if matched_all:
            results.append(node)

    return results