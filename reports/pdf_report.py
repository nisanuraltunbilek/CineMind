from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFReport:

    @staticmethod
    def create(filename, repo):

        styles = getSampleStyleSheet()

        pdf = SimpleDocTemplate(filename)

        story = []

        story.append(Paragraph("<b>CineMind Film Raporu</b>", styles["Title"]))

        story.append(
            Paragraph(
                f"Toplam Film: {repo.get_total_movies()}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Favori Film: {repo.get_favorite_count()}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Ortalama Kullanıcı Puanı: {repo.get_average_rating()}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Ortalama IMDb: {repo.get_average_imdb()}",
                styles["Normal"]
            )
        )

        pdf.build(story)

        print("\n✅ PDF başarıyla oluşturuldu.")