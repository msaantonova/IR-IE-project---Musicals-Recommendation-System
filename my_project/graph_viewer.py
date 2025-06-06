import networkx as nx
import pickle
import matplotlib.pyplot as plt
import os

root = os.path.dirname(os.path.dirname(__file__))  
in_graph = os.path.join(root, "output", "musical_graph.gpickle")

with open(in_graph, 'rb') as f:
    G = pickle.load(f)

print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.15, iterations=20)  
nx.draw(G, pos, node_size=50, node_color='skyblue', edge_color='gray', with_labels=False)
plt.title("Musical Graph Visualization")
plt.show()
