from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class FormWilayah(QDialog):
    def __init__(self, mode='tambah', nama='', relasi_list=None, relasi_label=''):
        super().__init__()
        loadUi("ui/admin_pusat/form_wilayah.ui", self)

        self.setWindowTitle("Form Wilayah")
        self.mode = mode
        self.relasi_id = None

        # Set input default (kalau mode edit)
        self.inputNama.setText(nama)

        # Atur ComboBox relasi (jika ada)
        if relasi_list:
            self.comboRelasi.setVisible(True)
            self.comboRelasi.clear()
            self.comboRelasi.addItem(f"-- Pilih {relasi_label} --", None)
            for id_val, display in relasi_list:
                self.comboRelasi.addItem(display, id_val)
        else:
            self.comboRelasi.setVisible(False)

        self.btnSimpan.clicked.connect(self.accept)
        self.btnBatal.clicked.connect(self.reject)

    def get_data(self):
        nama = self.inputNama.text().strip()
        relasi_id = self.comboRelasi.currentData() if self.comboRelasi.isVisible() else None
        return {
            'nama': nama,
            'relasi_id': relasi_id
        }
