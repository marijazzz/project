import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        coord = (self.x, self.y)
        return coord

    def draw(self, painter):
        painter.setPen(Qt.red)
        painter.drawPoint(self.x, self.y)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(800, 700)
        self.center()

        self.setWindowTitle('Center')
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        u = Point(600, 300)
        u.draw(qp)
        # self.draw_points(qp)
        qp.end()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
