
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from database.koneksi import create_connection
from modules.admin_pusat.form_madrasah import FormMadrasah
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument


class CrudMadrasah(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/admin_pusat/crud_madrasah.ui", self)
        self.setWindowTitle("Manajemen Data Madrasah")

        self.comboJenjang.addItems(["MI", "MTs", "MA"])
        self.comboJenjang.currentIndexChanged.connect(self.load_data)
        self.inputCari.textChanged.connect(self.load_data)
        self.btnTambah.clicked.connect(self.tambah_data_popup)
        self.btnEdit.clicked.connect(self.edit_data_popup)
        self.btnHapus.clicked.connect(self.hapus_data)
        self.btnPrint.clicked.connect(self.print_pdf)
        self._print_doc = None

        self.load_data()

    
    def load_data(self):
        jenjang = self.comboJenjang.currentText()
        keyword = self.inputCari.text().strip().lower()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id_madrasah, m.nama_madrasah, m.jenjang, m.alamat,
                   k.nama_kecamatan, m.jumlah_guru, m.jumlah_siswa, m.tahun_berdiri
            FROM madrasah m
            JOIN kecamatan k ON m.id_kecamatan = k.id_kecamatan
            WHERE m.jenjang = %s
        """, (jenjang,))
        result = cursor.fetchall()
        self.tableMadrasah.setRowCount(0)
        self.tableMadrasah.setColumnCount(8)
        self.tableMadrasah.setHorizontalHeaderLabels([
            "ID", "Nama", "Jenjang", "Alamat", "Kecamatan",
            "Jumlah Guru", "Jumlah Siswa", "Tahun Berdiri"
        ])

        for row_data in result:
            if (keyword in row_data[1].lower() or
                keyword in row_data[3].lower() or
                keyword in row_data[4].lower()):
                row_num = self.tableMadrasah.rowCount()
                self.tableMadrasah.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tableMadrasah.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))

        conn.close()
        self.tableMadrasah.setColumnHidden(0, True)

    def tambah_data_popup(self):
        form = FormMadrasah(mode='tambah')
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            if not data:
                return
            jenjang = self.comboJenjang.currentText()
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO madrasah (nama_madrasah, alamat, jenjang, id_kecamatan,
                                          jumlah_guru, jumlah_siswa, tahun_berdiri)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (data['nama'], data['alamat'], jenjang,
                      data['id_kecamatan'], data['guru'], data['siswa'], data['tahun']))
                conn.commit()
                conn.close()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Gagal", str(e))

    def edit_data_popup(self):
        row = self.tableMadrasah.currentRow()
        if row >= 0:
            id_madrasah = self.tableMadrasah.item(row, 0).text()
            nama_kec = self.tableMadrasah.item(row, 4).text()

            # Cari id_kecamatan berdasarkan nama_kecamatan
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_kecamatan FROM kecamatan WHERE nama_kecamatan = %s", (nama_kec,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                QMessageBox.critical(self, "Error", "ID kecamatan tidak ditemukan.")
                return

            id_kecamatan = result[0]

            data_awal = {
                'nama': self.tableMadrasah.item(row, 1).text(),
                'alamat': self.tableMadrasah.item(row, 3).text(),
                'id_kecamatan': id_kecamatan,
                'guru': self.tableMadrasah.item(row, 5).text(),
                'siswa': self.tableMadrasah.item(row, 6).text(),
                'tahun': self.tableMadrasah.item(row, 7).text()
            }

            form = FormMadrasah(mode='edit', data=data_awal)
            if form.exec_() == QDialog.Accepted:
                data = form.get_data()
                if not data:
                    return
                try:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE madrasah
                        SET nama_madrasah=%s, alamat=%s, id_kecamatan=%s,
                            jumlah_guru=%s, jumlah_siswa=%s, tahun_berdiri=%s
                        WHERE id_madrasah=%s
                    """, (data['nama'], data['alamat'], data['id_kecamatan'],
                          data['guru'], data['siswa'], data['tahun'], id_madrasah))
                    conn.commit()
                    conn.close()
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Gagal", str(e))
        else:
            QMessageBox.warning(self, "Pilih Data", "Pilih data yang ingin diedit.")

    def hapus_data(self):
        row = self.tableMadrasah.currentRow()
        if row >= 0:
            id_madrasah = self.tableMadrasah.item(row, 0).text()
            nama = self.tableMadrasah.item(row, 1).text()
            confirm = QMessageBox.question(
                self,
                "Konfirmasi Hapus",
                f"Yakin ingin menghapus madrasah: <b>{nama}<b> ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                try:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM madrasah WHERE id_madrasah=%s", (id_madrasah,))
                    conn.commit()
                    conn.close()
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Gagal", str(e))
        else:
            QMessageBox.warning(self, "Pilih Data", "Pilih data yang ingin dihapus.")

    
    def print_pdf(self):
        html = """
            <h2 style='text-align: center;'>DAFTAR MADRASAH</h2>
            <table border='1' cellspacing='0' cellpadding='4' width='100%'>
        """

        # Ambil kolom yang ditampilkan selain kolom ID
        visible_columns = [
            i for i in range(self.tableMadrasah.columnCount())
            if not self.tableMadrasah.isColumnHidden(i)
               and self.tableMadrasah.horizontalHeaderItem(i).text() != "ID"
        ]

        # Header tabel
        html += "<tr><th width='40' align='center'>No</th>"
        for col in visible_columns:
            header = self.tableMadrasah.horizontalHeaderItem(col).text()
            html += f"<th>{header}</th>"
        html += "</tr>"

        # Data baris
        for row in range(self.tableMadrasah.rowCount()):
            html += f"<tr><td align='center' width='40'>{row + 1}</td>"
            for col in visible_columns:
                item = self.tableMadrasah.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"

        html += "</table>"

        # Preview cetak
        self._print_doc = QTextDocument()
        self._print_doc.setHtml(html)

        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Preview Cetak Data Madrasah")
        preview.paintRequested.connect(self._print_doc.print_)
        preview.exec_()

        
