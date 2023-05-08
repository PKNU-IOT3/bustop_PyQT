import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql
import resources_rc

class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui',self)
        self.setWindowIcon(QIcon('bustopimage.png'))
        self.setWindowTitle('BuSTOP v2')


if __name__ == '__main__':
    app=QApplication(sys.argv)    
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())