
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class HomeAdminProvinsi(QMainWindow):
    def __init__(self):
        super(HomeAdminProvinsi, self).__init__()
        loadUi("ui/home_admin_provinsi.ui", self)
        self.setWindowTitle("Dashboard Admin Provinsi")
