#определение рисования

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


