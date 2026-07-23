# Pusat Generator Instrumen Ajar SMA

Aplikasi web statis untuk membantu guru SMA menyusun instrumen ajar berbasis Kurikulum Merdeka: Prota, Prosem, AME, ATP, KKTP, Modul Ajar (RPP/LKPD/Infografis), Asesmen, dan Daftar Nilai.

## Stack
- HTML, CSS, JavaScript (vanilla)
- Tailwind CSS (CDN)
- Font Awesome (CDN)
- html2pdf.js (CDN)

## Project Structure
- `index.html` — aplikasi utama
- `data/cp-data.js` — data Capaian Pembelajaran (CP) dan pemetaan materi (dipisah dari logika aplikasi)
- `gen.html` — file lama yang tidak digunakan (tidak terhubung dari aplikasi utama)
- `.replit` — konfigurasi Replit

## How to Run
Klik workflow **Start application** di Replit atau jalankan:

```bash
python -m http.server 5000
```

Aplikasi akan tersedia di port 5000 (webview).

## User preferences
- Aplikasi khusus jenjang SMA: Kelas X = Fase E, Kelas XI/XII = Fase F.
- CP resmi menjadi sumber utama; jika CP belum tersedia, aplikasi menampilkan pesan error dan tidak menghasilkan dokumen.
- Tidak ada fallback data palsu ("Konsep Dasar...", "Analisis Lanjutan...", dsb.).
- Data CP dipisahkan di `/data/cp-data.js` dengan struktur `mapel -> fase -> { cp, elements, source, curriculumMap }`.
- Semua CP resmi saat ini dikosongkan; isi CP akan dimasukkan dari dokumen sumber resmi pada tahap berikutnya.
