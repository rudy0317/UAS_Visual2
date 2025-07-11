from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from database.koneksi import create_connection

class FormKecamatan(QDialog):
    def __init__(self, mode='tambah', data=None):
        super().__init__()
        loadUi("ui/admin_pusat/form_kecamatan.ui", self)
        self.setWindowTitle("Form Kecamatan")

        self.kabupaten_map = {}
        self.load_kabupaten()

        if mode == 'edit' and data:
            self.inputNama.setText(data['nama'])
            index = self.comboKabupaten.findText(data['kabupaten'])
            if index >= 0:
                self.comboKabupaten.setCurrentIndex(index)

        self.btnSimpan.clicked.connect(self.accept)
        self.btnBatal.clicked.connect(self.reject)

    def load_kabupaten(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_kabupaten, nama_kabupaten FROM kabupaten")
        for id_kab, nama in cursor.fetchall():
            self.comboKabupaten.addItem(nama)
            self.kabupaten_map[nama] = id_kab
        conn.close()

    def get_data(self):
        nama = self.inputNama.text().strip()
        kab = self.comboKabupaten.currentText()
        return {'nama': nama, 'id_kabupaten': self.kabupaten_map.get(kab)}
