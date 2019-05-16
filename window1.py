from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *

global pixmap

class FieldWidget(QWidget):

    def __init__(self, parent=None):
        super(FieldWidget, self).__init__(parent)

        self.cardPixmaps = []
        self.cardRects = []
        self.cardLocations = []
        self.highlightedRect = QRect()

        self.setAcceptDrops(True)
        self.setMinimumSize(1000, 600)
        self.setMaximumSize(1000, 600)
        self.update()


    def clear(self):
        self.cardLocations = []
        self.cardPixmaps = []
        self.cardRects = []
        self.highlightedRect = QRect()
        self.update()


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.updateRect = self.highlightedRect
        self.highlightedRect = QRect()
        self.update(self.updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('image'):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QRect()
            event.ignore()

        self.update(self.updateRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image'):
            cardData = event.mimeData().data('image')
            dataStream = QDataStream(cardData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            location = QPoint()
            dataStream >> pixmap >> location

            self.cardLocations.append(location)
            self.cardPixmaps.append(pixmap)

            self.hightlightedRect = QRect()

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QRect()
            event.ignore()


    def mousePressEvent(self, event):
        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)

        dataStream << pixmap << location

        mimeData = QMimeData()
        mimeData.setData('image/x-puzzle-card', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)

        if drag.exec_(Qt.MoveAction) != Qt.MoveAction:
            self.cardLocations.insert(found, location)
            self.cardPixmaps.insert(found, pixmap)
            self.cardRects.insert(found, square)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(self.rect(), Qt.white)
        painter.setBrush(QColor(255, 255, 0))
        SquareCount=20
        for i in range(0, SquareCount):
            painter.drawLine(0 + self.width() / SquareCount * i, 0, self.width() / SquareCount * i, self.height())
            painter.drawLine(0, self.height() / SquareCount * i, self.width(), self.height() / SquareCount * i)
        if self.highlightedRect.isValid():
            painter.setBrush(QColor("#ffcccc"))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for rect, pixmap in zip(self.cardRects, self.cardPixmaps):
            painter.drawPixmap(rect, pixmap)

        painter.end()



class CardList(QListWidget):
    def __init__(self, parent=None):
        super(CardList, self).__init__(parent)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(60, 60))
        self.setSpacing(10)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setMaximumSize(100, 400)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage():
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def addcard(self, pixmap, location):
        cardItem = QListWidgetItem(self)
        cardItem.setIcon(QIcon(pixmap))
        cardItem.setData(Qt.UserRole, pixmap)
        cardItem.setData(Qt.UserRole + 1, location)
        cardItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image'):
            cardData = event.mimeData().data('image')
            dataStream = QDataStream(cardData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            location = QPoint()
            dataStream >> pixmap >> location

            self.addcard(pixmap, location)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def addcard(self, pixmap, location):
        cardItem = QListWidgetItem(self)
        cardItem.setIcon(QIcon(pixmap))
        cardItem.setData(Qt.UserRole, pixmap)
        cardItem.setData(Qt.UserRole+1, location)
        cardItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

    def startDrag(self, supportedActions):
        item = self.currentItem()

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        pixmap = QPixmap(item.data(Qt.UserRole))
        location = item.data(Qt.UserRole+1)

        dataStream << pixmap << location

        mimeData = QMimeData()
        mimeData.setData('image', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            self.takeItem(self.row(item))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.showFullScreen()
        self.setupWidgets()


    def setupWidgets(self):
        frame = QFrame()
        frameLayout = QHBoxLayout(frame)
        self.screen = app.primaryScreen()
        self.screenSize = self.screen.size()
        self.rulesButton = QPushButton('Правила', self)
        self.rulesButton.setGeometry(0, 0, 100, 100)
        self.rulesButton.show()
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.setGeometry(self.screenSize.width() - 100, 0, 100, 100)
        self.exitButton.show()
        self.playButton = QPushButton('Играть', self)
        self.playButton.setGeometry(self.screenSize.width() / 2 - 50, self.screenSize  .height() / 2 - 50, 100, 100)
        self.playButton.show()
        self.rulesButton.clicked.connect(self.show_message)
        self.playButton.clicked.connect(self.start_game)
        self.exitButton.clicked.connect(self.exit_game)
        self.cardList = None
        self.cardList = CardList()
        self.cardList.setGeometry(0, 0, 100, 100)
        self.cardList.hide()
        self.fieldWidget = FieldWidget()
        self.fieldWidget.setGeometry(0, 0, 100, 100)
        self.fieldWidget.hide()
        self.setCentralWidget(frame)
        frameLayout.addWidget(self.fieldWidget)
        frameLayout.addWidget(self.cardList)
        frameLayout.addWidget(self.playButton)
        frameLayout.addWidget(self.rulesButton)
        frameLayout.addWidget(self.exitButton)
        self.setCentralWidget(frame)

    def exit_game(self):
        QCoreApplication.instance().quit()

    def show_message(self):
        text = "Как играть? Игру начинает самый младший игрок, затем ход передаётся по часовой стрелке. В свой ход вы можете совершить одно из двух действий. 1. Выложить 1, 2, 3 или 4 карты в линию по правилам (смотрите Правила выкладывания линий  ниже). В конце своего хода подсчитайте и запишите победные очки, полученные вами за этот ход. Доберите карты в руку до четырёх. \n 2. Пропустить ход. Пропуская ход, вы можете положить любое количество карт из руки (от 1 до 4) под низ колоды и взять из неё соответствующее количество карт взамен. Менять таким образом карты не обязательно. \n Правила выкладывания линий Выкладывая карты в линию, вы должны соблюдать три условия: 1. Сторона. Каждая из выкладываемых карт должна хотя бы одной из сторон касаться уже лежащей на столе карты. 2. Линия. Вы можете выкладывать карты только в одну линию. То есть, вы можете: • создать/продолжить линию с одной стороны от ранее выложенной карты, • создать/продолжить линию с двух стороны от ранее выложенной карты (см. Ход 2). При этом у вас могут возникать и/или продолжаться и другие линии 3. Признаки. У карт в одной линии каждый из признаков (цвет, форма и число), рассмотренных по отдельности, должен быть или одинаковым для всех карт, или совсем разным для всех карт.  Карты в линии могут идти в любом порядке. Если между картами есть пустые  места, такие карты не считаются линией. В линии может быть не более 4 карт. Линия из 4 карт называется цепочкой. \n Подсчёт очков После каждого хода, подсчитайте  количество очков за каждую линию, созданную или продолженную вами в этот ход – для этого сложите числа, указанные на картах в линии. Если карта попадает в 2 линии, то и считать очки за нее нужно дважды. За каждую созданную цепочку (линию из 4 карт) удвойте все очки за этот ход. Удвойте очки снова, если в этот ход вы использовали все 4 карты из руки. Конец игры Игра завершается, когда заканчивается стопка карт и один из игроков выкладывает свою последнюю карту. Если вы выложили последнюю карту, удвойте количество очков за этот ход. Тот, кто набрал больше всего очков – выигрывает!"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Правила")
        msg.setInformativeText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def start_game(self):
        self.playButton.hide()
        self.rulesButton.hide()
        self.cardList.show()
        self.fieldWidget.show()

    def openImage(self, path=None):
        if not path:
            path = QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png *.jpg *.bmp)")

        if path:
            newImage = QPixmap()
            if not newImage.load(path):
                QMessageBox.warning(self, "Open Image",
                        "The image file could not be loaded.",
                        QMessageBox.Cancel)
                return

            self.puzzleImage = newImage
            self.setupPuzzle()



if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()