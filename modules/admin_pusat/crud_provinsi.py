from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from database.koneksi import create_connection
from modules.admin_pusat.form_provinsi import FormProvinsi
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument


class CrudProvinsi(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/admin_pusat/crud_provinsi.ui", self)
        self.setWindowTitle("Manajemen Data Provinsi")
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
            SELECT * FROM provinsi
        """)
        result = cursor.fetchall()
        self.tableProvinsi.setRowCount(0)
        self.tableProvinsi.setColumnCount(2)
        self.tableProvinsi.setHorizontalHeaderLabels(["ID", "Nama Provinsi"])

        for row_data in result:
            if keyword in row_data[1].lower():
                row_num = self.tableProvinsi.rowCount()
                self.tableProvinsi.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tableProvinsi.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))

        conn.close()
        self.tableProvinsi.setColumnHidden(0, True)

    def tambah_data_popup(self):
        form = FormProvinsi(mode='tambah')
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            if not data:
                return
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO provinsi (nama_provinsi) VALUES (%s)", (data['nama'],))
                conn.commit()
                conn.close()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Gagal", str(e))

    def edit_data_popup(self):
        row = self.tableProvinsi.currentRow()
        if row >= 0:
            id_provinsi = self.tableProvinsi.item(row, 0).text()
            nama_lama = self.tableProvinsi.item(row, 1).text()
            form = FormProvinsi(mode='edit', data={'nama': nama_lama})
            if form.exec_() == QDialog.Accepted:
                data = form.get_data()
                if not data:
                    return
                try:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE provinsi SET nama_provinsi=%s WHERE id_provinsi=%s",
                                   (data['nama'], id_provinsi))
                    conn.commit()
                    conn.close()
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Gagal", str(e))
        else:
            QMessageBox.warning(self, "Pilih Data", "Pilih data yang ingin diedit.")

    def hapus_data(self):
        row = self.tableProvinsi.currentRow()
        if row >= 0:
            id_provinsi = self.tableProvinsi.item(row, 0).text()
            nama = self.tableProvinsi.item(row, 1).text()

            # Tampilkan konfirmasi dengan warning berjenjang
            confirm = QMessageBox.question(
                self,
                "Konfirmasi Hapus",
                f"Provinsi <b>{nama}</b> akan dihapus.\n"
                "Semua kabupaten dan kecamatan yang terkait juga akan ikut terhapus.\n\n"
                "Yakin ingin melanjutkan?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    conn = create_connection()
                    cursor = conn.cursor()

                    # 1. Hapus kecamatan
                    delete_kecamatan = """
                        DELETE FROM kecamatan
                        WHERE id_kabupaten IN (
                            SELECT id_kabupaten FROM kabupaten WHERE id_provinsi = %s
                        )
                    """
                    cursor.execute(delete_kecamatan, (id_provinsi,))

                    # 2. Hapus kabupaten
                    delete_kabupaten = "DELETE FROM kabupaten WHERE id_provinsi = %s"
                    cursor.execute(delete_kabupaten, (id_provinsi,))

                    # 3. Hapus provinsi
                    delete_provinsi = "DELETE FROM provinsi WHERE id_provinsi = %s"
                    cursor.execute(delete_provinsi, (id_provinsi,))

                    conn.commit()
                    conn.close()

                    QMessageBox.information(self, "Sukses",
                                            f"Provinsi '{nama}' dan semua data terkait berhasil dihapus.")
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Gagal", f"Gagal menghapus data:\n{e}")
        else:
            QMessageBox.warning(self, "Pilih Data", "Pilih data yang ingin dihapus.")

    def print_pdf(self):
        html = """
            <h2 style='text-align: center;'>DAFTAR PROVINSI</h2>
            <table border='1' cellspacing='0' cellpadding='4' width='100%'>
        """

        headers = [
            self.tableProvinsi.horizontalHeaderItem(i).text()
            for i in range(self.tableProvinsi.columnCount())
            if not self.tableProvinsi.isColumnHidden(i)
        ]

        html += "<tr><th width='50'>No</th>" + "".join(
            f"<th>{header}</th>" for header in headers if header != "ID"
        ) + "</tr>"

        for row in range(self.tableProvinsi.rowCount()):
            html += f"<tr><td align='center' width='50'>{row + 1}</td>"
            for col in range(self.tableProvinsi.columnCount()):
                if self.tableProvinsi.isColumnHidden(col):
                    continue
                item = self.tableProvinsi.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"

        html += "</table>"

        doc = QTextDocument()
        doc.setHtml(html)

        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(doc.print_)
        preview.exec_()
