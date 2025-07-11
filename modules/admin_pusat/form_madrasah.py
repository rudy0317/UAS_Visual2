from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from database.koneksi import create_connection

class FormMadrasah(QDialog):
    def __init__(self, mode='tambah', data=None):
        super().__init__()
        loadUi("ui/admin_pusat/form_madrasah.ui", self)
        self.setWindowTitle("Form Madrasah Ibtidaiyah")

        self.mode = mode
        self.data = data

        self.isi_combo_kecamatan()
        self.btnSimpan.clicked.connect(self.validasi_dan_terima)
        self.btnBatal.clicked.connect(self.reject)
        if self.mode == 'edit' and self.data:
            self.inputNama.setText(self.data['nama'])
            self.inputAlamat.setText(self.data['alamat'])
            self.inputGuru.setText(str(self.data['guru']))
            self.inputSiswa.setText(str(self.data['siswa']))
            self.inputTahun.setText(str(self.data['tahun']))
            self.set_kecamatan(self.data['id_kecamatan'])



    def isi_combo_kecamatan(self):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan")
            results = cursor.fetchall()
            self.comboKecamatan.clear()
            self.comboKecamatan.addItem("-- Pilih Kecamatan--", None)
            for id_kec, nama in results:
                self.comboKecamatan.addItem(nama, id_kec)
            conn.close()

    def set_kecamatan(self, id_kecamatan):
        index = self.comboKecamatan.findData(id_kecamatan)
        if index >= 0:
            self.comboKecamatan.setCurrentIndex(index)

    def get_data(self):
        # Buat Validasi
        if not self.inputNama.text() or not self.inputAlamat.text() or not self.inputGuru.text() or not self.inputSiswa.text() or not self.inputTahun.text():
            QMessageBox.warning(self, "Input Tidak Lengkap", "Semua field harus diisi.")
            return None

        if self.comboKecamatan.currentData() is None:
            QMessageBox.warning(self, "Input Tidak Lengkap", "Silakan pilih kecamatan terlebih dahulu.")
            return None

        return {
            'nama': self.inputNama.text(),
            'alamat': self.inputAlamat.text(),
            'id_kecamatan': self.comboKecamatan.currentData(),
            'guru': self.inputGuru.text(),
            'siswa': self.inputSiswa.text(),
            'tahun': self.inputTahun.text()
        }

    def validasi_dan_terima(self):
        if not self.inputNama.text() or not self.inputAlamat.text() or \
                not self.inputGuru.text() or not self.inputSiswa.text() or \
                not self.inputTahun.text():
            QMessageBox.warning(self, "Input Tidak Lengkap", "Semua field harus diisi.")
            return

        if self.comboKecamatan.currentData() is None:
            QMessageBox.warning(self, "Input Tidak Lengkap", "Silakan pilih kecamatan terlebih dahulu.")
            return

        self.accept()

