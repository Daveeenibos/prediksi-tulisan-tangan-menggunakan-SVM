# Prediksi Tulisan Tangan Menggunakan SVM

Proyek ini adalah sistem pengenalan tulisan tangan (handwriting recognition) sederhana yang menggunakan algoritma Support Vector Machine (SVM). Sistem ini terdiri dari model machine learning yang dilatih menggunakan dataset angka tulis tangan dan antarmuka pengguna grafis (GUI) berbasis Kivy untuk memudahkan pengujian prediksi.

## Fitur

- **Pelatihan Model**: Notebook Jupyter (`SVM.ipynb`) untuk memuat dataset, memproses gambar, melatih model SVM, dan mengevaluasi akurasi.
- **GUI Interaktif**: Aplikasi desktop (`gui_kivy.py`) yang memungkinkan pengguna memilih gambar dan melihat hasil prediksi model secara langsung.
- **Visualisasi**: Tampilan antarmuka yang bersih dengan statistik akurasi model.

## Prasyarat

Sebelum menjalankan proyek ini, pastikan Anda telah menginstal pustaka Python berikut:

- Python 3.x
- Numpy
- Scikit-learn
- Pillow (PIL)
- Kivy
- Joblib
- Matplotlib (opsional, untuk visualisasi di notebook)

Anda dapat menginstalnya menggunakan pip:

```bash
pip install numpy scikit-learn pillow kivy joblib matplotlib
```

## Cara Penggunaan

### 1. Pelatihan Model (Opsional)

Jika Anda ingin melatih ulang model atau menggunakan dataset Anda sendiri:

1. Buka file `SVM.ipynb` menggunakan Jupyter Notebook atau editor yang mendukung (seperti VS Code).
2. Pastikan dataset Anda tersedia dan path di dalam notebook disesuaikan dengan lokasi dataset Anda.
3. Jalankan sel-sel di notebook secara berurutan untuk melatih model.
4. Model yang telah dilatih akan disimpan sebagai `svm_model.pkl`.

### 2. Menjalankan Aplikasi GUI

Untuk menggunakan aplikasi prediksi:

1. Pastikan file `svm_model.pkl` berada di direktori yang sama dengan `gui_kivy.py`. (Jika belum ada, jalankan notebook pelatihan terlebih dahulu).
2. Jalankan aplikasi dengan perintah:

```bash
python gui_kivy.py
```

3. Pada antarmuka aplikasi:
    - Klik tombol **Pilih Gambar** untuk mengunggah gambar tulisan tangan (format .png, .jpg, .jpeg).
    - Gambar akan muncul di preview.
    - Klik tombol **Prediksi Sekarang** untuk melihat hasil pengenalan angka.

## Struktur File

- `SVM.ipynb`: Notebook untuk preprocessing data dan pelatihan model SVM.
- `gui_kivy.py`: Skript utama untuk aplikasi GUI.
- `svm_model.pkl`: File model SVM yang sudah dilatih (dihasilkan setelah menjalankan notebook).
- `logo UNPATTI.png`: Aset logo untuk aplikasi GUI.

## Catatan

- Aplikasi ini dirancang untuk menerima input gambar berupa angka tulisan tangan (0-9).
- Untuk hasil terbaik, gunakan gambar dengan latar belakang bersih dan kontras yang baik, mirip dengan dataset MNIST atau data latih yang digunakan.
