# Import library yang diperlukan
import requests  # Untuk mengambil data dari web
from bs4 import BeautifulSoup  # Untuk parsing HTML
from wordcloud import WordCloud  # Untuk membuat word cloud
import matplotlib.pyplot as plt  # Untuk visualisasi
import re  # Untuk operasi regex (pembersihan teks)
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory  # Stopword bahasa Indonesia

#Ambil HTML dari artikel Kompas
url = "https://money.kompas.com/read/2025/02/01/120000226/transaksi-kripto-indonesia-melonjak-4-kali-lipat-tembus-rp-650-61-triliun"
headers = {"User-Agent": "Mozilla/5.0"}  # Untuk menghindari pemblokiran bot
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

#Ambil isi teks artikel dari elemen <div class="read__content">
article = soup.find("div", class_="read__content")
text = " ".join([p.get_text() for p in article.find_all("p")]) if article else ""

#Bersihkan teks
# Menghapus karakter non-huruf dan mengubah semua ke huruf kecil
text = re.sub(r'[^a-zA-Z\s]', '', text).lower()

# Stopwords Bahasa Indonesia
# Kombinasi stopword dari Sastrawi + daftar tambahan manual
factory = StopWordRemoverFactory()
stopwords_indonesia = set(factory.get_stop_words() + [
    "dan", "yang", "di", "ke", "dari", "untuk", "dengan", "pada", "sebagai",
    "juga", "akan", "ini", "itu", "adalah", "dalam", "oleh", "karena", "tidak",
    "atau", "lebih", "telah", "tahun", "juta", "rp", "triliun", "meskipun", "selain", "menjadi", "bagi", "segi",
    "menunjukkan", "mencapai", "lagi", "kompascom", "dapat", "diperlukan", "menambahkan", "diharapkan", "serta",
    "masih", "bahwa", "katanya", "lalu", "baca", "empat", "sabtu", "bisa", "berada", "memberikan", "agar",
    "mudahkan", "termasuk", "dikutip", "menyebut", "harus", "berdasarkan", "baik", "iqbal", "hampir", "sebelumnya"
])

# Buat Word Cloud dengan konfigurasi estetika
wordcloud = WordCloud(
    width=1200,                # Lebar canvas
    height=600,                # Tinggi canvas
    background_color="white",  # Warna latar belakang
    colormap="viridis",        # Skema warna (alternatif: inferno, plasma, cool, Set2)
    stopwords=stopwords_indonesia,  # Daftar kata yang diabaikan
    collocations=False,        # Hindari kombinasi dua kata muncul sebagai satu
    contour_color='black',     # Garis tepi word cloud (jika pakai mask)
    contour_width=1            # Ketebalan garis tepi
).generate(text)               # Hasilkan word cloud dari teks yang telah dibersihkan

#visualisasi word cloud
plt.figure(figsize=(14, 7))  # Ukuran gambar yang ditampilkan
plt.imshow(wordcloud, interpolation="bilinear")  # Gambar word cloud
plt.axis("off")  # Hilangkan sumbu
plt.title("Word Cloud – Transaksi Kripto di Indonesia", fontsize=20, pad=20)  # Judul visualisasi
plt.tight_layout()  # Rapiin layout
plt.show()


#linechart
import requests  # Untuk mengirim HTTP request ke website
from bs4 import BeautifulSoup  # Untuk parsing konten HTML
from collections import Counter  # Untuk menghitung jumlah artikel per bulan
import datetime  # Untuk manipulasi tanggal
import matplotlib.pyplot as plt  # Untuk visualisasi data dalam bentuk grafik
import time  # Untuk memberikan jeda antar request (agar tidak diblokir)

# Kata kunci yang berkaitan dengan kripto
KEYWORDS = ["kripto", "crypto", "bitcoin", "ethereum", "blockchain", "eth", "xrp", "btc"]

artikel_per_bulan = Counter()  # Menyimpan jumlah artikel kripto untuk setiap bulan

# Menentukan rentang tanggal dari 1 Januari 2025 sampai 30 April 2025
start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 4, 30)
delta = datetime.timedelta(days=1)  # Interval per hari

# Header agar server mengira request berasal dari browser biasa
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

current_date = start_date  # Mulai dari tanggal awal

