# Pusat Generator Instrumen Ajar SMA

Aplikasi web statis untuk membantu guru SMA menyusun instrumen ajar berbasis Kurikulum Merdeka: Prota, Prosem, AME, ATP, KKTP, Modul Ajar (RPP/LKPD/Infografis), Asesmen, dan Daftar Nilai.

## Stack
- HTML, CSS, JavaScript (vanilla)
- Tailwind CSS (CDN)
- Font Awesome (CDN)
- html2pdf.js (CDN)

## Project Structure
- `index.html` — aplikasi utama
- `data/cp-data.js` — data Capaian Pembelajaran (CP) resmi: mapel, fase, CP, elemen CP, sumber regulasi
- `data/curriculum-map.js` — pemetaan pembelajaran per kelas: semester, topik, TP, JP, pertemuan
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
- CP resmi menjadi sumber utama dari `data/cp-data.js`; jika CP belum tersedia, aplikasi menampilkan pesan error dan tidak menghasilkan dokumen yang bergantung pada CP (Prota, Prosem, ATP, KKTP, Modul Ajar, Asesmen).
- Dokumen administratif AME dan Format Daftar Nilai tetap dapat dibuat walaupun CP masih kosong.
- Tidak ada fallback data palsu, tidak ada admin panel, tidak ada import/export CP, dan tidak ada database/AI.
- Data CP dipisahkan dari data pemetaan materi.
- Semua CP resmi saat ini dikosongkan; isi CP akan dimasukkan dari dokumen sumber resmi pada tahap berikutnya.
- Login: `guru` / `merdeka2026` — hanya untuk mengaktifkan tombol unduh/salin.
