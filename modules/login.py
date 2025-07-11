import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from database.koneksi import create_connection


class LoginForm(QMainWindow):
    def __init__(self):
        super(LoginForm, self).__init__()
        loadUi("ui/login.ui", self)
        self.window = None

        self.setWindowTitle("Login - Sistem Madrasah")
        self.btnLogin.clicked.connect(self.login_aksi)

    def login_aksi(self):
        user = self.lineEditUsername.text()
        pwd = self.lineEditPassword.text()

        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Gagal Koneksi", "Tidak bisa terhubung ke database.")
            return

        try:
            cursor = conn.cursor()
            query = "SELECT role FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (user, pwd))
            result = cursor.fetchone()

            if result:
                role = result[0]
                if role == "admin_pusat":
                    self.open_admin_pusat()
                elif role =="admin_provinsi":
                    self.open_admin_provinsi()
                elif role == "madrasah":
                    self.open_madrasah()
                else:
                    QMessageBox.warning(self, "Akses Ditolak", "Role tidak dikenali atau tidak diizinkan.")
            else:
                QMessageBox.warning(self, "Login Gagal", "Username atau Password salah.")

        except Exception as e:
            QMessageBox.critical(self, "Error DB", str(e))
        finally:
            conn.close()

    def open_admin_pusat(self):
        from modules.home_admin import HomeAdmin
        self.window = HomeAdmin()
        self.window.show()
        self.close()

    def open_admin_provinsi(self):
        from modules.home_admin_provinsi import HomeAdminProvinsi
        self.window = HomeAdminProvinsi()
        self.window.show()
        self.close()

    def open_madrasah(self):
        from modules.home_madrasah import HomeMadrasah
        self.window = HomeMadrasah()
        self.window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
