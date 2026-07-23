// Data Capaian Pembelajaran (CP) dan pemetaan materi untuk jenjang SMA.
// Struktur: mapel -> fase -> { cp, elements, source, curriculumMap: { kelas: [...] } }
// CP resmi harus diisi dari dokumen sumber resmi. Saat ini CP resmi belum dimasukkan.
window.cpData = {
    "B.Indonesia": {
        "E": {
            mapel: "Bahasa Indonesia",
            fase: "E",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                X: [
                    { topik: "Teks Laporan Hasil Observasi", jp: 12, pertemuan: 4, tp: "Menganalisis struktur dan kaidah kebahasaan teks LHO secara kritis." },
                    { topik: "Teks Anekdot", jp: 12, pertemuan: 4, tp: "Mengevaluasi makna tersirat dan kritik sosial dalam anekdot." },
                    { topik: "Hikayat dan Cerpen", jp: 16, pertemuan: 6, tp: "Membandingkan nilai-nilai dalam hikayat dengan kehidupan modern." },
                    { topik: "Teks Negosiasi", jp: 12, pertemuan: 4, tp: "Menyusun teks negosiasi tulis yang logis dan persuasif." },
                    { topik: "Teks Biografi", jp: 12, pertemuan: 4, tp: "Menelaah karakter unggul tokoh dalam teks biografi." },
                    { topik: "Puisi Kontemporer", jp: 12, pertemuan: 4, tp: "Mendemonstrasikan pembacaan puisi dengan ekspresi yang tepat." }
                ]
            }
        },
        "F": {
            mapel: "Bahasa Indonesia",
            fase: "F",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                XI: [
                    { topik: "Teks Argumentasi & Ketahanan Pangan", jp: 16, pertemuan: 6, tp: "Menulis teks argumentasi berdasarkan fakta akurat." },
                    { topik: "Teks Berita (Vlog/Video)", jp: 12, pertemuan: 4, tp: "Menyajikan teks berita dalam bentuk vlog." },
                    { topik: "Cerpen (Latar Sejarah)", jp: 16, pertemuan: 6, tp: "Menganalisis cerpen berlatar belakang sejarah Indonesia." },
                    { topik: "Karya Ilmiah", jp: 20, pertemuan: 7, tp: "Menyusun proposal dan karya ilmiah sederhana sesuai kaidah." }
                ],
                XII: [
                    { topik: "Surat Lamaran Pekerjaan", jp: 12, pertemuan: 4, tp: "Menulis surat lamaran dan CV yang efektif." },
                    { topik: "Teks Editorial", jp: 16, pertemuan: 6, tp: "Menyusun opini editorial menanggapi isu terkini." },
                    { topik: "Novel (Apresiasi Sastra)", jp: 20, pertemuan: 7, tp: "Menganalisis unsur intrinsik, ekstrinsik, dan nilai sosial novel." },
                    { topik: "Artikel Ilmiah Populer", jp: 16, pertemuan: 6, tp: "Mengonversi makalah menjadi artikel opini media massa." }
                ]
            }
        }
    },
    "Matematika": {
        "E": {
            mapel: "Matematika",
            fase: "E",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                X: [
                    { topik: "Eksponen dan Logaritma", jp: 16, pertemuan: 6, tp: "Menyelesaikan masalah kontekstual berkaitan dengan eksponen dan logaritma." },
                    { topik: "Barisan dan Deret Aritmetika", jp: 12, pertemuan: 4, tp: "Menerapkan barisan aritmetika pada masalah bunga tunggal/majemuk." },
                    { topik: "Barisan dan Deret Geometri", jp: 12, pertemuan: 4, tp: "Menerapkan barisan geometri pada pertumbuhan dan peluruhan." },
                    { topik: "Trigonometri Segitiga Siku-siku", jp: 16, pertemuan: 6, tp: "Memecahkan masalah jarak dan tinggi menggunakan perbandingan trigonometri." },
                    { topik: "Sistem Persamaan Linear Tiga Variabel", jp: 12, pertemuan: 4, tp: "Menyelesaikan model matematika SPLTV dari masalah nyata." }
                ]
            }
        },
        "F": {
            mapel: "Matematika",
            fase: "F",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                XI: [
                    { topik: "Komposisi dan Invers Fungsi", jp: 16, pertemuan: 6, tp: "Menganalisis operasi aljabar pada fungsi, komposisi, dan fungsi invers." },
                    { topik: "Matriks (Determinan & Invers)", jp: 16, pertemuan: 6, tp: "Menyelesaikan SPLDV menggunakan matriks." },
                    { topik: "Persamaan Lingkaran", jp: 16, pertemuan: 6, tp: "Menentukan persamaan lingkaran dan garis singgung lingkaran." },
                    { topik: "Transformasi Geometri", jp: 16, pertemuan: 6, tp: "Menganalisis sifat transformasi (translasi, refleksi, rotasi, dilatasi) matriks." }
                ],
                XII: [
                    { topik: "Geometri Ruang (Dimensi Tiga)", jp: 20, pertemuan: 7, tp: "Menentukan jarak antar titik, titik ke garis, dan titik ke bidang." },
                    { topik: "Statistika Data Berkelompok", jp: 20, pertemuan: 7, tp: "Menganalisis ukuran pemusatan dan penyebaran data histogram." },
                    { topik: "Kaidah Pencacahan", jp: 12, pertemuan: 4, tp: "Menyelesaikan masalah permutasi dan kombinasi." },
                    { topik: "Teori Peluang Kejadian Majemuk", jp: 12, pertemuan: 4, tp: "Menganalisis kejadian saling lepas, bebas, dan bersyarat." }
                ]
            }
        }
    },
    "Matematika Lanjut": {
        "F": {
            mapel: "Matematika Tingkat Lanjut",
            fase: "F",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                XI: [
                    { topik: "Polinomial (Suku Banyak)", jp: 24, pertemuan: 8, tp: "Menganalisis operasi, teorema sisa, dan teorema faktor polinomial." },
                    { topik: "Irisan Kerucut (Parabola & Elips)", jp: 20, pertemuan: 7, tp: "Menentukan persamaan irisan kerucut dengan puncaknya." },
                    { topik: "Matriks Tingkat Lanjut", jp: 20, pertemuan: 7, tp: "Menerapkan transformasi geometri kompleks menggunakan matriks ordo 3x3." }
                ],
                XII: [
                    { topik: "Limit Fungsi Aljabar & Trigonometri", jp: 24, pertemuan: 8, tp: "Menyelesaikan limit fungsi di suatu titik dan di tak hingga." },
                    { topik: "Turunan Fungsi Trigonometri", jp: 24, pertemuan: 8, tp: "Menerapkan turunan untuk menentukan nilai maksimum/minimum." },
                    { topik: "Integral Tentu dan Tak Tentu", jp: 24, pertemuan: 8, tp: "Menerapkan integral untuk menghitung luas daerah dan volume benda putar." }
                ]
            }
        }
    },
    "B.Inggris": {
        "E": {
            mapel: "Bahasa Inggris",
            fase: "E",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                X: [
                    { topik: "Descriptive Text (Place/Person)", jp: 12, pertemuan: 4, tp: "Menyusun teks deskriptif lisan dan tulis yang padu." },
                    { topik: "Recount Text (Experience)", jp: 12, pertemuan: 4, tp: "Menceritakan kembali pengalaman masa lalu secara runtut." },
                    { topik: "Narrative Text (Legends)", jp: 16, pertemuan: 6, tp: "Menganalisis pesan moral dari naratif legenda Nusantara." },
                    { topik: "Expository Text (Basic)", jp: 16, pertemuan: 6, tp: "Menyatakan argumen logis terhadap isu lingkungan sekitar." }
                ]
            }
        },
        "F": {
            mapel: "Bahasa Inggris",
            fase: "F",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                XI: [
                    { topik: "Asking & Giving Opinion", jp: 12, pertemuan: 4, tp: "Mempertahankan opini dalam diskusi kelas berbahasa Inggris." },
                    { topik: "Analytical Exposition", jp: 16, pertemuan: 6, tp: "Menganalisis struktur tesis, argumen, dan reiterasi secara kritis." },
                    { topik: "Personal Letter & Invitation", jp: 12, pertemuan: 4, tp: "Menulis surat undangan resmi dan pribadi yang sopan." },
                    { topik: "Cause and Effect Relationship", jp: 12, pertemuan: 4, tp: "Menggunakan konjungsi sebab-akibat dengan akurat." }
                ],
                XII: [
                    { topik: "Job Application Letter & CV", jp: 16, pertemuan: 6, tp: "Mempresentasikan lamaran kerja dalam simulasi wawancara." },
                    { topik: "News Item Text", jp: 16, pertemuan: 6, tp: "Meringkas berita aktual dari media berbahasa Inggris." },
                    { topik: "Discussion Text", jp: 16, pertemuan: 6, tp: "Menyajikan dua sudut pandang (Pro & Kontra) dalam debat." },
                    { topik: "Procedure Text (Manual/Tips)", jp: 12, pertemuan: 4, tp: "Mendemonstrasikan manual operasi alat teknologi mutakhir." }
                ]
            }
        }
    },
    "B.Inggris Lanjut": {
        "F": {
            mapel: "Bahasa Inggris Tingkat Lanjut",
            fase: "F",
            source: { regulation: "", number: "", year: "", status: "active" },
            cp: "",
            elements: [],
            curriculumMap: {
                XI: [
                    { topik: "Hortatory Exposition", jp: 20, pertemuan: 7, tp: "Menganalisis dan menyusun teks persuasi yang berakhiran dengan rekomendasi." },
                    { topik: "English Literature: Short Story", jp: 20, pertemuan: 7, tp: "Menganalisis elemen sastra (plot, setting, character) cerita pendek klasik." },
                    { topik: "Academic Presentation", jp: 24, pertemuan: 8, tp: "Melakukan presentasi akademis berbasis riset mini (Mini Research)." }
                ],
                XII: [
                    { topik: "English Literature: Poetry", jp: 16, pertemuan: 6, tp: "Menganalisis figures of speech dan rima dalam puisi berbahasa Inggris." },
                    { topik: "Review Text (Movie/Book)", jp: 20, pertemuan: 7, tp: "Menyusun kritik atau ulasan komprehensif terhadap film/buku." },
                    { topik: "Advanced Discussion & Debate", jp: 28, pertemuan: 10, tp: "Mengaplikasikan format debat parlementer (Asian/British Parliamentary)." }
                ]
            }
        }
    }
};
