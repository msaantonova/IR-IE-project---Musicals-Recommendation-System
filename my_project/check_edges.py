import networkx as nx
import pickle

graph_path = "output/musical_graph.gpickle"

with open(graph_path, 'rb') as f:
    G = pickle.load(f)

musical_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'musical']

print("Edges between musical nodes:")
for u, v in G.edges():
    if u.startswith("MUSICAL:") and v.startswith("MUSICAL:"):
        print(f"{u} <-> {v}")

print("\nEdges where at least 1 is Musical:")
for u, v in G.edges():
    if u.startswith("MUSICAL:") or v.startswith("MUSICAL:"):
        print(f"{u} <-> {v}")

print("\nNumber of musical nodes:", len(musical_nodes))

