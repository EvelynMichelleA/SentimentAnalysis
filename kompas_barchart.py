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

