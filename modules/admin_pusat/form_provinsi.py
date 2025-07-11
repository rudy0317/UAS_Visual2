from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class FormProvinsi(QDialog):
    def __init__(self, mode='tambah', data=None):
        super().__init__()
        loadUi("ui/admin_pusat/form_provinsi.ui", self)
        self.setWindowTitle("Form Provinsi")

        self.mode = mode
        if mode == 'edit' and data:
            self.inputNama.setText(data['nama'])

        self.btnSimpan.clicked.connect(self.accept)
        self.btnBatal.clicked.connect(self.reject)

    def get_data(self):
        nama = self.inputNama.text().strip()
        if not nama:
            return None
        return {'nama': nama}
