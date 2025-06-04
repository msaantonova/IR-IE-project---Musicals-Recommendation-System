import networkx as nx
import matplotlib.pyplot as plt
import pickle

graph_path = "output/musical_graph.gpickle"

with open(graph_path, 'rb') as f:
    G = pickle.load(f)

print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Функция для фильтрации узлов по типу
def filter_nodes_by_type(graph, node_type):
    return [n for n, attr in graph.nodes(data=True) if attr.get('type') == node_type]

musical_nodes = filter_nodes_by_type(G, 'musical')

# Ограничимся первыми 50 музыкальными узлами
sub_nodes = musical_nodes[:50]
subgraph = G.subgraph(sub_nodes)

degree_dict = dict(subgraph.degree())
print("Degree of nodes in subgraph:")
for node, deg in degree_dict.items():
    # Попытка получить читаемое имя из атрибутов
    name = G.nodes[node].get('name') or G.nodes[node].get('title') or str(node)
    print(f"MUSICAL: {name}: {deg}")

# Визуализация подграфа
pos = nx.spring_layout(subgraph, k=0.3, iterations=30)
plt.figure(figsize=(12, 12))
nx.draw_networkx_nodes(subgraph, pos, node_size=200, node_color='lightgreen')
nx.draw_networkx_edges(subgraph, pos, alpha=0.5)
nx.draw_networkx_labels(subgraph, pos, font_size=10)

plt.title("Visualization of Musical Nodes Subgraph")
plt.axis('off')
plt.show()


