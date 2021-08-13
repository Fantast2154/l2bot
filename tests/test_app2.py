import atexit
import sys
import threading
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QFileInfo, QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import (QColor, QImage, QMatrix4x4, QOpenGLShader,
                         QOpenGLShaderProgram, QOpenGLTexture, QOpenGLVersionProfile,
                         QSurfaceFormat, QPolygon)
from PyQt5.QtWidgets import QApplication, QGridLayout, QOpenGLWidget, QWidget, QDialog
from PyQt5 import uic
#from game_gui_app import Ui_Dialog
from net import Client
import random


class Ui(QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        self.machine_id = random.randint(0, 100000000)
        uic.loadUi('game_gui_app_2.ui', self)
        self.main_click_button.clicked.connect(self.main_click)
        self.connect.clicked.connect(self.connect_to_server)
        self.client = None
        self.connected = False
        self.count = 0

        self.s = QtWidgets.QLabel(self)
        self.s.setText(str(self.count))
        self.s.move(100, 100)
        self.s.setFixedWidth(200)

        self.show()

    def connect_to_server(self):
        if not self.connected:
            self.client = Client(self.machine_id)
            self.connected = True
            self.connect.setEnabled(False)
            t = threading.Thread(target=self.foo)
            t.start()

    def foo(self):
        while self.client.connected:

            x = self.client.client_receive_message().copy()
            #print(x)
            if x:
                for id_, value in x.items():
                    if id_ != self.machine_id:
                        print('-1')
                        self.count -= 1
                        self.s.setText(str(self.count))
                    else:
                        print('+1')
                        self.count += 1
                        self.s.setText(str(self.count))

    def main_click(self):
        self.client.client_send('))))')


def exit_handler(w):
    w.client.server.send(b'exit')
    w.client.server.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()

    app.exec_()

    # atexit.register(exit_handler)
