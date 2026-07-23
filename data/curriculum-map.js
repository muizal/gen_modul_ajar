// Pemetaan pembelajaran (materi/topik, TP, JP, pertemuan) per kelas untuk jenjang SMA.
// Dipisah dari data CP resmi. Semester diinfer dari posisi item dalam kelas:
// setengah pertama = Ganjil, setengah kedua = Genap (sama dengan logika Prosem existing).
window.curriculumMap = {
    "B.Indonesia": {
        "X": [
            { semester: "Ganjil", topik: "Teks Laporan Hasil Observasi", jp: 12, pertemuan: 4, tp: "Menganalisis struktur dan kaidah kebahasaan teks LHO secara kritis." },
            { semester: "Ganjil", topik: "Teks Anekdot", jp: 12, pertemuan: 4, tp: "Mengevaluasi makna tersirat dan kritik sosial dalam anekdot." },
            { semester: "Ganjil", topik: "Hikayat dan Cerpen", jp: 16, pertemuan: 6, tp: "Membandingkan nilai-nilai dalam hikayat dengan kehidupan modern." },
            { semester: "Genap", topik: "Teks Negosiasi", jp: 12, pertemuan: 4, tp: "Menyusun teks negosiasi tulis yang logis dan persuasif." },
            { semester: "Genap", topik: "Teks Biografi", jp: 12, pertemuan: 4, tp: "Menelaah karakter unggul tokoh dalam teks biografi." },
            { semester: "Genap", topik: "Puisi Kontemporer", jp: 12, pertemuan: 4, tp: "Mendemonstrasikan pembacaan puisi dengan ekspresi yang tepat." }
        ],
        "XI": [
            { semester: "Ganjil", topik: "Teks Argumentasi & Ketahanan Pangan", jp: 16, pertemuan: 6, tp: "Menulis teks argumentasi berdasarkan fakta akurat." },
            { semester: "Ganjil", topik: "Teks Berita (Vlog/Video)", jp: 12, pertemuan: 4, tp: "Menyajikan teks berita dalam bentuk vlog." },
            { semester: "Genap", topik: "Cerpen (Latar Sejarah)", jp: 16, pertemuan: 6, tp: "Menganalisis cerpen berlatar belakang sejarah Indonesia." },
            { semester: "Genap", topik: "Karya Ilmiah", jp: 20, pertemuan: 7, tp: "Menyusun proposal dan karya ilmiah sederhana sesuai kaidah." }
        ],
        "XII": [
            { semester: "Ganjil", topik: "Surat Lamaran Pekerjaan", jp: 12, pertemuan: 4, tp: "Menulis surat lamaran dan CV yang efektif." },
            { semester: "Ganjil", topik: "Teks Editorial", jp: 16, pertemuan: 6, tp: "Menyusun opini editorial menanggapi isu terkini." },
            { semester: "Genap", topik: "Novel (Apresiasi Sastra)", jp: 20, pertemuan: 7, tp: "Menganalisis unsur intrinsik, ekstrinsik, dan nilai sosial novel." },
            { semester: "Genap", topik: "Artikel Ilmiah Populer", jp: 16, pertemuan: 6, tp: "Mengonversi makalah menjadi artikel opini media massa." }
        ]
    },
    "Matematika": {
        "X": [
            { semester: "Ganjil", topik: "Eksponen dan Logaritma", jp: 16, pertemuan: 6, tp: "Menyelesaikan masalah kontekstual berkaitan dengan eksponen dan logaritma." },
            { semester: "Ganjil", topik: "Barisan dan Deret Aritmetika", jp: 12, pertemuan: 4, tp: "Menerapkan barisan aritmetika pada masalah bunga tunggal/majemuk." },
            { semester: "Ganjil", topik: "Barisan dan Deret Geometri", jp: 12, pertemuan: 4, tp: "Menerapkan barisan geometri pada pertumbuhan dan peluruhan." },
            { semester: "Genap", topik: "Trigonometri Segitiga Siku-siku", jp: 16, pertemuan: 6, tp: "Memecahkan masalah jarak dan tinggi menggunakan perbandingan trigonometri." },
            { semester: "Genap", topik: "Sistem Persamaan Linear Tiga Variabel", jp: 12, pertemuan: 4, tp: "Menyelesaikan model matematika SPLTV dari masalah nyata." }
        ],
        "XI": [
            { semester: "Ganjil", topik: "Komposisi dan Invers Fungsi", jp: 16, pertemuan: 6, tp: "Menganalisis operasi aljabar pada fungsi, komposisi, dan fungsi invers." },
            { semester: "Ganjil", topik: "Matriks (Determinan & Invers)", jp: 16, pertemuan: 6, tp: "Menyelesaikan SPLDV menggunakan matriks." },
            { semester: "Genap", topik: "Persamaan Lingkaran", jp: 16, pertemuan: 6, tp: "Menentukan persamaan lingkaran dan garis singgung lingkaran." },
            { semester: "Genap", topik: "Transformasi Geometri", jp: 16, pertemuan: 6, tp: "Menganalisis sifat transformasi (translasi, refleksi, rotasi, dilatasi) matriks." }
        ],
        "XII": [
            { semester: "Ganjil", topik: "Geometri Ruang (Dimensi Tiga)", jp: 20, pertemuan: 7, tp: "Menentukan jarak antar titik, titik ke garis, dan titik ke bidang." },
            { semester: "Ganjil", topik: "Statistika Data Berkelompok", jp: 20, pertemuan: 7, tp: "Menganalisis ukuran pemusatan dan penyebaran data histogram." },
            { semester: "Genap", topik: "Kaidah Pencacahan", jp: 12, pertemuan: 4, tp: "Menyelesaikan masalah permutasi dan kombinasi." },
            { semester: "Genap", topik: "Teori Peluang Kejadian Majemuk", jp: 12, pertemuan: 4, tp: "Menganalisis kejadian saling lepas, bebas, dan bersyarat." }
        ]
    },
    "Matematika Lanjut": {
        "XI": [
            { semester: "Ganjil", topik: "Polinomial (Suku Banyak)", jp: 24, pertemuan: 8, tp: "Menganalisis operasi, teorema sisa, dan teorema faktor polinomial." },
            { semester: "Ganjil", topik: "Irisan Kerucut (Parabola & Elips)", jp: 20, pertemuan: 7, tp: "Menentukan persamaan irisan kerucut dengan puncaknya." },
            { semester: "Genap", topik: "Matriks Tingkat Lanjut", jp: 20, pertemuan: 7, tp: "Menerapkan transformasi geometri kompleks menggunakan matriks ordo 3x3." }
        ],
        "XII": [
            { semester: "Ganjil", topik: "Limit Fungsi Aljabar & Trigonometri", jp: 24, pertemuan: 8, tp: "Menyelesaikan limit fungsi di suatu titik dan di tak hingga." },
            { semester: "Ganjil", topik: "Turunan Fungsi Trigonometri", jp: 24, pertemuan: 8, tp: "Menerapkan turunan untuk menentukan nilai maksimum/minimum." },
            { semester: "Genap", topik: "Integral Tentu dan Tak Tentu", jp: 24, pertemuan: 8, tp: "Menerapkan integral untuk menghitung luas daerah dan volume benda putar." }
        ]
    },
    "B.Inggris": {
        "X": [
            { semester: "Ganjil", topik: "Descriptive Text (Place/Person)", jp: 12, pertemuan: 4, tp: "Menyusun teks deskriptif lisan dan tulis yang padu." },
            { semester: "Ganjil", topik: "Recount Text (Experience)", jp: 12, pertemuan: 4, tp: "Menceritakan kembali pengalaman masa lalu secara runtut." },
            { semester: "Genap", topik: "Narrative Text (Legends)", jp: 16, pertemuan: 6, tp: "Menganalisis pesan moral dari naratif legenda Nusantara." },
            { semester: "Genap", topik: "Expository Text (Basic)", jp: 16, pertemuan: 6, tp: "Menyatakan argumen logis terhadap isu lingkungan sekitar." }
        ],
        "XI": [
            { semester: "Ganjil", topik: "Asking & Giving Opinion", jp: 12, pertemuan: 4, tp: "Mempertahankan opini dalam diskusi kelas berbahasa Inggris." },
            { semester: "Ganjil", topik: "Analytical Exposition", jp: 16, pertemuan: 6, tp: "Menganalisis struktur tesis, argumen, dan reiterasi secara kritis." },
            { semester: "Genap", topik: "Personal Letter & Invitation", jp: 12, pertemuan: 4, tp: "Menulis surat undangan resmi dan pribadi yang sopan." },
            { semester: "Genap", topik: "Cause and Effect Relationship", jp: 12, pertemuan: 4, tp: "Menggunakan konjungsi sebab-akibat dengan akurat." }
        ],
        "XII": [
            { semester: "Ganjil", topik: "Job Application Letter & CV", jp: 16, pertemuan: 6, tp: "Mempresentasikan lamaran kerja dalam simulasi wawancara." },
            { semester: "Ganjil", topik: "News Item Text", jp: 16, pertemuan: 6, tp: "Meringkas berita aktual dari media berbahasa Inggris." },
            { semester: "Genap", topik: "Discussion Text", jp: 16, pertemuan: 6, tp: "Menyajikan dua sudut pandang (Pro & Kontra) dalam debat." },
            { semester: "Genap", topik: "Procedure Text (Manual/Tips)", jp: 12, pertemuan: 4, tp: "Mendemonstrasikan manual operasi alat teknologi mutakhir." }
        ]
    },
    "B.Inggris Lanjut": {
        "XI": [
            { semester: "Ganjil", topik: "Hortatory Exposition", jp: 20, pertemuan: 7, tp: "Menganalisis dan menyusun teks persuasi yang berakhiran dengan rekomendasi." },
            { semester: "Ganjil", topik: "English Literature: Short Story", jp: 20, pertemuan: 7, tp: "Menganalisis elemen sastra (plot, setting, character) cerita pendek klasik." },
            { semester: "Genap", topik: "Academic Presentation", jp: 24, pertemuan: 8, tp: "Melakukan presentasi akademis berbasis riset mini (Mini Research)." }
        ],
        "XII": [
            { semester: "Ganjil", topik: "English Literature: Poetry", jp: 16, pertemuan: 6, tp: "Menganalisis figures of speech dan rima dalam puisi berbahasa Inggris." },
            { semester: "Ganjil", topik: "Review Text (Movie/Book)", jp: 20, pertemuan: 7, tp: "Menyusun kritik atau ulasan komprehensif terhadap film/buku." },
            { semester: "Genap", topik: "Advanced Discussion & Debate", jp: 28, pertemuan: 10, tp: "Mengaplikasikan format debat parlementer (Asian/British Parliamentary)." }
        ]
    }
};
