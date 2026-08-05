from database.user_repository import UserRepository
from database.repository import MovieRepository
from recommender.content_based import ContentBasedRecommender
from visualization.charts import Charts
from reports.pdf_report import PDFReport
from database.database import Database

db = Database()
db.initialize()


def film_ekle(repo):

    print("\n===== Film Ekle =====")

    movie_title = input("Film adı: ").strip()

    if movie_title == "":
        print("❌ Film adı boş olamaz.")
        return

    try:
        user_rating = float(input("Puan (1-10): "))
    except ValueError:
        print("❌ Geçersiz puan.")
        return

    favorite = input("Favori mi? (E/H): ").strip().upper()

    watch_date = input("İzleme tarihi: ")

    movie_repo = MovieRepository()

    bulunanlar = movie_repo.find_by_title(movie_title)

    if not bulunanlar:
      print("\n❌ Bu film veri setinde bulunamadı.")
      return

    film = bulunanlar[0]

    if repo.movie_exists(film.title):

       print("\n❌ Bu film zaten kütüphanende mevcut.\n")
       return

    print(f"\nFilm bulundu: {film.title} ({film.year})")
    print(f"Tür: {film.genre}")
    print(f"Yönetmen: {film.director}")
    print(f"IMDb: {film.imdb}")
    
    repo.add_movie(
        film.title,
        film.genre,
        film.director,
        film.actors,
        film.imdb,
        user_rating,
        1 if favorite == "E" else 0,
        watch_date
)
    print("\n✅ Film başarıyla eklendi.\n")


def kutuphaneyi_goster(repo):

    print("\n========== KÜTÜPHANEM ==========\n")

    movies = repo.get_all_movies()

    if not movies:
        print("Henüz film eklenmedi.\n")
        return

    for movie in movies:

       title, genre, director, imdb, rating, fav, date = movie

       fav_text = "⭐" if fav else "-"

       print(
          f"🎬 {title} ({imdb})\n"
          f"🎭 Tür: {genre}\n"
          f"🎥 Yönetmen: {director}\n"
          f"⭐ Senin Puanın: {rating}\n"
          f"❤️ Favori: {fav_text}\n"
          f"📅 İzleme Tarihi: {date}\n"
)



def film_oner(repo):

    recommender = ContentBasedRecommender()

    movies = repo.get_all_movies()

    if not movies:
        print("\nÖnce kütüphanene film eklemelisin.\n")
        return

    watched_movies = []

    for movie in movies:
        watched_movies.append(movie.movie_title)

    recommendations = recommender.recommend_for_user(
        watched_movies
    )

    print("\n========== SENİN İÇİN ÖNERİLER ==========\n")

    if not recommendations:
        print("Öneri bulunamadı.\n")
        return

    for i, film in enumerate(recommendations[:10], start=1):

      print(
         f"🎬 {i}. {film['Series_Title']} ({film['Released_Year']})\n"
         f"🎭 Tür: {film['Genre']}\n"
         f"🎥 Yönetmen: {film['Director']}\n"
         f"⭐ IMDb: {film['IMDB_Rating']}\n"
    )

    print()


def film_sil(repo):

    movie = input("Silinecek film: ").strip()

    deleted = repo.delete_movie(movie)

    if deleted:
        print("\n✅ Film silindi.\n")
    else:
        print("\n❌ Film bulunamadı.\n")


def film_ara():

    repo = MovieRepository()

    print("\n========== GELİŞMİŞ FİLM ARAMA ==========\n")
    print("1 - Film Adına Göre")
    print("2 - Türe Göre")
    print("3 - Yönetmene Göre")
    print("4 - IMDb Puanına Göre")
    print("5 - Yıla Göre")

    secim = input("\nSeçimin: ").strip()

    if secim == "1":

        kelime = input("Film adı: ").strip()
        bulunanlar = repo.find_by_title(kelime)

    elif secim == "2":

        tur = input("Tür: ").strip()
        bulunanlar = repo.find_by_genre(tur)

    elif secim == "3":

        yonetmen = input("Yönetmen: ").strip()
        bulunanlar = repo.find_by_director(yonetmen)

    elif secim == "4":

        try:
            imdb = float(input("Minimum IMDb: "))
        except ValueError:
            print("Geçersiz puan.")
            return

        bulunanlar = repo.find_by_imdb(imdb)

    elif secim == "5":

        try:
            yil = int(input("Yıl: "))
        except ValueError:
            print("Geçersiz yıl.")
            return

        bulunanlar = repo.find_by_year(yil)

    else:
        print("Geçersiz seçim.")
        return

    print("\n========== SONUÇLAR ==========\n")

    if not bulunanlar:
        print("Film bulunamadı.\n")
        return

    for film in bulunanlar:

        print(
            f"🎬 {film.title} ({film.year})\n"
            f"🎭 Tür: {film.genre}\n"
            f"🎥 Yönetmen: {film.director}\n"
            f"⭐ IMDb: {film.imdb}\n"
        )

        ekle = input("📌 İzleme listesine eklensin mi? (E/H): ").strip().upper()

        if ekle == "E":

            repo_user = UserRepository()

            repo_user.add_to_watchlist(
                film.title,
                film.genre,
                film.director,
                film.imdb
            )

            print("✅ İzleme listesine eklendi.\n")

def bugun_ne_izlesem():

       repo = MovieRepository()

       movie = repo.random_movie()

       if movie is None:
           print("Film bulunamadı.")
           return

       print("\n========== 🎲 BUGÜN NE İZLESEM? ==========\n")

       print(
            f"🎬 {movie.title} ({movie.year})\n"
            f"🎭 Tür: {movie.genre}\n"
            f"🎥 Yönetmen: {movie.director}\n"
            f"⭐ IMDb: {movie.imdb}\n"
      )

       print("🍿 İyi seyirler!\n")

