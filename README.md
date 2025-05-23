# FETopsis

**Versi Python:** 3.13.3

Sistem Pendukung Keputusan dengan Metode TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)

## Deskripsi Proyek

FETopsis adalah aplikasi web berbasis Django yang membantu pengguna melakukan perhitungan dan analisis keputusan multikriteria menggunakan metode TOPSIS. Sistem ini menyediakan antarmuka modern untuk melakukan input kriteria, alternatif, bobot, serta melihat hasil ranking dan riwayat perhitungan.

## Fitur Utama
- **Autentikasi Pengguna**: Registrasi, login, dan logout.
- **Dashboard Interaktif**: Akses cepat ke fitur utama dan tutorial.
- **Perhitungan TOPSIS**: Input kriteria, alternatif, bobot, dan tipe (benefit/cost), lalu lakukan perhitungan otomatis.
- **Riwayat & Detail Perhitungan**: Simpan, lihat, dan analisis hasil perhitungan sebelumnya.
- **Visualisasi Hasil**: Tabel, ranking, dan breakdown nilai untuk setiap alternatif.
- **Tutorial Penggunaan**: Penjelasan langkah-langkah metode TOPSIS secara interaktif.

## Alur Penggunaan
1. **Registrasi/Login**: Pengguna membuat akun atau masuk ke sistem.
2. **Dashboard**: Pengguna dapat memulai perhitungan baru, melihat history, atau membaca tutorial.
3. **Perhitungan TOPSIS**:
   - Input kriteria beserta bobot dan tipe.
   - Input alternatif dan nilai untuk setiap kriteria.
   - Sistem akan melakukan normalisasi, perhitungan bobot, solusi ideal, dan ranking otomatis.
   - Hasil dapat disimpan ke history.
4. **History & Detail**: Pengguna dapat melihat riwayat perhitungan, detail hasil, dan breakdown nilai setiap alternatif.

## Struktur Proyek
```
frontend-project/
├── frontend/                # Aplikasi utama (views, urls, templates)
│   ├── templates/frontend/  # Template HTML (dashboard, login, topsis, dsb)
│   ├── views.py             # Logika utama (autentikasi, topsis, dsb)
│   ├── urls.py              # Routing URL aplikasi frontend
│   ├── models.py            # Model (kosong, data disimpan di backend/api)
│   └── ...
├── mysite/                  # Konfigurasi proyek Django
│   ├── settings.py          # Pengaturan aplikasi, database, static, dsb
│   ├── urls.py              # Routing global proyek
│   └── ...
├── staticfiles/             # File statis hasil collectstatic
├── templates/               # Template global (base, navbar, footer)
├── requirements.txt         # Daftar dependensi Python
├── manage.py                # Entrypoint manajemen Django
└── db.sqlite3               # Database SQLite (default)
```

## Instalasi & Menjalankan Proyek
1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd frontend-project
   ```
2. **Buat virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Migrasi database**
   ```bash
   python manage.py migrate
   ```
4. **Jalankan server**
   ```bash
   python manage.py runserver
   ```
5. **Akses aplikasi**
   Buka browser ke `http://localhost:8000/`

## Penjelasan Kode Utama
- **`frontend/views.py`**: Berisi fungsi-fungsi utama seperti `signup`, `login`, `dashboard`, `topsis_calculate`, `topsis_save`, `topsis_history`, dan `topsis_detail`.
- **`frontend/templates/frontend/`**: Terdapat file HTML untuk dashboard, login, hasil topsis, history, dan detail.
- **`mysite/settings.py`**: Konfigurasi aplikasi, database, static files, dan template.
- **`requirements.txt`**: Daftar library yang digunakan, termasuk Django, requests, whitenoise, dsb.

## Metode TOPSIS
Metode TOPSIS adalah teknik pengambilan keputusan multikriteria yang memilih alternatif terbaik berdasarkan kedekatan relatif terhadap solusi ideal positif dan negatif. Langkah-langkah utama:
1. Normalisasi matriks keputusan
2. Mengalikan dengan bobot kriteria
3. Menentukan solusi ideal positif dan negatif
4. Menghitung jarak setiap alternatif ke solusi ideal
5. Menghitung nilai kedekatan relatif
6. Merangking alternatif

## Credits
- Dibuat oleh: Nabil Ulil Albab
- Framework: Django 4.2.3
- Template UI: TailwindCSS (melalui CDN)

## Lisensi
Proyek ini bersifat open-source dan dapat dikembangkan sesuai kebutuhan.
