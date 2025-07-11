from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from database.koneksi import create_connection

class FormKabupaten(QDialog):
    def __init__(self, mode='tambah', data=None):
        super().__init__()
        loadUi("ui/admin_pusat/form_kabupaten.ui", self)
        self.setWindowTitle("Form Kabupaten")

        self.provinsi_map = {}
        self.load_provinsi()

        if mode == 'edit' and data:
            self.inputNama.setText(data['nama'])
            index = self.comboProvinsi.findText(data['provinsi'])
            if index >= 0:
                self.comboProvinsi.setCurrentIndex(index)

        self.btnSimpan.clicked.connect(self.accept)
        self.btnBatal.clicked.connect(self.reject)

    def load_provinsi(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_provinsi, nama_provinsi FROM provinsi")
        for id_prov, nama in cursor.fetchall():
            self.comboProvinsi.addItem(nama)
            self.provinsi_map[nama] = id_prov
        conn.close()

    def get_data(self):
        nama = self.inputNama.text().strip()
        prov = self.comboProvinsi.currentText()
        return {'nama': nama, 'id_provinsi': self.provinsi_map.get(prov)}
