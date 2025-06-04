import networkx as nx
import csv
import ast
import hashlib
import os
import pickle

# Функция для генерации уникального ID (хэш) по тексту
def get_hash_id(text, prefix):
    return f"{prefix}_{hashlib.md5(text.encode('utf-8')).hexdigest()}"

# Добавляет один мюзикл и все связанные узлы/рёбра в граф
def add_musical_to_graph(
    graph,
    title,
    release_date,
    genre,
    location,
    director,
    actors,
    characters,
    songs,
    album_link,
    time_period,
    composer,
    source_material,
    plot,
    quote
):
    title = title or "Unknown"
    musical_node = f"MUSICAL: {title}"
    graph.add_node(musical_node, type='musical', release_date=release_date)
    print(f"✅ Added musical: {musical_node}")


    # Жанры
    for g in genre:
        graph.add_node(g, type='genre')
        graph.add_edge(musical_node, g, relationship='has_genre')

    # Актёры
    for actor in actors:
        graph.add_node(actor, type='actor')
        graph.add_edge(musical_node, actor, relationship='features_actor')

    # Режиссёр
    if director:
        graph.add_node(director, type='director')
        graph.add_edge(musical_node, director, relationship='directed_by')

    # Дата релиза (или просто год)
    if release_date:
        graph.add_node(str(release_date), type='date')
        graph.add_edge(musical_node, str(release_date), relationship='released_on')

    # Локация («место действия»)
    # Локации
    for loc in location:
        if loc:
            graph.add_node(loc, type='place')
            graph.add_edge(musical_node, loc, relationship='set_in')


    # Композитор
    if composer:
        graph.add_node(composer, type='composer')
        graph.add_edge(musical_node, composer, relationship='created_music_for')

    # Источник (по мотивам чего)
    if source_material:
        graph.add_node(source_material, type='source_material')
        graph.add_edge(musical_node, source_material, relationship='is_based_on_source')

    # Персонажи
    for character in characters:
        if character:
            graph.add_node(character, type='character')
            graph.add_edge(musical_node, character, relationship='features_character')

    # Песни
    for song in songs:
        if isinstance(song, str) and song.strip():
            song_node = f"song::{song.strip()}"
            graph.add_node(song_node, type='song', text=song.strip())
            graph.add_edge(musical_node, song_node, relationship='has_song')

    # Ссылка на Spotify (или любой другой ресурс)
    if album_link:
        graph.add_node(album_link, type='link')
        graph.add_edge(musical_node, album_link, relationship='has_music_link')

    # Временной период действия
    if time_period:
        graph.add_node(time_period, type='time_period')
        graph.add_edge(musical_node, time_period, relationship='set_in_time_period')

    # Сюжет (plot) — может быть строкой или списком строк
    if isinstance(plot, list):
        for plot_text in plot:
            if isinstance(plot_text, str) and plot_text.strip():
                plot_id = get_hash_id(plot_text, "plot")
                graph.add_node(plot_id, type='plot', text=plot_text.strip())
                graph.add_edge(musical_node, plot_id, relationship='has_plot')
    else:
        if isinstance(plot, str) and plot.strip():
            plot_id = get_hash_id(plot, "plot")
            graph.add_node(plot_id, type='plot', text=plot.strip())
            graph.add_edge(musical_node, plot_id, relationship='has_plot')

    # Цитаты (quote) — предполагается, что это список строк
    for q in quote:
        if isinstance(q, str) and q.strip():
            quote_node = f"quote::{q.strip()[:30]}"
            graph.add_node(quote_node, type='quote', text=q.strip())
            graph.add_edge(musical_node, quote_node, relationship='has_quote')

    print(f"✅ Added musical: {title}")