while current_date <= end_date:  # Loop selama masih dalam rentang tanggal
    tanggal_str = current_date.strftime("%Y-%m-%d")  # Format tanggal untuk URL
    bulan_str = current_date.strftime("%Y-%m")  # Format bulan untuk rekap
    url = f"https://indeks.kompas.com/?site=all&date={tanggal_str}"  # URL indeks berita harian

    print(f"Mengecek: {tanggal_str}")  # Tampilkan tanggal yang sedang dicek
    try:
        r = requests.get(url, headers=headers, timeout=10)  # Kirim request HTTP
        r.raise_for_status()  # Jika status bukan 200, munculkan exception
        soup = BeautifulSoup(r.text, 'lxml')  # Parsing konten HTML menggunakan lxml

        headlines = soup.find_all("h2", class_="articleTitle")  # Ambil semua judul artikel

        jumlah_berita_kripto = 0  # Inisialisasi jumlah artikel kripto untuk hari itu
        for h in headlines:
            judul = h.get_text(strip=True).lower()  # Ambil teks dan ubah ke huruf kecil
            if any(keyword in judul for keyword in KEYWORDS):  # Cek apakah judul mengandung kata kunci
                jumlah_berita_kripto += 1  # Tambah hitungan jika cocok

        if jumlah_berita_kripto > 0:  # Jika ada artikel kripto di hari tersebut
            artikel_per_bulan[bulan_str] += jumlah_berita_kripto  # Tambahkan ke total bulanan

        time.sleep(0.5)  # Jeda 0.5 detik agar tidak dianggap bot

    except Exception as e:  # Tangani error jika request gagal
        print(f"Gagal mengambil tanggal {tanggal_str}: {e}")

    current_date += delta  # Lanjut ke tanggal berikutnya

# Tampilkan hasil jumlah artikel kripto yang ditemukan per bulan
print("\nJumlah Berita Kripto per Bulan (2025):")
for bulan, total in sorted(artikel_per_bulan.items()):  # Urutkan berdasarkan bulan
    print(f"{bulan}: {total} artikel")  # Cetak hasil

# Visualisasi grafik tren berita kripto
if artikel_per_bulan:
    sorted_bulan = sorted(artikel_per_bulan.items())  # Urutkan data berdasarkan bulan
    bulan_labels, jumlah = zip(*sorted_bulan)  # Pisahkan label dan jumlah

    plt.figure(figsize=(12, 6))  # Ukuran grafik
    plt.plot(bulan_labels, jumlah, marker='o', linestyle='-', color='blue')  # Buat garis grafik
    plt.title('Tren Berita Kripto Tahun 2025')  # Judul grafik
    plt.xlabel('Bulan (YYYY-MM)')  # Label sumbu X
    plt.ylabel('Jumlah Artikel Kripto')  # Label sumbu Y
    plt.xticks(rotation=45)  # Rotasi label X agar tidak menumpuk

    plt.yticks(range(min(jumlah), max(jumlah)+1))  # Tampilkan angka bulat di sumbu Y

    plt.grid(True)  # Tambahkan garis bantu
    plt.tight_layout()  # Atur agar tata letak pas
    plt.show()  # Tampilkan grafik

else:
    print("Tidak ditemukan berita kripto di tahun 2025.")  # Jika tidak ada data sama sekali


#barchart
# Import library untuk scraping dan visualisasi
import requests  # Untuk melakukan HTTP request
from bs4 import BeautifulSoup  # Untuk parsing HTML
import matplotlib.pyplot as plt  # Untuk menampilkan grafik


# Fungsi untuk menghitung jumlah berita pada suatu kategori
def ambil_jumlah_berita(url, domain_prefix, kategori):
    # Kirim permintaan ke URL yang diberikan
    req = requests.get(url)
    # Parsing konten HTML dari response menggunakan BeautifulSoup
    soup = BeautifulSoup(req.text, 'lxml')

    # Cari semua elemen <a> yang memiliki atribut href (tautan)
    a_tags = soup.find_all('a', href=True)

    # Buat list untuk menyimpan link berita unik
    kumpulan_link = []

    # Iterasi setiap elemen <a>
    for a in a_tags:
        href = a['href']  # Ambil link href dari tag <a>

        # Cek apakah href mengandung '/read/' (format artikel) dan berasal dari domain yang sesuai
        if '/read/' in href and href.startswith(domain_prefix):
            # Cegah duplikasi link
            if href not in kumpulan_link:
                kumpulan_link.append(href)

    # Tampilkan jumlah berita untuk kategori tersebut
    print(f'Total berita kategori {kategori} ditemukan: {len(kumpulan_link)}')

    # Kembalikan jumlah total link berita
    return len(kumpulan_link)


## Data kategori: nama kategori, URL kategori, dan prefix domain artikel
kategori_data = [
    ('money', 'https://money.kompas.com/?source=navbar', 'https://money.kompas.com'),
    ('Nusaraya', 'https://www.kompas.com/nusaraya?source=navbar', 'https://www.kompas.com'),
    ('Tekno', 'https://tekno.kompas.com/?source=navbar', 'https://tekno.kompas.com'),
    ('Otomotif', 'https://otomotif.kompas.com/?source=navbar', 'https://otomotif.kompas.com'),
    ('Bola', 'https://bola.kompas.com/?source=navbar', 'https://bola.kompas.com'),
    ('Lifestyle', 'https://lifestyle.kompas.com/?source=navbar', 'https://lifestyle.kompas.com'),
    ('Tren', 'https://www.kompas.com/tren?source=navbar', 'https://www.kompas.com'),
    ('Lestari', 'https://lestari.kompas.com/?source=navbar', 'https://lestari.kompas.com'),
    ('Health', 'https://health.kompas.com/?source=navbar', 'https://health.kompas.com'),
    ('Travel', 'https://travel.kompas.com/?source=navbar', 'https://travel.kompas.com'),
]


# List untuk label dan data jumlah berita
labels = []
jumlah_berita = []

