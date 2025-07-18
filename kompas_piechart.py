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
