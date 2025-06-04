import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import wikipedia
from imdb import IMDb
import spacy
import csv

wikipedia.set_lang("en")
nlp = spacy.load("en_core_web_sm")
ia = IMDb()

# -----------------------------
# Wikipedia parsing
# -----------------------------
def get_wikipedia_info(title: str) -> dict:
    try:
        page = wikipedia.page(title)
        content = page.content

        composer_match = re.search(
            r"[Mm]usic by ([A-Z][\w\-\’é]+(?: [A-Z][\w\-\’é]+)+)", content)
        composer = composer_match.group(1) if composer_match else "Unknown"

        source_match = re.search(
            r"(?:based on|adapted from).*?novel.*?by ([A-Z][\w\-\’é]+(?: [A-Z][\w\-\’é]+)*)",
            content,
            re.IGNORECASE
        )
        source_material = f"Novel by {source_match.group(1)}" if source_match else "Unknown"

        return {"composer": composer, "source_material": source_material}

    except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
        return {"composer": "Unknown", "source_material": "Unknown"}


def get_songs_from_wikipedia(title: str) -> list:
    url_title = title.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{url_title}"

    response = requests.get(url)
    if response.status_code != 200:
        return ["Unknown"]

    soup = BeautifulSoup(response.text, "html.parser")

    section_titles = ["Musical numbers", "Soundtrack", "Track listing", "Songs"]
    songs = []
    found_section = False

    for tag in soup.find_all(['h2', 'h3', 'ul', 'ol', 'div']):
        if tag.name in ['h2', 'h3']:
            header_text = tag.get_text().strip()
            if any(section in header_text for section in section_titles):
                found_section = True
                continue

        if found_section:
            if tag.name in ['h2', 'h3']:
                break
            if tag.name in ['ul', 'ol', 'div']:
                for li in tag.find_all('li'):
                    text = li.get_text(strip=True)
                    match = re.match(r'["“](.*?)["”]', text)
                    songs.append(match.group(1) if match else text)

    return songs if songs else ["Unknown"]


# -----------------------------
# Time and Location extraction
# -----------------------------
def extract_time_period(text):
    if not text or not isinstance(text, str):
        return "Unknown"

    patterns = [
        r'\b\d{1,2}(st|nd|rd|th)?-century\b',
        r'\b(1[5-9]|20|21)(st|nd|rd|th)?\s*century\b',
        r'\b(19|18|17|20)\d{2}s\b',
        r'\b(during|in|around)\s+(World War I|World War II|Cold War)\b',
        r'\b(medieval|renaissance|victorian|industrial|modern|future|ancient)\s+era\b',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return "Unknown"


def extract_location(text):
    if not text or not isinstance(text, str):
        return ["Unknown"]

    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    return list(set(locations)) if locations else ["Unknown"]


# -----------------------------
# IMDb parsing
# -----------------------------
def get_imdb_info(title: str) -> dict:
    results = ia.search_movie(title)
    if not results:
        return {
            "imdb_title": None,
            "release_date": None,
            "directors": [],
            "genres": [],
            "actors": [],
            "characters": [],
            "plot": [],
            "time_period": "Unknown",
            "location": ["Unknown"]
        }

    movie = results[0]
    ia.update(movie, info=['main', 'plot'])  

    raw_plot_list = movie.get("plot") or []
    plot_text = raw_plot_list[0] if raw_plot_list and isinstance(raw_plot_list[0], str) else ""

    time_period = extract_time_period(plot_text)
    location = extract_location(plot_text)

    return {
        "imdb_title": movie.get("title"),
        "release_date": movie.get("year"),
        "directors": [d["name"] for d in movie.get("directors", [])],
        "genres": movie.get("genres", []),
        "actors": [a["name"] for a in movie.get("cast", [])[:5]],
        "characters": [
            str(a.currentRole) if a.currentRole else None
            for a in movie.get("cast", [])[:5]
        ],
        "plot": raw_plot_list,
        "time_period": time_period,
        "location": location
    }


# -----------------------------
# process_row для process_musicals()
# -----------------------------
def process_row(title):
    try:
        imdb_data = get_imdb_info(title)
        wiki_data = get_wikipedia_info(title)
        songs = get_songs_from_wikipedia(title)
    except Exception as e:
        print(f"[WARN] Error processing {title}: {e}")
        imdb_data = {}
        wiki_data = {}
        songs = ["Unknown"]

    songs_text = "; ".join(songs) if songs and songs != ["Unknown"] else "Unknown"
    return {
        **imdb_data,
        **wiki_data,
        "songs": songs_text
    }


# -----------------------------
# process_musicals (без дублей и с логами)
# -----------------------------
def process_musicals(input_file, output_file, critic_file, limit=5):
    results = []
    seen_ids = set()  

    critic_quotes = {}
    with open(critic_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie_id = row['movieId'].strip()
            quote = row['quote'].strip()
            if movie_id and quote and movie_id not in critic_quotes:
                critic_quotes[movie_id] = quote

    print(f"[INFO] Start preprocessing the file {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            title = row['movieTitle'].strip()
            movie_id = row['movieId'].strip()

            if movie_id in seen_ids:
                print(f"[SKIP] Double {movie_id} («{title}»)")
                continue

            print(f"[INFO] Processing ({i}) «{title}» (ID={movie_id})")
            seen_ids.add(movie_id)

            data = process_row(title)
            if not data:
                print(f"[WARN] process_row returns None for «{title}», skip.")
                continue

            data['id'] = len(results) + 1
            data['movieId'] = movie_id
            data['quote'] = critic_quotes.get(movie_id, '')

            results.append(data)
            print(f"[OK] Added «{title}» ({len(results)})")

    all_keys = set()
    for r in results:
        all_keys.update(r.keys())
    fieldnames = ['id', 'movieId'] + sorted(k for k in all_keys if k not in ['id', 'movieId'])

    with open('output/output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for idx, row in enumerate(results, start=1):
            for key, value in row.items():
                if isinstance(value, list):
                    row[key] = ", ".join(map(str, value))

            writer.writerow(row)

