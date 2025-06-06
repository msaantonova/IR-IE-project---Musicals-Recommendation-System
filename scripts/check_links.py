import networkx as nx
import pickle

def load_graph(path="output/musical_graph.gpickle"):
    with open(path, "rb") as f:
        return pickle.load(f)

def check_album_links(graph):
    count_with_link = 0
    total_nodes = 0
    for node in graph.nodes:
        total_nodes += 1
        node_data = graph.nodes[node]
        if "album_link" in node_data or "album_url" in node_data:
            count_with_link += 1
            print(f"Node: {node}")
            print(f"album_link: {node_data.get('album_link')}")
            print(f"album_url: {node_data.get('album_url')}")
            print("-" * 20)

def check_album_link_nodes(graph):
    album_link_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('type') == 'album_link']
    print(f"Всего узлов с типом 'album_link': {len(album_link_nodes)}")
    for node in album_link_nodes[:10]:  
        print(node)

def check_musical_album_links(graph):
    count_with_links = 0
    musical_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('type') == 'musical']
    for musical in musical_nodes:
        album_links = [
            nbr for nbr in graph.neighbors(musical)
            if graph.nodes[nbr].get('type') == 'album_link'
        ]
        if album_links:
            count_with_links += 1
    print(f"Musicals with at least 1 link: {count_with_links} from {len(musical_nodes)}")

    print(f"Nods of albums with links: {count_with_links}")


if __name__ == "__main__":
    g = load_graph()
    check_album_link_nodes(g)
    check_musical_album_links(g)
