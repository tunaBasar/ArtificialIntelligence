# BLG 307 Yapay Zeka Sistemleri Ders Projeleri

Ad Soyad: Hilmi Tunahan BAŞAR
Okul No: 2112721019
Dönem: 2025-2026 Güz

Bu depo, Yapay Zeka Sistemleri dersi için hazırladığım iki adet proje ödevini içermektedir. Okul numaramın son hanesi 9 olduğu için her iki projede de Senaryo 9 seçilmiştir.

Dosya Yapısı:
- HomeWork1: Genetik Algoritma Projesi
- HomeWork2: Karınca Kolonisi Algoritması (ACO) Projesi

---

# HomeWork1: Genetik Algoritma ile Optimizasyon

Bu klasörde, Senaryo 9 (Öğrenci Etüt Programı Planlaması) konusu ele alınmıştır. Bir öğrencinin Matematik ve Fen derslerine ayıracağı süreyi optimize ederek en yüksek sınav başarı skorunu elde etmesi hedeflenmiştir.

Senaryo Detayları:
Amaç Fonksiyonu: y = 4x1 + 5x2 - 0.5(x1^2) - 0.2(x2^2)
x1: Matematik etüt süresi (0-10 saat)
x2: Fen etüt süresi (0-10 saat)

Kısıtlar:
Toplam çalışma süresi 12 saati geçemez.
Fen dersine en az 2 saat çalışılmalıdır.

Klasör içerisindeki kodlar çalıştırıldığında popülasyonun değişimi ve en iyi uygunluk değerinin grafiği oluşturulmaktadır.

---

# HomeWork2: Karınca Kolonisi Algoritması (ACO) ile Rota Optimizasyonu

Bu klasörde, Senaryo 9 (Kitap Dağıtımı Rota Planlaması) konusu işlenmiştir. Isparta İl Milli Eğitim Müdürlüğü'nden başlayarak belirlenen 15 farklı okula kitap dağıtımı yapacak bir aracın en kısa rotası hesaplanmaktadır.

Proje Özellikleri:
- Arayüz için Streamlit kütüphanesi kullanıldı.
- Okullar arası gerçek mesafe verileri Google Maps Distance Matrix API ile çekildi.
- Okul isimlerinin koordinata çevrilmesi için Geocoding API kullanıldı.
- Sonuç rota harita üzerinde görselleştirildi.

Kurulum ve Çalıştırma:

1. Gerekli kütüphanelerin yüklenmesi:
Terminalde HomeWork2 klasörüne gidip aşağıdaki komutu çalıştırın:
pip install -r requirements.txt

2. API Anahtarı Ayarı:
Projenin çalışabilmesi için Google Maps API anahtarı gereklidir. HomeWork2 klasörünün içinde .streamlit adında bir klasör oluşturun. Bu klasörün içine secrets.toml adında bir dosya açın ve anahtarınızı şu formatta kaydedin:
GOOGLE_API_KEY = "BURAYA_API_ANAHTARINIZI_YAZIN"

Not: API anahtarı güvenlik nedeniyle GitHub'a yüklenmemiştir. Projeyi test ederken kendi anahtarınızı eklemeniz gerekmektedir.

3. Uygulamanın Başlatılması:
Ayarlar yapıldıktan sonra terminale şu komutu yazarak arayüzü başlatabilirsiniz:
streamlit run main.py
