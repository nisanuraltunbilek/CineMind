import os
import pandas as pd
import requests
import re
from tmdbv3api import TMDb, Movie

from dotenv import load_dotenv

load_dotenv()

tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")


tmdb = TMDb()
tmdb.api_key = "2230e1b6000258d06dde6cc26ecec7d7"

CSV_FILE = "datasets/movies.csv"
POSTER_DIR = "assets/posters"

os.makedirs(POSTER_DIR, exist_ok=True)

def normalize(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9]+", "_", title)
    return title.strip("_") + ".jpg"

df = pd.read_csv(CSV_FILE)
titles = df["Series_Title"].dropna().unique()

movie_api = Movie()
count = 0

for title in titles:
    try:
        results = movie_api.search(title)

        if results:
            poster_path = results[0].poster_path

            if poster_path:
                url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                img = requests.get(url, timeout=10).content

                filename = normalize(title)
                path = os.path.join(POSTER_DIR, filename)

                with open(path, "wb") as f:
                    f.write(img)

                count += 1
                print(f"İndirildi: {title}")

    except Exception as e:
        print(f"Hata: {title} -> {e}")

print(f"Toplam {count} poster indirildi.")