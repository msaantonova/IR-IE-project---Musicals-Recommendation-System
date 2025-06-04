import networkx as nx
import pickle

graph_path = "output/musical_graph.gpickle"

with open(graph_path, 'rb') as f:
    G = pickle.load(f)

musical_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'musical']

print("Пары рёбер между музыкальными узлами:")
for u, v in G.edges():
    if u.startswith("MUSICAL:") and v.startswith("MUSICAL:"):
        print(f"{u} <-> {v}")

print("\nРёбра, где хотя бы одна вершина — музыкальная:")
for u, v in G.edges():
    if u.startswith("MUSICAL:") or v.startswith("MUSICAL:"):
        print(f"{u} <-> {v}")

print("\nКоличество музыкальных узлов:", len(musical_nodes))

