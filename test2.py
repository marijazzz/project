import sip

sip.setapi('QVariant', 2)

import random

from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class tile():
    def __init__(self):
        self.card = None
        self.player = None
        self.piecePixmap = None

    def setcard(self, card_Id):
        self.card = card_Id

    def setpixmap(self, pixmap):
        self.card = 1
        self.piecePixmap = pixmap

    def getpixmap(self):
        return self.piecePixmap


class PuzzleWidget(QWidget):
    puzzleCompleted = QtCore.pyqtSignal()

    def __init__(self, parent=None):

        super(PuzzleWidget, self).__init__()
        self.parent = parent
        self.FIELDSIZE = 103
        self.TILESIZE = 100
        self.playfield = [[0] * self.FIELDSIZE for i in range(self.FIELDSIZE)]
        for i in range(self.FIELDSIZE):
            for j in range(self.FIELDSIZE):
                self.playfield[i][j] = tile()
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0

        self.setAcceptDrops(True)
        self.setMinimumSize(self.TILESIZE * self.FIELDSIZE, self.TILESIZE * self.FIELDSIZE)
        self.setMaximumSize(self.TILESIZE * self.FIELDSIZE, self.TILESIZE * self.FIELDSIZE)
        self.tile_Image = self.loadtileimg('tile.png')
        self.centraltile_Image = self.loadtileimg('centraltile.png')

    def zoom_in(self):
        if self.TILESIZE < 100:
            self.TILESIZE += 5
            self.setMinimumSize(self.TILESIZE * self.FIELDSIZE, self.TILESIZE * self.FIELDSIZE)
            self.setMaximumSize(self.TILESIZE * self.FIELDSIZE, self.TILESIZE * self.FIELDSIZE)
            self.update()

    def zoom_out(self):
        if self.TILESIZE > 30:
            self.TILESIZE -= 5
            self.setMinimumSize(self.TILESIZE * self.FIELDSIZE, self.TILESIZE * self.FIELDSIZE)
            self.setMaximumSize(self.TILESIZE * self.FIELDSIZE, self.TILESIZE * self.FIELDSIZE)
            self.update()

    def clear(self):
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.update()

    def loadtileimg(self, path=None):
        newImage = QPixmap()
        if not newImage.load(path):
            QMessageBox.warning(self, "Open Image",
                                "The image file could not be loaded.",
                                QMessageBox.Cancel)
            return

        return newImage

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect
        self.highlightedRect = QtCore.QRect()
        self.update(updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.united(self.targetSquare(event.pos()))

        rect = self.targetSquare(event.pos())

        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):

        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            pieceData = event.mimeData().data('image/x-puzzle-piece')
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)

            square = self.targetSquare(event.pos())
            print(square)
            pixmap = QPixmap()
            stream >> pixmap

            # self.hightlightedRect = QtCore.QRect()

            self.update(square)

            event.setDropAction(QtCore.Qt.MoveAction)

            if (self.playfield[square.x() // self.TILESIZE][square.y() // self.TILESIZE].getpixmap()) == None:
                self.playfield[square.x() // self.TILESIZE][square.y() // self.TILESIZE].setpixmap(pixmap)
                event.accept()
            else:
                event.ignore()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

    def findPiece(self, pieceRect):
        try:
            return self.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mousePressEvent(self, event):
        square = self.targetSquare(event.pos())
        found = self.findPiece(square)

        if found == -1:
            return

        pixmap = self.piecePixmaps[found]

        del self.piecePixmaps[found]
        del self.pieceRects[found]

        self.update(square)

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

        dataStream << pixmap

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-puzzle-piece', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)
        # if drag.start(QtCore.Qt.MoveAction) == 0:

        if drag.exec(QtCore.Qt.MoveAction) == 0:
            self.piecePixmaps.insert(found, pixmap)
            self.pieceRects.insert(found, square)
            self.update(self.targetSquare(event.pos()))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        r = QtCore.QRect(0, 0, self.FIELDSIZE * self.TILESIZE, self.FIELDSIZE * self.TILESIZE)
        painter.fillRect(r, QtCore.Qt.white)

        for x in range(self.FIELDSIZE):
            for y in range(self.FIELDSIZE):

                if self.playfield[x][y].card == None:
                    if x == 52 and y == 52:
                        painter.drawPixmap(x * self.TILESIZE, y * self.TILESIZE, self.TILESIZE, self.TILESIZE,
                                           self.centraltile_Image)
                    else:
                        painter.drawPixmap(x * self.TILESIZE, y * self.TILESIZE, self.TILESIZE, self.TILESIZE,
                                           self.tile_Image)
                else:
                    painter.drawPixmap(x * self.TILESIZE, y * self.TILESIZE, self.TILESIZE, self.TILESIZE,
                                       self.playfield[x][y].getpixmap())

        # for i, pieceRect in enumerate(self.pieceRects):
        #    painter.drawPixmap(pieceRect, self.piecePixmaps[i])

        painter.end()

    def targetSquare(self, position):
        return QtCore.QRect(position.x() // self.TILESIZE * self.TILESIZE,
                            position.y() // self.TILESIZE * self.TILESIZE, self.TILESIZE, self.TILESIZE)


class PiecesModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(PiecesModel, self).__init__(parent)
        self.pixmap_stack = []
        self.pixmaps = []

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DecorationRole:
            return QIcon(self.pixmaps[index.row()].scaled(
                60, 60, QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))

        if role == QtCore.Qt.UserRole:
            return self.pixmaps[index.row()]

        return None

    def addPiece(self, pixmap):
        if random.random() < 0.5:
            row = 0
        else:
            row = len(self.pixmaps)

        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.endInsertRows()

    def flags(self, index):
        if index.isValid():
            return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                    QtCore.Qt.ItemIsDragEnabled)

        return QtCore.Qt.ItemIsDropEnabled

    def removeRows(self, row, count, parent):
        if parent.isValid():
            return False

        if row >= len(self.pixmaps) or row + count <= 0:
            return False

        beginRow = max(0, row)
        endRow = min(row + count - 1, len(self.pixmaps) - 1)

        self.beginRemoveRows(parent, beginRow, endRow)

        del self.pixmaps[beginRow:endRow + 1]

        self.endRemoveRows()
        return True

    def mimeTypes(self):
        return ['image/x-puzzle-piece']

    def mimeData(self, indexes):
        mimeData = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()

        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                pixmap = QPixmap(self.data(index, QtCore.Qt.UserRole))
                stream << pixmap

        mimeData.setData('image/x-puzzle-piece', encodedData)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('image/x-puzzle-piece'):
            return False

        if action == QtCore.Qt.IgnoreAction:
            return True

        if column > 0:
            return False

        if not parent.isValid():
            if row < 0:
                endRow = len(self.pixmaps)
            else:
                endRow = min(row, len(self.pixmaps))
        else:
            endRow = parent.row()

        encodedData = data.data('image/x-puzzle-piece')
        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.ReadOnly)

        while not stream.atEnd():
            pixmap = QPixmap()
            stream >> pixmap

            self.beginInsertRows(QtCore.QModelIndex(), endRow, endRow)
            self.pixmaps.insert(endRow, pixmap)
            self.endInsertRows()

            endRow += 1

        return True

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.pixmaps)

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def setStack(self, pixmap):
        self.pixmap_stack = pixmap

    def addPieces(self):
        for y in range(len(self.pixmaps), 4):
            if len(self.pixmap_stack) != 0:
                img = self.pixmap_stack.pop(0)
                pieceImage = img.copy(0, 0, 500, 500)
                self.addPiece(pieceImage)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.puzzleImage = QPixmap()
        self.setGeometry(200, 200, 400, 400)

        self.setupMenus()
        self.setupWidgets()

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        self.setWindowTitle("Puzzle")

    def openImage(self, path=None):
        newImage = []
        z = ['411', '212', '312', '112', '342', '321', '234', '322', '333', '242', '222', '444']
        for i in range(12):
            newImg = QPixmap()
            newImg.load(str(z[i]) + '.png')
            newImage.append(newImg)
        self.puzzleImage = newImage
        self.showFullScreen()
        self.setupPuzzle()

    def setCompleted(self):
        QMessageBox.information(self, "Puzzle Completed",
                                "Congratulations! You have completed the puzzle!\nClick OK "
                                "to start again.",
                                QMessageBox.Ok)

        self.setupPuzzle()

    def setupPuzzle(self):
        self.model.setStack(self.puzzleImage)
        self.model.addPieces()
        self.puzzleWidget.clear()

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")


        exitAction = fileMenu.addAction("E&xit")
        exitAction.setShortcut("Ctrl+Q")

        gameMenu = self.menuBar().addMenu("&Game")

        restartAction = gameMenu.addAction("&Restart")

        exitAction.triggered.connect(qApp.quit)
        restartAction.triggered.connect(self.setupPuzzle)

    def setupWidgets(self):
        frame = QFrame()
        frameLayout = QGridLayout(frame)

        self.piecesList = QListView()
        self.piecesList.setDragEnabled(True)
        self.piecesList.setViewMode(QListView.IconMode)
        self.piecesList.setIconSize(QtCore.QSize(80, 80))
        self.piecesList.setGridSize(QtCore.QSize(90, 90))
        self.piecesList.setSpacing(10)
        self.piecesList.setMovement(QListView.Snap)
        self.piecesList.setAcceptDrops(True)
        self.piecesList.setDropIndicatorShown(True)

        self.model = PiecesModel(self)
        self.piecesList.setModel(self.model)
        self.piecesList.setMaximumWidth(100)
        self.puzzleWidget = PuzzleWidget(parent=self)

        self.puzzleWidget.puzzleCompleted.connect(self.setCompleted,
                                                  QtCore.Qt.QueuedConnection)
        self.scroll_area = QScrollArea()
        self.scroll_widget = self.puzzleWidget
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.puzzleWidget.TILESIZE *( self.puzzleWidget.FIELDSIZE - 10) / 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.puzzleWidget.TILESIZE * (self.puzzleWidget.FIELDSIZE - 5) / 2 )
        self.splitter = QSplitter()
        self.splitter.addWidget(self.piecesList)
        self.splitter.addWidget(self.scroll_area)
        self.rulesButton = QPushButton('Правила')
        self.playButton = QPushButton('Играть')
        self.zoom_inButton = QPushButton('zoom in')
        self.zoom_outButton = QPushButton('zoom out')
        self.end_turnButton = QPushButton('Закончить ход')
        self.rulesButton.clicked.connect(self.show_message)
        self.exitButton = QPushButton('Exit')
        splitter2 = QSplitter()
        splitter2.setOrientation(QtCore.Qt.Vertical)
        self.buttons = QFrame()
        buttonLayout = QHBoxLayout(self.buttons)
        buttonLayout.addWidget(self.rulesButton)
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.zoom_inButton)
        buttonLayout.addWidget(self.zoom_outButton)
        buttonLayout.addWidget(self.end_turnButton)
        buttonLayout.addWidget(self.exitButton)
        self.end_turnButton.hide()
        self.zoom_inButton.hide()
        self.zoom_outButton.hide()
        splitter2.addWidget(self.splitter)
        splitter2.addWidget(self.buttons)
        frameLayout.addWidget(splitter2)
        self.setCentralWidget(frame)
        self.splitter.hide()
        self.playButton.clicked.connect(self.startGame)
        self.zoom_inButton.clicked.connect(self.Zoom_in)
        self.zoom_outButton.clicked.connect(self.Zoom_out)
        self.end_turnButton.clicked.connect(self.endTurn)
        self.exitButton.clicked.connect(qApp.quit)

    def startGame(self):
        self.playButton.hide()
        self.rulesButton.hide()
        self.zoom_inButton.show()
        self.zoom_outButton.show()
        self.end_turnButton.show()
        self.splitter.show()

    def endTurn(self):
        self.model.addPieces()

    def Zoom_in(self):
        self.puzzleWidget.zoom_in()
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.puzzleWidget.TILESIZE * self.puzzleWidget.FIELDSIZE // 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.puzzleWidget.TILESIZE * self.puzzleWidget.FIELDSIZE // 2)
    def show_message(self):
        text = "Как играть? Игру начинает самый младший игрок, затем ход передаётся по часовой стрелке. В свой ход вы можете совершить одно из двух действий. 1. Выложить 1, 2, 3 или 4 карты в линию по правилам (смотрите Правила выкладывания линий  ниже). В конце своего хода подсчитайте и запишите победные очки, полученные вами за этот ход. Доберите карты в руку до четырёх. \n 2. Пропустить ход. Пропуская ход, вы можете положить любое количество карт из руки (от 1 до 4) под низ колоды и взять из неё соответствующее количество карт взамен. Менять таким образом карты не обязательно. \n Правила выкладывания линий Выкладывая карты в линию, вы должны соблюдать три условия: 1. Сторона. Каждая из выкладываемых карт должна хотя бы одной из сторон касаться уже лежащей на столе карты. 2. Линия. Вы можете выкладывать карты только в одну линию. То есть, вы можете: • создать/продолжить линию с одной стороны от ранее выложенной карты, • создать/продолжить линию с двух стороны от ранее выложенной карты (см. Ход 2). При этом у вас могут возникать и/или продолжаться и другие линии 3. Признаки. У карт в одной линии каждый из признаков (цвет, форма и число), рассмотренных по отдельности, должен быть или одинаковым для всех карт, или совсем разным для всех карт.  Карты в линии могут идти в любом порядке. Если между картами есть пустые  места, такие карты не считаются линией. В линии может быть не более 4 карт. Линия из 4 карт называется цепочкой. \n Подсчёт очков После каждого хода, подсчитайте  количество очков за каждую линию, созданную или продолженную вами в этот ход – для этого сложите числа, указанные на картах в линии. Если карта попадает в 2 линии, то и считать очки за нее нужно дважды. За каждую созданную цепочку (линию из 4 карт) удвойте все очки за этот ход. Удвойте очки снова, если в этот ход вы использовали все 4 карты из руки. Конец игры Игра завершается, когда заканчивается стопка карт и один из игроков выкладывает свою последнюю карту. Если вы выложили последнюю карту, удвойте количество очков за этот ход. Тот, кто набрал больше всего очков – выигрывает!"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Правила")
        msg.setInformativeText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def Zoom_out(self):
        self.puzzleWidget.zoom_out()
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.puzzleWidget.TILESIZE *( self.puzzleWidget.FIELDSIZE - 3) / 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.puzzleWidget.TILESIZE * (self.puzzleWidget.FIELDSIZE - 1) / 2 )


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.openImage()
    window.show()
    sys.exit(app.exec_())