def watchlist_goster(repo):

        print("\n========== 🎬 İZLEME LİSTEM ==========\n")

        movies = repo.get_watchlist()

        if not movies:
           print("İzleme listesi boş.\n")
           return

        for movie in movies:

           title, genre, director, imdb = movie

           print(
               f"🎬 {title}\n"
               f"🎭 Tür: {genre}\n"
               f"🎥 Yönetmen: {director}\n"
               f"⭐ IMDb: {imdb}\n"
        )  


def istatistikler(repo):

    print("\n========== 📊 CİNEMIND İSTATİSTİKLERİ ==========\n")

    print(f"🎬 Toplam Film        : {repo.get_total_movies()}")

    print(f"⭐ Favori Film        : {repo.get_favorite_count()}")

    print(f"⭐ Ortalama Puan      : {repo.get_average_rating()}")

    print(f"📅 Son İzlenen Film   : {repo.get_last_movie()}")

    print(f"📆 Bu Ay İzlenen      : {repo.get_this_month_count()}")

    print(f"📅 Bu Yıl İzlenen     : {repo.get_this_year_count()}")

    print("\n🎭 En Çok İzlenen Türler\n")

    genres = repo.get_genre_statistics()

    for genre, total in genres:

      print(f"{genre} : {total}")


    print("\n🏆 En Yüksek Puan Verdiğin Filmler\n")

    top_movies = repo.get_top_rated_movies()

    for i, movie in enumerate(top_movies, start=1):

        print(
            f"{i}. {movie[0]} ⭐ {movie[1]}"
        )

    print()

    print("\n🎭 En Sevdiğin Türler\n")

    genres = repo.get_favorite_genres()

    for genre, total in genres:

       print(f"{genre} ({total} film)")

    print("\n🎥 En Sevdiğin Yönetmenler\n")

    directors = repo.get_favorite_directors()

    for director, total in directors:

       print(f"{director} ({total} film)")   

    print("\n🎭 En Çok İzlediğin Oyuncular\n")

    actors = repo.get_favorite_actors()

    for actor, total in actors:

       print(f"{actor} ({total} film)")


    print("\n⭐ İzlediğin Filmlerin Ortalama IMDb'si\n")

    avg_imdb = repo.get_average_imdb()

    print(f"{avg_imdb}\n")

    print("\n🤖 CİNEMIND AI ANALİZİ\n")

    genres = repo.get_favorite_genres()
    directors = repo.get_favorite_directors()
    actors = repo.get_favorite_actors()

    avg_imdb = repo.get_average_imdb()
    avg_user = repo.get_average_user_rating()

    if genres:
        print(f"🎭 En sevdiğin tür: {genres[0][0]}")

    if directors:
       print(f"🎥 Favori yönetmenin: {directors[0][0]}")

    if actors:
      print(f"⭐ En çok izlediğin oyuncu: {actors[0][0]}")
 
    print(f"\n⭐ Ortalama IMDb tercihin: {avg_imdb}")

    if avg_imdb >= 8:
      print("Kaliteli yapımları tercih ediyorsun.")
    elif avg_imdb >= 7:
       print("Popüler filmleri seviyorsun.")
    else:
       print("Farklı türlerde filmler izliyorsun.")

    print(f"\n🎬 Ortalama kullanıcı puanın: {avg_user}")

    if avg_user >= 8:
        print("İzlediğin filmleri seçerken oldukça seçicisin.")
    elif avg_user >= 6:
      print("Genel olarak izlediğin filmleri beğeniyorsun.")
    else:
       print("Filmleri değerlendirmede oldukça eleştirelsin.")

def grafikler(repo):
    genres = repo.get_favorite_genres()

    directors = repo.get_favorite_directors()

    actors = repo.get_favorite_actors()

    imdb_scores = repo.get_imdb_scores()

    watch_dates = repo.get_watch_dates()

    Charts.dashboard(
        genres,
        directors,
        actors,
        imdb_scores,
        watch_dates
    )

def pdf_olustur(repo):

    PDFReport.create(
        "CineMind_Report.pdf",
        repo
    )


def main():
    ...


def main():

    repo = UserRepository()

    while True:

        print("\n========== CineMind ==========\n")
        print("1 - Film Ekle")
        print("2 - Kütüphaneyi Göster")
        print("3 - Bana Öner")
        print("4 - Film Sil")
        print("5 - Film Ara")
        print("6 - İstatistikler")
        print("7 - İzleme Listem")
        print("8 - Bugün Ne İzlesem?")
        print("9 - 📊 Grafikler")
        print("10 - 📄 PDF Rapor Oluştur")
        print("0 - Çıkış")

        secim = input("\nSeçimin: ").strip()

        if secim == "1":
            film_ekle(repo)

        elif secim == "2":
            kutuphaneyi_goster(repo)

        elif secim == "3":
            film_oner(repo)

        elif secim == "4":
            film_sil(repo)

        elif secim == "5":
            film_ara()

        elif secim == "6":
              istatistikler(repo) 

        elif secim == "7":
              watchlist_goster(repo) 

        elif secim == "8":
              bugun_ne_izlesem()   

        elif secim == "9":
              grafikler(repo)  

        elif secim == "10":
              pdf_olustur(repo)

        elif secim == "0":
            print("\nGörüşürüz 👋")
            break

        else:
            print("\nGeçersiz seçim.\n")


if __name__ == "__main__":
    main()