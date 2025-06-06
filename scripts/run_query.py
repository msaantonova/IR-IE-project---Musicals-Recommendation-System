import networkx as nx
from my_project.search import sort_musicals_query  
import pickle

def load_graph(path="output/musical_graph.gpickle"):
    with open(path, "rb") as f:
        return pickle.load(f)

def get_album_link(graph, musical_node):
    album_links = [
        nbr for nbr in graph.neighbors(musical_node)
        if graph.nodes[nbr].get('type') == 'album_link'
    ]
    if album_links:
        album_node = album_links[0]
        album_data = graph.nodes[album_node]
        return album_data.get("album_url") or album_data.get("album_link") or album_node
    else:
        return "—"


def main():
    graph = load_graph()

    print("🎭 Musical Recommender 🎶")
    print("Enter your ideas (Example: love, 1950s):")

    while True:
        try:
            query = input("🔍 Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 See you later!")
            break

        if not query:
            print("Exit.")
            break

        results = sort_musicals_query(graph, query)
        if not results:
            print("⚠️ Nothing found, try other ideas.")
            continue

        main_rec = results[0]
        also_like = results[1:3]

        album_link = get_album_link(graph, main_rec)

        print("\n🎯 Your best match:")
        print(f"• {main_rec} → Album: {album_link}")

        if also_like:
            print("\n💡 You might also like:")
            for alt in also_like:
                alt_url = get_album_link(graph, alt)  
                line = f"• {alt}"                      
                if alt_url != "—":                    
                    line += f" → Album: {alt_url}"    
                print(line)                          



        print("\n" + "—" * 30)

if __name__ == "__main__":
    main()
 