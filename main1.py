import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
import okno
import drawing


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = okno.Example()
    sys.exit(app.exec_())