import pandas as pd
from pathlib import Path

from database.database import Database


def main():

    project_root = Path(__file__).resolve().parent.parent

    csv_path = project_root / "datasets" / "movies.csv"

    df = pd.read_csv(csv_path)

    print("CSV Sütunları:")
    print(df.columns.tolist())

    database = Database()
    database.initialize()

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM movies")

    imported = 0

    for _, row in df.iterrows():

        # Yıl sayı değilse bu filmi atla
        try:
            year = int(row["Released_Year"])
        except ValueError:
            continue

        cursor.execute(
            """
            INSERT INTO movies
            (
                title,
                year,
                genre,
                director,
                actors,
                imdb,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["Series_Title"],
                year,
                row["Genre"],
                row["Director"],
                f"{row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}",
                float(row["IMDB_Rating"]),
                row["Overview"],
            ),
        )

        imported += 1

    connection.commit()
    connection.close()

    print(f"✅ {imported} film başarıyla aktarıldı.")


if __name__ == "__main__":
    main()