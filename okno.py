#Все действия в окне

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent
import drawing as d
import random


class Example(QWidget):
    global x_g, y_g
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
        u = d.Point(e.x, e.y)
        u.draw(qp)
        qp.end()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()


        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)

    def mousePressEvent(self, e):
        if e.type() == QEvent.MouseButtonPress:
            print('mousePressEvent')




