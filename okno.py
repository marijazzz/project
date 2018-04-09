import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import drawing as d
import random


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):

        self.resize(800, 700)
        self.center()
        self.setWindowTitle('Center')
        self.label = QLabel(self)
        self.label.resize(200, 40)
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        u = d.Point(600, 300)
        u.draw(qp)
        # self.draw_points(qp)
        qp.end()



    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))



