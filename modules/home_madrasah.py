
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class HomeMadrasah(QMainWindow):
    def __init__(self):
        super(HomeMadrasah, self).__init__()
        loadUi("ui/home_madrasah.ui", self)
        self.setWindowTitle("Dashboard Madrasah")
