# 🎬 CineMind

## Yapay Zekâ Destekli Kişisel Film Arşivi, Öneri ve Analiz Platformu

CineMind, sinemaseverlerin izledikleri filmleri tek bir platformda arşivleyebilmesi, puanlayabilmesi, favorilerine ayırabilmesi ve yapay zekâ destekli kişiselleştirilmiş öneriler alabilmesi amacıyla geliştirilen modern bir web uygulamasıdır.

Proje; **Python, Streamlit ve SQLite** teknolojileri kullanılarak geliştirilmiş olup kullanıcı deneyimini artırmak için sinematik bir arayüz, dinamik öneri sistemi, maraton planlayıcı ve istatistiksel analiz ekranları içermektedir.

---

## 🎯 Proje Amacı

Bu proje aşağıdaki ihtiyaçları karşılamak amacıyla geliştirilmiştir:

* Kullanıcının film geçmişini düzenli şekilde saklamak
* İzleme alışkanlıklarını analiz etmek
* Tür, yönetmen ve puan tercihlerini anlamlandırmak
* Yapay zekâ ile kişiselleştirilmiş film önerileri sunmak
* Film izleme deneyimini oyunlaştırılmış özelliklerle daha eğlenceli hâle getirmek

---

## ✨ Uygulama Özellikleri

### 🔍 Akıllı Film Arama

* Film adına göre arama
* IMDb puanı, tür, yönetmen ve oyuncu bilgilerini görüntüleme
* Poster görseli çekme
* Tek tıkla fragman sayfasına yönlendirme

### 📚 Kişisel Film Kütüphanesi

* Film ekleme / silme
* Puan verme
* İzlenme tarihi kaydetme
* Favorilere ekleme
* Favori filmleri pembe parıltı efektiyle vurgulama

### 🤖 AI Film Öneri Sistemi

* Kullanıcının beğendiği filmleri analiz eder
* Benzer tür ve yönetmenlere göre öneriler üretir
* Tek tıkla önerilen filmi kütüphaneye ekleme

### 📊 Gelişmiş Dashboard

* Yıllık izleme özeti
* Ortalama puan analizi
* Tür dağılımı grafiği
* En çok izlenen yönetmenler
* Oyuncu yoğunluğu analizi
* İzleme zaman çizelgesi

### 🍿 Film Maraton Sistemi

* Tematik maraton oluşturma (ör. Christopher Nolan Serisi)
* Günlük izleme planı
* Tamamlanan filmleri işaretleme
* İlerleme çubuğu ile takip

### 🏅 Rozet ve Başarı Sistemi

* Gece Kuşu
* Koleksiyoncu
* Maratoncu
* Arşivci

Kullanıcının izleme alışkanlıklarına göre otomatik rozet kazanımı sağlar.

### 🌙 Sinematik Arayüz

* Mor / lacivert gece teması
* Parallax yıldız arka planı
* Hover animasyonları
* Glow efektleri
* Cam (glassmorphism) kart tasarımı

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji         | Amaç                    |
| ----------------- | ----------------------- |
| **Python**        | Ana uygulama dili       |
| **Streamlit**     | Web arayüzü             |
| **SQLite**        | Yerel veritabanı        |
| **Pandas**        | Veri işleme             |
| **Matplotlib**    | Grafik üretimi          |
| **TMDb API**      | Poster ve film verileri |
| **python-dotenv** | API anahtarı yönetimi   |

---

## 📂 Proje Yapısı

```text
CineMind/
│
├── app.py
├── pages/
│   ├── Search.py
│   ├── Library.py
│   ├── AI.py
│   └── Dashboard.py
│
├── database/
├── recommender/
├── utils/
├── assets/
│   └── posters/
├── data/
├── datasets/
└── README.md
```

---

## 🚀 Kurulum

Depoyu bilgisayarınıza klonlayın:

```bash
git clone https://github.com/nisanuraltunbilek/CineMind.git
cd CineMind
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

Proje kök dizininde `.env` dosyası oluşturun:

```text
TMDB_API_KEY=your_api_key_here
```

Uygulamayı çalıştırın:

```bash
streamlit run app.py
```

Tarayıcıda açılan adres üzerinden uygulamayı kullanabilirsiniz.

---

## 📸 Ekran Görüntüleri

Aşağıdaki ekran görüntüleri uygulamanın temel modüllerini göstermektedir:

* Ana sayfa
* Film arama ekranı
* Kütüphane ekranı
* AI öneri ekranı
* Dashboard ekranı
* Maraton sistemi

---

## 🔐 Güvenlik

API anahtarları güvenlik nedeniyle GitHub deposuna eklenmemiştir. Uygulamayı çalıştırmak için kendi **TMDb API** anahtarınızı `.env` dosyasına tanımlamanız gerekir.

---

## 💡 Geliştirme Sürecinde Uygulanan Özellikler

Bu proje kapsamında ayrıca:

* Dinamik giriş serisi
* Günün önerisi sistemi
* Rastgele film ruleti
* Daha sonra izle listesi
* Favori filtreleme
* Açılır / kapanır film listesi
* Responsive kart düzeni
* Sidebar otomatik kapatma davranışı

gibi kullanıcı deneyimini iyileştiren ek özellikler geliştirilmiştir.

---

## 🎓 Akademik ve Staj Kapsamı

Bu çalışma, yazılım geliştirme stajı kapsamında hazırlanmış olup;

* kullanıcı arayüzü tasarımı,
* veritabanı yönetimi,
* API entegrasyonu,
* veri analizi,
* öneri sistemleri,
* kullanıcı etkileşimi tasarımı

konularında uygulamalı geliştirme deneyimi kazandırmayı hedeflemektedir.

---

## 👩‍💻 Geliştirici

**Nisanur Altunbilek**

Bilgisayar Mühendisliği Öğrencisi

GitHub: https://github.com/nisanuraltunbilek
