from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from database.koneksi import create_connection
from modules.admin_pusat.form_kecamatan import FormKecamatan
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument


class CrudKecamatan(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/admin_pusat/crud_kecamatan.ui", self)
        self.setWindowTitle("Manajemen Data Kecamatan")
        self.inputCari.textChanged.connect(self.load_data)
        self.btnTambah.clicked.connect(self.tambah_data_popup)
        self.btnEdit.clicked.connect(self.edit_data_popup)
        self.btnHapus.clicked.connect(self.hapus_data)
        self.btnPrint.clicked.connect(self.print)
        self._print_doc = None

        # Inisialisasi tabel
        self.tableKecamatan.setColumnCount(3)  # Sesuaikan dengan jumlah kolom
        self.tableKecamatan.setHorizontalHeaderLabels(["ID", "Nama Kecamatan", "Kabupaten"])
        self.tableKecamatan.setColumnHidden(0, True)  # Sembunyikan kolom ID
        self.load_data()

    def load_data(self):
        keyword = self.inputCari.text().strip().lower()
        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Error", "Gagal terhubung ke database")
            return

        try:
            cursor = conn.cursor()
            # Query dengan JOIN untuk mendapatkan nama kabupaten
            cursor.execute("""
                SELECT k.id_kecamatan, k.nama_kecamatan, b.nama_kabupaten 
                FROM kecamatan k
                JOIN kabupaten b ON k.id_kabupaten = b.id_kabupaten
            """)
            result = cursor.fetchall()

            self.tableKecamatan.setRowCount(0)

            for row_data in result:
                if keyword in row_data[1].lower() or keyword in row_data[2].lower():
                    row_num = self.tableKecamatan.rowCount()
                    self.tableKecamatan.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        self.tableKecamatan.setItem(row_num, col_num,
                                                    QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")
        finally:
            conn.close()

    def tambah_data_popup(self):
        form = FormKecamatan(mode='tambah')
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = create_connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "Gagal terhubung ke database")
                return

            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO kecamatan (nama_kecamatan, id_kabupaten) 
                    VALUES (%s, %s)
                """, (data['nama'], data['id_kabupaten']))
                conn.commit()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menambah data: {str(e)}")
            finally:
                conn.close()

    def edit_data_popup(self):
        row = self.tableKecamatan.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Data", "Pilih baris yang ingin diedit.")
            return

        try:
            id_kec = self.tableKecamatan.item(row, 0).text()
            nama_kec = self.tableKecamatan.item(row, 1).text()
            nama_kab = self.tableKecamatan.item(row, 2).text()

            form = FormKecamatan(mode='edit', data={
                'nama': nama_kec,
                'kabupaten': nama_kab
            })

            if form.exec_() == QDialog.Accepted:
                data = form.get_data()
                conn = create_connection()
                if conn is None:
                    QMessageBox.critical(self, "Error", "Gagal terhubung ke database")
                    return

                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE kecamatan 
                        SET nama_kecamatan=%s, id_kabupaten=%s 
                        WHERE id_kecamatan=%s
                    """, (data['nama'], data['id_kabupaten'], id_kec))
                    conn.commit()
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Gagal mengupdate data: {str(e)}")
                finally:
                    conn.close()

        except AttributeError:
            QMessageBox.warning(self, "Error", "Data tidak valid")

    def hapus_data(self):
        row = self.tableKecamatan.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Data", "Pilih baris yang ingin dihapus.")
            return

        try:
            id_kec = self.tableKecamatan.item(row, 0).text()
            nama_kec = self.tableKecamatan.item(row, 1).text()

            confirm = QMessageBox.question(
                self,
                "Konfirmasi Hapus",
                f"Kecamatan <b>{nama_kec}</b> akan dihapus.\n"
                "Semua madrasah di kecamatan ini juga akan ikut terhapus.\n\n"
                "Yakin ingin melanjutkan?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                conn = create_connection()
                if conn is None:
                    QMessageBox.critical(self, "Error", "Gagal terhubung ke database")
                    return

                try:
                    cursor = conn.cursor()
                    # Hapus madrasah terlebih dahulu
                    cursor.execute("DELETE FROM madrasah WHERE id_kecamatan = %s", (id_kec,))
                    # Hapus kecamatan
                    cursor.execute("DELETE FROM kecamatan WHERE id_kecamatan = %s", (id_kec,))
                    conn.commit()
                    QMessageBox.information(self, "Sukses",
                                            f"Kecamatan <b>{nama_kec}</b> dan semua madrasah terkait berhasil dihapus.")
                    self.load_data()
                except Exception as e:
                    conn.rollback()
                    QMessageBox.critical(self, "Gagal", f"Gagal menghapus data:\n{str(e)}")
                finally:
                    conn.close()

        except AttributeError:
            QMessageBox.warning(self, "Error", "Data tidak valid")


    def print(self):
        html = """
            <h2 style='text-align: center;'>DAFTAR KECAMATAN</h2>
            <table border='1' cellspacing='0' cellpadding='4' width='100%'>
        """

        # Ambil kolom yang akan ditampilkan (tanpa kolom ID jika ada)
        visible_columns = [
            i for i in range(self.tableKecamatan.columnCount())
            if not self.tableKecamatan.isColumnHidden(i)
               and self.tableKecamatan.horizontalHeaderItem(i).text() != "ID"
        ]

        # Header tabel
        html += "<tr><th width='40' align='center'>No</th>"
        for col in visible_columns:
            header = self.tableKecamatan.horizontalHeaderItem(col).text()
            html += f"<th>{header}</th>"
        html += "</tr>"

        # Baris data
        for row in range(self.tableKecamatan.rowCount()):
            html += f"<tr><td align='center' width='40'>{row + 1}</td>"
            for col in visible_columns:
                item = self.tableKecamatan.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"

        html += "</table>"

        # Cetak dengan preview
        self._print_doc = QTextDocument()
        self._print_doc.setHtml(html)

        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Preview Cetak Data Kecamatan")
        preview.paintRequested.connect(self._print_doc.print_)
        preview.exec_()
