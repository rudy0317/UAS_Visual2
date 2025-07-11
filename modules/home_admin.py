from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from modules.admin_pusat.crud_kabupaten import CrudKabupaten
from modules.admin_pusat.crud_kecamatan import CrudKecamatan
from modules.admin_pusat.crud_madrasah import CrudMadrasah
from modules.admin_pusat.crud_provinsi import CrudProvinsi
from modules.admin_pusat.dashboard_admin import DashboardAdmin


class HomeAdmin(QMainWindow):
    def __init__(self):
        super(HomeAdmin, self).__init__()
        loadUi("ui/home_admin.ui", self)
        self.resize(1280, 720)
        self.setWindowTitle("Dashboard Admin Pusat")
        self.pageDashboard = None
        self.pageMadrasah = None
        self.login = None
        self.pageProvinsi = None
        self.pageKabupaten = None
        self.pageKecamatan = None
        self.btnDashboard.clicked.connect(self.load_dashboard)
        self.btnMadrasahGabungan.clicked.connect(self.load_madrasah_page)
        self.btnProvinsi.clicked.connect(self.load_provinsi_page)
        self.btnKabupaten.clicked.connect(self.load_kabupaten_page)
        self.btnKecamatan.clicked.connect(self.load_kecamatan_page)
        self.btnLogout.clicked.connect(self.logout)

    def load_dashboard(self):
        self.pageDashboard = DashboardAdmin()
        self.stackedPages.addWidget(self.pageDashboard)
        self.stackedPages.setCurrentWidget(self.pageDashboard)

    def load_madrasah_page(self):
        self.pageMadrasah = CrudMadrasah()
        self.stackedPages.addWidget(self.pageMadrasah)
        self.stackedPages.setCurrentWidget(self.pageMadrasah)

    def load_provinsi_page(self):
        self.pageProvinsi = CrudProvinsi()
        self.stackedPages.addWidget(self.pageProvinsi)
        self.stackedPages.setCurrentWidget(self.pageProvinsi)

    def load_kabupaten_page(self):
        self.pageKabupaten = CrudKabupaten()
        self.stackedPages.addWidget(self.pageKabupaten)
        self.stackedPages.setCurrentWidget(self.pageKabupaten)

    def load_kecamatan_page(self):
        self.pageKecamatan = CrudKecamatan()
        self.stackedPages.addWidget(self.pageKecamatan)
        self.stackedPages.setCurrentWidget(self.pageKecamatan)

    def logout(self):
        from modules.login import LoginForm
        self.login = LoginForm()
        self.login.show()
        self.close()
