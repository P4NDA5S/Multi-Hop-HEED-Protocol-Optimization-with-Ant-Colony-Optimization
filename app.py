# app.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFormLayout, QSpinBox, QTextEdit,
    QStatusBar, QStackedWidget, QHBoxLayout, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from wsn import WSN
from heed import HEED
from aco import AntColony


class WSNApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Optimasi Multi-Hop HEED + ACO")
        # Default window tuned for desktop (Full HD friendly)
        self.resize(1280, 800)

        # Stack widget untuk semua halaman
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Global style (simple, professional)
        self.setStyleSheet("""
            QMainWindow { background: #f4f6f8; }
            QLabel#title { color: #2b4f81; }
            QFrame#card { background: #ffffff; border: 1px solid #d0d7df; border-radius: 10px; }
            QPushButton { min-height: 42px; font-size: 12pt; padding: 6px 12px; }
            QPushButton.primary { background: #2b7cff; color: white; border-radius: 6px; }
            QTextEdit { background: white; border: 1px solid #dfe6ee; }
        """)

        # Prepare matplotlib default style for clarity
        plt.rcParams.update({'font.size': 10})

        # Tambahkan semua halaman
        self.init_welcome_page()
        self.init_menu_page()
        self.init_panduan_page()
        self.init_parameter_page()
        self.init_summary_page()
        self.init_visual_page()

        # Tampilkan welcome page pertama kali
        self.stack.setCurrentWidget(self.welcome_page)

    # ----------  Page 0: Welcome ----------
    def init_welcome_page(self):
        self.welcome_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setSpacing(20)

        title = QLabel("Aplikasi Optimasi Multi-Hop HEED + ACO")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        desc = QLabel(
            "Simulasi optimasi routing pada Wireless Sensor Network\n"
            "menggunakan kombinasi Multi-Hop HEED dan Ant Colony Optimization (ACO)."
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 12))

        start_button = QPushButton("Mulai")
        start_button.setObjectName("start")
        start_button.setProperty("class", "primary")
        start_button.setStyleSheet("QPushButton.primary { background: #2b7cff; color: white; font-weight: bold; }")
        start_button.setFixedSize(220, 48)
        start_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(10)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.welcome_page.setLayout(layout)
        self.stack.addWidget(self.welcome_page)

    # ----------  Page 1: Menu Card ----------
    def init_menu_page(self):
        self.menu_page = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(40)

        # Card helper
        def make_card(icon, title, subtitle, callback):
            card = QFrame()
            card.setObjectName("card")
            card.setFixedSize(460, 320)
            vbox = QVBoxLayout()
            vbox.setContentsMargins(20, 20, 20, 20)
            vbox.setSpacing(12)

            lbl_icon = QLabel(icon)
            lbl_icon.setAlignment(Qt.AlignCenter)
            lbl_icon.setFont(QFont("Segoe UI Emoji", 40))

            lbl_title = QLabel(title)
            lbl_title.setAlignment(Qt.AlignCenter)
            lbl_title.setFont(QFont("Segoe UI", 16, QFont.Bold))

            lbl_sub = QLabel(subtitle)
            lbl_sub.setAlignment(Qt.AlignCenter)
            lbl_sub.setWordWrap(True)
            lbl_sub.setFont(QFont("Segoe UI", 11))
            lbl_sub.setStyleSheet("color: #4b5966;")

            btn = QPushButton("Pilih")
            btn.setFixedWidth(160)
            btn.setProperty("class", "primary")
            btn.setStyleSheet("QPushButton.primary { background: #2b7cff; color: white; font-weight: bold; }")
            btn.clicked.connect(callback)

            vbox.addStretch()
            vbox.addWidget(lbl_icon)
            vbox.addWidget(lbl_title)
            vbox.addWidget(lbl_sub)
            vbox.addStretch()
            vbox.addWidget(btn, alignment=Qt.AlignCenter)
            card.setLayout(vbox)
            return card

        card1 = make_card("📘", "Panduan", "Panduan singkat penggunaan aplikasi dan alur langkah.", lambda: self.stack.setCurrentWidget(self.panduan_page))
        card2 = make_card("🧪", "Simulasi", "Masukkan parameter simulasi dan jalankan optimasi.", lambda: self.stack.setCurrentWidget(self.param_page))

        layout.addStretch()
        layout.addWidget(card1)
        layout.addWidget(card2)
        layout.addStretch()

        self.menu_page.setLayout(layout)
        self.stack.addWidget(self.menu_page)

    # ----------  Page 2: Panduan ----------
    def init_panduan_page(self):
        self.panduan_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(16)

        title = QLabel("Panduan Penggunaan")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(
            "1. Klik menu Simulasi atau pilih 'Simulasi' pada halaman menu.\n"
            "2. Pada halaman Simulasi, atur parameter: Jumlah Node, Ukuran Area, Jumlah Semut, dan Jumlah Iterasi.\n"
            "3. Tekan tombol 'Jalankan Simulasi'. Tunggu hingga proses selesai.\n"
            "4. Setelah selesai, Anda akan melihat ringkasan hasil. Untuk melihat detail grafik, tekan 'Lihat Visualisasi'.\n\n"
            "Catatan: Untuk screenshot dokumen HKI, gunakan halaman Ringkasan dan Visualisasi."
        )
        text.setFont(QFont("Segoe UI", 11))

        btn_next = QPushButton("➡️ Lanjut ke Simulasi")
        btn_next.setFixedSize(200, 40)
        btn_next.clicked.connect(lambda: self.stack.setCurrentWidget(self.param_page))

        btn_back = QPushButton("⬅️ Kembali ke Menu")
        btn_back.setFixedSize(160, 40)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))

        nav = QHBoxLayout()
        nav.addWidget(btn_back)
        nav.addStretch()
        nav.addWidget(btn_next)

        layout.addWidget(title)
        layout.addWidget(text)
        layout.addLayout(nav)

        self.panduan_page.setLayout(layout)
        self.stack.addWidget(self.panduan_page)

    # ----------  Page 3: Parameter ----------
    def init_parameter_page(self):
        self.param_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(80, 30, 80, 30)
        layout.setSpacing(18)

        title = QLabel("Halaman Simulasi")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignLeft)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(14)

        self.node_input = QSpinBox()
        self.node_input.setRange(10, 500)
        self.node_input.setValue(50)
        self.node_input.setFixedWidth(140)

        self.area_input = QSpinBox()
        self.area_input.setRange(50, 2000)
        self.area_input.setValue(100)
        self.area_input.setFixedWidth(140)

        self.ants_input = QSpinBox()
        self.ants_input.setRange(5, 200)
        self.ants_input.setValue(20)
        self.ants_input.setFixedWidth(140)

        self.iter_input = QSpinBox()
        self.iter_input.setRange(10, 2000)
        self.iter_input.setValue(50)
        self.iter_input.setFixedWidth(140)

        form.addRow("Jumlah Node:", self.node_input)
        form.addRow("Ukuran Area (px):", self.area_input)
        form.addRow("Jumlah Semut (ACO):", self.ants_input)
        form.addRow("Jumlah Iterasi (ACO):", self.iter_input)

        run_button = QPushButton("Jalankan Simulasi")
        run_button.setProperty("class", "primary")
        run_button.setFixedSize(220, 48)
        run_button.clicked.connect(self.run_simulation)

        btn_back = QPushButton("⬅️ Kembali ke Menu")
        btn_back.setFixedSize(160, 40)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addSpacing(8)
        layout.addWidget(run_button, alignment=Qt.AlignLeft)
        layout.addSpacing(6)
        layout.addWidget(btn_back, alignment=Qt.AlignLeft)

        self.param_page.setLayout(layout)
        self.stack.addWidget(self.param_page)

    # ----------  Page 4: Ringkasan ----------
    def init_summary_page(self):
        self.summary_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(80, 30, 80, 30)
        layout.setSpacing(16)

        title = QLabel("Ringkasan Hasil")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setFont(QFont("Segoe UI", 11))

        btn_next = QPushButton("➡️ Lihat Visualisasi")
        btn_next.setFixedSize(200, 40)
        btn_next.clicked.connect(lambda: self.stack.setCurrentWidget(self.visual_page))

        btn_back = QPushButton("⬅️ Kembali ke Simulasi")
        btn_back.setFixedSize(160, 40)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.param_page))

        nav = QHBoxLayout()
        nav.addWidget(btn_back)
        nav.addStretch()
        nav.addWidget(btn_next)

        layout.addWidget(title)
        layout.addWidget(self.summary_text)
        layout.addLayout(nav)

        self.summary_page.setLayout(layout)
        self.stack.addWidget(self.summary_page)

    # ----------  Page 5: Visualisasi (grid 2x2) ----------
    def init_visual_page(self):
        self.visual_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(12)

        title = QLabel("Visualisasi Hasil Simulasi")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)

        # create 4 figures and canvas
        self.figures = [plt.figure(figsize=(6, 4)) for _ in range(4)]
        self.canvases = [FigureCanvas(fig) for fig in self.figures]
        vis_titles = ["Topologi Awal", "Clustering HEED", "Routing ACO", "Energi Residual"]

        for i, (canvas, t) in enumerate(zip(self.canvases, vis_titles)):
            frame = QFrame()
            f_layout = QVBoxLayout()
            lab = QLabel(t)
            lab.setFont(QFont("Segoe UI", 12, QFont.Bold))
            lab.setAlignment(Qt.AlignCenter)
            f_layout.addWidget(lab)
            f_layout.addWidget(canvas)
            frame.setLayout(f_layout)
            # grid positions: (0,0),(0,1),(1,0),(1,1)
            grid.addWidget(frame, i // 2, i % 2)

        layout.addLayout(grid)

        btn_back = QPushButton("⬅️ Kembali ke Ringkasan")
        btn_back.setFixedSize(200, 40)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.summary_page))
        layout.addWidget(btn_back, alignment=Qt.AlignLeft)

        self.visual_page.setLayout(layout)
        self.stack.addWidget(self.visual_page)

    # ---------- Simulasi ----------
    def run_simulation(self):
        # read params
        num_nodes = self.node_input.value()
        area = self.area_input.value()
        n_ants = self.ants_input.value()
        n_iter = self.iter_input.value()

        self.statusBar.showMessage("Menjalankan simulasi...")

        # initialize WSN
        wsn = WSN(num_nodes=num_nodes, area_size=area, init_energy=1.0)

        # Topologi
        ax = self.figures[0].gca()
        ax.clear()
        ax.scatter(wsn.pos[:, 0], wsn.pos[:, 1], c="#2b7cff", s=30)
        ax.set_title("Topologi Awal")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        self.canvases[0].draw()

        # HEED
        heed = HEED(wsn)
        ch = heed.select_cluster_heads()
        ax = self.figures[1].gca()
        ax.clear()
        wsn.plot_clusters(title="Clustering HEED", ax=ax)
        self.canvases[1].draw()

        # ACO
        graph = wsn.build_graph()
        aco = AntColony(graph, n_ants=n_ants, n_iterations=n_iter, decay=0.5)
        best_path, best_cost = aco.run(start=0, end=len(graph) - 1)
        ax = self.figures[2].gca()
        ax.clear()
        wsn.plot_routing(best_path, title="Routing ACO", ax=ax)
        self.canvases[2].draw()

        # Energi
        energies = wsn.simulate_transmission(best_path)
        ax = self.figures[3].gca()
        ax.clear()
        ax.plot(energies, marker="o")
        ax.set_title("Energi Residual Node")
        ax.set_xlabel("Round")
        ax.set_ylabel("Energi Rata-rata")
        self.canvases[3].draw()

        # Ringkasan
        summary = (
            f"📊 Ringkasan Hasil Simulasi\n\n"
            f"- Jumlah Node       : {num_nodes}\n"
            f"- Ukuran Area       : {area} x {area}\n"
            f"- Cluster Head      : {ch}\n"
            f"- Jalur ACO         : {best_path}\n"
            f"- Biaya Routing     : {best_cost:.2f}\n"
            f"- Energi Akhir Rata : {energies[-1]:.2f}\n"
        )
        self.summary_text.setPlainText(summary)

        # pindah ke ringkasan otomatis
        self.stack.setCurrentWidget(self.summary_page)
        self.statusBar.showMessage("Simulasi selesai")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WSNApp()
    # optional: start maximized on Full HD
    window.showMaximized()
    sys.exit(app.exec_())