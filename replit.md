# Pusat Generator Instrumen Ajar SMA

Aplikasi web statis untuk membantu guru SMA menyusun instrumen ajar berbasis Kurikulum Merdeka: Prota, Prosem, AME, ATP, KKTP, Modul Ajar (RPP/LKPD/Infografis), Asesmen, dan Daftar Nilai.

## Stack
- HTML, CSS, JavaScript (vanilla)
- Tailwind CSS (CDN)
- Font Awesome (CDN)
- html2pdf.js (CDN)
- Python 3 (backend minimal, tanpa package tambahan)

## Project Structure
- `index.html` — aplikasi utama
- `server.py` — backend minimal untuk melayani static files dan endpoint AI `/api/generate`
- `data/cp-data.js` — data Capaian Pembelajaran (CP) resmi: mapel, fase, CP, elemen CP, sumber regulasi
- `data/curriculum-map.js` — pemetaan pembelajaran per kelas: semester, topik, TP, JP, pertemuan
- `gen.html` — file lama yang tidak digunakan (tidak terhubung dari aplikasi utama)
- `.replit` — konfigurasi Replit

## How to Run
Klik workflow **Start application** di Replit atau jalankan:

```bash
python server.py
```

Aplikasi akan tersedia di port 5000 (webview).

## Secrets
Aktifkan fitur AI dengan menambahkan secret di Replit:

- `AI_API_KEY` — API key provider AI (default OpenAI, model `gpt-4o-mini`).
- Opsional: `AI_BASE_URL` untuk provider lain (default `https://api.openai.com/v1`).
- Opsional: `AI_MODEL` untuk mengganti model (default `gpt-4o-mini`).

Jika `AI_API_KEY` kosong, aplikasi menampilkan pesan "AI API belum dikonfigurasi." dan tidak memanggil AI.

## User preferences
- Aplikasi khusus jenjang SMA: Kelas X = Fase E, Kelas XI/XII = Fase F.
- CP resmi menjadi sumber utama dari `data/cp-data.js`; AI dilarang membuat atau mengubah CP.
- Dokumen non-AI tetap berjalan lokal: AME, Prota, Prosem, ATP, KKTP, Format Daftar Nilai.
- Dokumen AI: Modul Ajar (RPP/LKPD) dan Asesmen. Infografis tetap generator lokal.
- Jika CP kosong, semua generator yang membutuhkan CP (termasuk AI) diblokir dengan pesan peringatan.
- Semua CP resmi saat ini dikosongkan; isi CP akan dimasukkan dari dokumen sumber resmi pada tahap berikutnya.
- Login: `guru` / `merdeka2026` — hanya untuk mengaktifkan tombol unduh/salin.
