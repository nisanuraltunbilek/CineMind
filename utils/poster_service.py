from pathlib import Path
import re

POSTER_DIR = Path("assets/posters")

def normalize(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^a-z0-9]+", "_", title)
    title = title.strip("_")
    return title + ".jpg"

def get_poster(title: str):

    if not title:
        return None

    filename = normalize(title)
    path = POSTER_DIR / filename

    if path.exists():
        return str(path)

    return None