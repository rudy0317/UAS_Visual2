from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QVBoxLayout, QFrame, QWidget
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from database.koneksi import create_connection
from modules.admin_pusat.crud_provinsi import CrudProvinsi
from modules.admin_pusat.crud_kabupaten import CrudKabupaten
from modules.admin_pusat.crud_kecamatan import CrudKecamatan
from modules.admin_pusat.crud_madrasah import CrudMadrasah



class DashboardAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Admin Pusat")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        self.cards = {}
        items = [
            ("Provinsi", "icons/provinsi.svg"),
            ("Kabupaten", "icons/kabupaten.png"),
            ("Kecamatan", "icons/kecamatan.png"),
            ("Madrasah", "icons/madrasah.png")
        ]

        for i, (label, icon_path) in enumerate(items):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    border: 1px solid #ccc;
                    border-radius: 12px;
                    background-color: #f8f9fa;
                    padding: 12px;
                }
                QLabel {
                    font-size: 14pt;
                }
            """)
            vbox = QVBoxLayout(card)

            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_path).scaled(48, 48))

            title_label = QLabel(f"Total {label}")
            count_label = QLabel("...")
            count_label.setObjectName(f"label{label}")
            count_label.setStyleSheet("font-size: 24pt; font-weight: bold;")

            vbox.addWidget(icon_label)
            vbox.addWidget(title_label)
            vbox.addWidget(count_label)

            self.grid.addWidget(card, i // 2, i % 2)
            self.cards[label.lower()] = count_label
            if label == "Provinsi":
                card.mousePressEvent = self.buka_provinsi
            elif label == "Kabupaten":
                card.mousePressEvent = self.buka_kabupaten
            elif label == "Kecamatan":
                card.mousePressEvent = self.buka_kecamatan
            elif label == "Madrasah":
                card.mousePressEvent = self.buka_madrasah

        # Chart
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.load_data()

    def load_data(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM provinsi")
            self.cards["provinsi"].setText(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM kabupaten")
            self.cards["kabupaten"].setText(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM kecamatan")
            self.cards["kecamatan"].setText(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM madrasah")
            self.cards["madrasah"].setText(str(cursor.fetchone()[0]))

            # Grafik pie jenjang madrasah
            cursor.execute("SELECT jenjang, COUNT(*) FROM madrasah GROUP BY jenjang")
            data = cursor.fetchall()
            labels = [row[0] for row in data]
            sizes = [row[1] for row in data]

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title("Distribusi Madrasah per Jenjang")
            self.canvas.draw()

            conn.close()
        except Exception as e:
            print(f"[ERROR Dashboard] {e}")

    def buka_provinsi(self, _):
        self.window_provinsi = CrudProvinsi()
        self.window_provinsi.show()

    def buka_kabupaten(self, _):
        self.window_kabupaten = CrudKabupaten()
        self.window_kabupaten.show()


    def buka_kecamatan(self, _):
        self.window_kecamatan = CrudKecamatan()
        self.window_kecamatan.show()

    def buka_madrasah(self, _):
        self.window_madrasah = CrudMadrasah()
        self.window_madrasah.show()
