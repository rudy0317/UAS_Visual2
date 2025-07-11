from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from database.koneksi import create_connection
from modules.admin_pusat.form_kabupaten import FormKabupaten
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument

class CrudKabupaten(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/admin_pusat/crud_kabupaten.ui", self)
        self.setWindowTitle("Manajemen Data Kabupaten")
        self.inputCari.textChanged.connect(self.load_data)
        self.btnTambah.clicked.connect(self.tambah_data_popup)
        self.btnEdit.clicked.connect(self.edit_data_popup)
        self.btnHapus.clicked.connect(self.hapus_data)
        self.btnPrint.clicked.connect(self.print_pdf)
        self._print_doc = None
        self.load_data()

    def load_data(self):
        keyword = self.inputCari.text().strip().lower()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.id_kabupaten, k.nama_kabupaten, p.nama_provinsi
            FROM kabupaten k
            JOIN provinsi p ON k.id_provinsi = p.id_provinsi
        """)
        result = cursor.fetchall()
        self.tableKabupaten.setRowCount(0)
        self.tableKabupaten.setColumnCount(3)
        self.tableKabupaten.setHorizontalHeaderLabels(["ID", "Nama Kabupaten", "Provinsi"])

        for row_data in result:
            if keyword in row_data[1].lower():  # Cari berdasarkan nama_kabupaten
                row_num = self.tableKabupaten.rowCount()
                self.tableKabupaten.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tableKabupaten.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))

        conn.close()
        self.tableKabupaten.setColumnHidden(0, True)

    def tambah_data_popup(self):
        form = FormKabupaten(mode='tambah')
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kabupaten (nama_kabupaten, id_provinsi) VALUES (%s, %s)",
                           (data['nama'], data['id_provinsi']))


            conn.commit()
            conn.close()
            self.load_data()

    def edit_data_popup(self):
        row = self.tableKabupaten.currentRow()
        if row >= 0:
            id_kab = self.tableKabupaten.item(row, 0).text()  # id_kabupaten
            nama_kab = self.tableKabupaten.item(row, 1).text()  # nama_kabupaten
            nama_prov = self.tableKabupaten.item(row, 2).text()  # nama_provinsi

            form = FormKabupaten(mode='edit', data={
                'nama': nama_kab,
                'provinsi': nama_prov
            })

            if form.exec_() == QDialog.Accepted:
                data = form.get_data()
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE kabupaten 
                    SET nama_kabupaten=%s, id_provinsi=%s 
                    WHERE id_kabupaten=%s
                """, (data['nama'], data['id_provinsi'], id_kab))
                conn.commit()
                conn.close()
                self.load_data()
        else:
            QMessageBox.warning(self, "Pilih Data", "Pilih baris yang ingin diedit.")

    def hapus_data(self):
        row = self.tableKabupaten.currentRow()
        if row >= 0:
            id_kab = self.tableKabupaten.item(row, 0).text()  # id_kabupaten
            nama_kab = self.tableKabupaten.item(row, 1).text()  # nama_kabupaten

            confirm = QMessageBox.question(
                self,
                "Konfirmasi Hapus",
                f"Kabupaten <b>{nama_kab}</b> akan dihapus.\n"
                "Semua kecamatan yang terkait juga akan ikut terhapus.\n\n"
                "Yakin ingin melanjutkan?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )


            if confirm == QMessageBox.Yes:
                try:
                    conn = create_connection()
                    cursor = conn.cursor()

                    # Hapus kecamatan terlebih dahulu
                    cursor.execute("DELETE FROM kecamatan WHERE id_kabupaten = %s", (id_kab,))

                    # Baru hapus kabupaten
                    cursor.execute("DELETE FROM kabupaten WHERE id_kabupaten = %s", (id_kab,))

                    conn.commit()
                    conn.close()

                    QMessageBox.information(self, "Sukses",
                                            f"Data kabupaten <b>{nama_kab}</b> dan semua kecamatan terkait berhasil dihapus.")
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Gagal", f"Gagal menghapus data:\n{e}")
        else:
            QMessageBox.warning(self, "Pilih Data", "Pilih baris yang ingin dihapus.")

    
    def print_pdf(self):
        html = """
            <h2 style='text-align: center;'>DAFTAR KABUPATEN</h2>
            <table border='1' cellspacing='0' cellpadding='4' width='100%'>
        """

        # Ambil index kolom yang tidak disembunyikan dan bukan ID
        visible_columns = [
            i for i in range(self.tableKabupaten.columnCount())
            if not self.tableKabupaten.isColumnHidden(i)
               and self.tableKabupaten.horizontalHeaderItem(i).text() != "ID"
        ]

        # Header
        html += "<tr><th width='40' align='center'>No</th>"
        for col in visible_columns:
            header = self.tableKabupaten.horizontalHeaderItem(col).text()
            html += f"<th>{header}</th>"
        html += "</tr>"

        # Baris data
        for row in range(self.tableKabupaten.rowCount()):
            html += f"<tr><td align='center' width='40'>{row + 1}</td>"
            for col in visible_columns:
                item = self.tableKabupaten.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"

        html += "</table>"

        # Cetak
        self._print_doc = QTextDocument()
        self._print_doc.setHtml(html)

        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Preview Cetak PDF")
        preview.paintRequested.connect(self._print_doc.print_)
        preview.exec_()

