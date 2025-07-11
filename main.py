import sys
from PyQt5 import QtWidgets
from modules.login import LoginForm

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