# Loop setiap kategori untuk mengambil jumlah berita
for kategori, url, prefix in kategori_data:
    total = ambil_jumlah_berita(url, prefix, kategori)  # Hitung jumlah berita
    labels.append(kategori)  # Simpan label kategori
    jumlah_berita.append(total)  # Simpan total berita

# Buat grafik batang untuk menampilkan hasil
plt.figure(figsize=(12, 6))  # Ukuran grafik
plt.bar(labels, jumlah_berita, color='skyblue')  # Buat bar chart
plt.title('Jumlah Berita per Kategori Kompas.com')  # Judul grafik
plt.xlabel('Kategori')  # Label sumbu X
plt.ylabel('Jumlah Berita')  # Label sumbu Y
plt.xticks(rotation=45)  # Rotasi label sumbu X agar rapi
plt.tight_layout()  # Atur tata letak agar tidak terpotong
plt.show()  # Tampilkan grafik

#piechart
# Import library eksternal
import requests  # Untuk mengambil data dari web menggunakan HTTP request
from bs4 import BeautifulSoup  # Untuk mem-parsing HTML dari web
import matplotlib.pyplot as plt  # Untuk menampilkan grafik (dalam hal ini pie chart)

# Fungsi untuk mengambil jumlah berita dari sebuah halaman kategori
def ambil_jumlah_berita(url, domain_prefix, kategori):
    # Kirim HTTP GET request ke halaman kategori
    req = requests.get(url)

    # Parsing konten HTML dari response menggunakan lxml parser
    soup = BeautifulSoup(req.text, 'lxml')

    # Temukan semua elemen <a> yang memiliki atribut href (link)
    a_tags = soup.find_all('a', href=True)

    kumpulan_link = []  # List untuk menyimpan link artikel yang valid

    # Loop setiap elemen <a> untuk mengecek apakah itu link artikel berita
    for a in a_tags:
        href = a['href']  # Ambil URL dari atribut href

        # Cek apakah link mengandung '/read/' (ciri khas artikel berita) dan berasal dari domain yang sesuai
        if '/read/' in href and href.startswith(domain_prefix):
            # Hindari memasukkan link yang sama dua kali
            if href not in kumpulan_link:
                kumpulan_link.append(href)

    # Cetak jumlah artikel yang berhasil dikumpulkan untuk kategori tersebut
    print(f'Total berita kategori {kategori} ditemukan: {len(kumpulan_link)}')

    # Kembalikan jumlah artikel yang ditemukan
    return len(kumpulan_link)

# Data kategori yang akan dianalisis
# Format: (nama_kategori, URL halaman utama kategori, prefix domain artikel untuk validasi)
kategori_data = [
    ('money', 'https://money.kompas.com/?source=navbar', 'https://money.kompas.com'),
    ('Nusaraya', 'https://www.kompas.com/nusaraya?source=navbar', 'https://www.kompas.com'),
    ('Tekno', 'https://tekno.kompas.com/?source=navbar', 'https://tekno.kompas.com'),
    ('Otomotif', 'https://otomotif.kompas.com/?source=navbar', 'https://otomotif.kompas.com'),
    ('Bola', 'https://bola.kompas.com/?source=navbar', 'https://bola.kompas.com'),
    ('Lifestyle', 'https://lifestyle.kompas.com/?source=navbar', 'https://lifestyle.kompas.com'),
    ('Tren', 'https://www.kompas.com/tren?source=navbar', 'https://www.kompas.com'),
    ('Lestari', 'https://lestari.kompas.com/?source=navbar', 'https://lestari.kompas.com'),
    ('Health', 'https://health.kompas.com/?source=navbar', 'https://health.kompas.com'),
    ('Travel', 'https://travel.kompas.com/?source=navbar', 'https://travel.kompas.com'),
]

# List kosong untuk menyimpan label dan jumlah berita dari masing-masing kategori
labels = []  # Untuk label pie chart (nama kategori)
jumlah_berita = []  # Untuk data jumlah berita yang akan divisualisasikan

# Loop setiap kategori yang sudah didefinisikan
for kategori, url, prefix in kategori_data:
    # Panggil fungsi untuk mendapatkan jumlah berita
    total = ambil_jumlah_berita(url, prefix, kategori)

    # Simpan label dan jumlahnya untuk dipakai di grafik
    labels.append(kategori)
    jumlah_berita.append(total)


# Tampilkan data dalam bentuk pie chart
plt.figure(figsize=(10, 10))  # Ukuran figure 10x10 inci
# Buat pie chart dengan data jumlah_berita dan labelnya
# autopct menampilkan persentase, startangle untuk memutar posisi awal chart
plt.pie(jumlah_berita, labels=labels, autopct='%1.1f%%', startangle=140)
# Tambahkan judul grafik
plt.title('Distribusi Jumlah Berita per Kategori Kompas.com')
# Biar pie chart-nya bulat, bukan oval
plt.axis('equal')
# Atur layout agar semua elemen pas dan tidak saling menimpa
plt.tight_layout()
# Tampilkan chart ke layar
plt.show()