def load_musicals_to_graph(csv_file):
    G = nx.Graph()
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('imdb_title') or row.get('title')
            release_date = row.get('release_date', '')

            # Жанры
            raw_genres = row.get('genres', '')
            try:
                genre = ast.literal_eval(raw_genres) if raw_genres.startswith('[') else [raw_genres]
            except Exception:
                genre = [raw_genres]

            # Локации
            raw_locations = row.get('locations', '')
            try:
                location = ast.literal_eval(raw_locations) if raw_locations.startswith('[') else [raw_locations]
            except Exception:
                location = [raw_locations]

            # Режиссёры
            raw_directors = row.get('directors', '')
            try:
                directors = ast.literal_eval(raw_directors) if raw_directors.startswith('[') else [raw_directors]
            except Exception:
                directors = [raw_directors]
            director = directors[0] if directors else ""

            # Актёры
            raw_actors = row.get('actors', '')
            try:
                actors = ast.literal_eval(raw_actors) if raw_actors.startswith('[') else [raw_actors]
            except Exception:
                actors = [raw_actors]

            # Персонажи
            raw_characters = row.get('characters', '')
            try:
                characters = ast.literal_eval(raw_characters) if raw_characters.startswith('[') else [raw_characters]
            except Exception:
                characters = [raw_characters]

            # Песни
            raw_songs = row.get('songs', '')
            try:
                songs = ast.literal_eval(raw_songs.replace("‘", "'").replace("’", "'")) if raw_songs.startswith('[') else [raw_songs]
            except Exception:
                songs = [raw_songs]

            # Ссылка на музыку
            spotify_link = row.get('spotify_link', '')

            # Временной период, композитор и источник
            time_period     = row.get('time_period', '')
            composer        = row.get('composer', '')
            source_material = row.get('source_material', '')

            # Сюжет
            raw_plot = row.get('plot', '')
            try:
                plot = ast.literal_eval(raw_plot) if raw_plot.startswith('[') else raw_plot
            except Exception:
                plot = raw_plot

            # Цитаты
            raw_quote = row.get('quote', '')
            try:
                quote = ast.literal_eval(raw_quote) if raw_quote.startswith('[') else [raw_quote]
            except Exception:
                quote = [raw_quote]

            # Добавление в граф
            add_musical_to_graph(
                G,
                title,
                release_date,
                genre,
                location,
                director,
                actors,
                characters,
                songs,
                spotify_link,
                time_period,
                composer,
                source_material,
                plot if isinstance(plot, list) else [plot],
                quote
            )

    return G

def add_weighted_edges_between_musicals(graph, attribute_types):
    musical_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('type') == 'musical']
    print(f"[DEBUG] Found {len(musical_nodes)} musical nodes")

    for i, m1 in enumerate(musical_nodes):
        attrs1 = {t: set() for t in attribute_types}
        for t in attribute_types:
            for nbr in graph.neighbors(m1):
                if graph.nodes[nbr].get('type') == t:
                    attrs1[t].add(nbr)

        for m2 in musical_nodes[i+1:]:
            attrs2 = {t: set() for t in attribute_types}
            for t in attribute_types:
                for nbr in graph.neighbors(m2):
                    if graph.nodes[nbr].get('type') == t:
                        attrs2[t].add(nbr)

            common_count = sum(len(attrs1[t].intersection(attrs2[t])) for t in attribute_types)
            if common_count > 0:
                print(f"[DEBUG] Adding edge between {m1} and {m2} with weight {common_count}")
                graph.add_edge(m1, m2, weight=common_count)

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(root, "output", "output.csv")

    print(f"[INFO] Loading musicals from {csv_path} into graph …")
    G = load_musicals_to_graph(csv_path)

    # Добавляем ребра с весами
    add_weighted_edges_between_musicals(G, [
        'genre', 'actor', 'director', 'composer', 'character', 'time_period', 'place', 'source_material'
    ])

    print(f"[INFO] Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    out_graph = os.path.join(root, "output", "musical_graph.gpickle")
    with open(out_graph, 'wb') as f:
        pickle.dump(G, f)
    print(f"[INFO] Graph saved as {out_graph}")

