import cv2
import imutils
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
        while True:
            ret, frame = cap.read()
            if ret:
                #global stop_threads
                #if cv2.waitKey(5) & stop_threads:
                #    break

                # https://stackoverflow.com/a/55468544/6622587
                #frame = imutils.resize(frame, width=320)
                image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                #image = cv2.resize(image, (320, 240))
                h, w, ch = image.shape
                #### image processing ####

                result = image.copy()
                src = image.copy()
                result[0:h, 0:w//2] = image[0:h, 0:w//2]
                result[0:h, w//2:w] = cv2.flip(image[0:h, 0:w//2], 1)

                #### processing ended ####
                bytesPerLine = ch * w
                convertToQtFormat = QImage(result.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(480, 360, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class App(QWidget): # old QWidget
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 0
        self.top = 0
        self.width = 480
        self.height = 360
        self.localPos = None
        self.xy = None
        self.th = None
        self.initUI()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.localPos = a0.localPos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        self.xy = [(a0.globalX() - self.localPos.x()), (a0.globalY() - self.localPos.y())]
        self.move(*map(int, self.xy))

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)

        #text = QtWidgets.QAction("Context Menu 1")
        #menu.addAction(text)

        quit_icon = QtGui.QIcon(self.style().standardIcon(self.style().SP_MessageBoxCritical))
        quit_action = QtWidgets.QAction(quit_icon, "종료", self)
        #quit_action.triggered.connect(QtWidgets.qApp.quit)
        menu.addAction(quit_action)

        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quit_action:
            QtWidgets.qApp.quit()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        #self.resize(1800, 1200)
        self.resize(self.width, self.height)

        # create a label
        self.label = QLabel(self)
        #self.label.move(280, 120)
        self.label.resize(self.width, self.height)

        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
