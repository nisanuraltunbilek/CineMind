import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime


class Charts:

    @staticmethod
    def genre_chart(genres):

        labels = []
        values = []

        for genre, total in genres:
            labels.append(genre)
            values.append(total)

        plt.figure(figsize=(8, 8))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Favori Film Türleri")
        plt.axis("equal")
        plt.show()


    @staticmethod
    def dashboard(genres, directors, actors, imdb_scores, watch_dates):

        fig = plt.figure(figsize=(15, 10))

        # Tür Grafiği
        ax1 = plt.subplot(2, 2, 1)

        genre_labels = [g[0] for g in genres]
        genre_values = [g[1] for g in genres]

        ax1.pie(
            genre_values,
            labels=genre_labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax1.set_title("🎭 Tür Dağılımı")

        # Yönetmen Grafiği
        ax2 = plt.subplot(2, 2, 2)

        director_labels = [d[0] for d in directors]
        director_values = [d[1] for d in directors]

        ax2.bar(director_labels, director_values)

        ax2.set_title("🎥 Yönetmenler")
        ax2.tick_params(axis="x", rotation=30)

        # Oyuncu Grafiği
        ax3 = plt.subplot(2, 2, 3)

        actor_labels = [a[0] for a in actors]
        actor_values = [a[1] for a in actors]

        ax3.barh(actor_labels, actor_values)

        ax3.set_title("🎭 Oyuncular")

        plt.tight_layout()
        plt.show()

        # 4. Grafik - IMDb Histogramı
        ax4 = plt.subplot(2, 2, 4)

        ax4.hist(
        imdb_scores,
        bins=8
)

        ax4.set_title("⭐ IMDb Dağılımı")
        ax4.set_xlabel("IMDb")
        ax4.set_ylabel("Film Sayısı")

        # Tarihleri aylara göre grupla
        months = []

        for date in watch_dates:

            try:
               month = datetime.strptime(date, "%Y-%m-%d").strftime("%b")
               months.append(month)

            except:
               pass

        month_counts = Counter(months)

        month_order = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
         ]

        values = []

        for month in month_order:
           values.append(month_counts.get(month, 0))


        fig2 = plt.figure(figsize=(10,4))

        plt.plot(
           month_order,
           values,
           marker="o",
           linewidth=2
        )
  
        plt.title("📈 Aylara Göre İzleme")

        plt.xlabel("Ay")

        plt.ylabel("Film Sayısı")

        plt.grid(True)

        plt.show()