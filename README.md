# Aplikasi Optimasi Multi-Hop HEED + ACO

Simulasi optimasi routing pada **Wireless Sensor Network (WSN)** menggunakan kombinasi **Multi-Hop HEED (Hybrid Energy-Efficient Distributed clustering)** dan **Ant Colony Optimization (ACO)**.  
Dibuat dengan **Python + PyQt5** untuk antarmuka grafis.

---

## 📌 Fitur Utama
- Tampilan GUI interaktif berbasis PyQt5.
- Input parameter simulasi:
  - Jumlah node sensor
  - Ukuran area simulasi
  - Jumlah semut (ACO)
  - Jumlah iterasi (ACO)
- Visualisasi 2x2 grid:
  - Topologi awal node
  - Clustering dengan HEED
  - Routing hasil ACO
  - Energi residual node
- Ringkasan hasil simulasi otomatis.
- Ekspor hasil:
  - Data simulasi ke **Excel (.xlsx)**
  - Grafik ke **PDF**

---

## 📦 Instalasi

### 1. Clone repository
```bash
git clone https://github.com/username/namaproject.git
cd namaproject


python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


pip install -r requirements.txt


pip install PyQt5 matplotlib numpy pandas openpyxl reportlab


python app.py



.
├── app.py          # Main GUI aplikasi
├── wsn.py          # Modul Wireless Sensor Network
├── heed.py         # Algoritma HEED clustering
├── aco.py          # Algoritma Ant Colony Optimization
├── requirements.txt
└── README.md
