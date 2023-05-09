import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
import mysql.connector
import pymysql
import resources_rc

class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui',self)
        self.setWindowIcon(QIcon('bustopimage.png'))
        self.setWindowTitle('BuSTOP v2')
        self.UI초기화()
    
    def UI초기화(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bus"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM bus_table")
        myresult=mycursor.fetchall()

        self.BusInfor.setRowCount(len(myresult))
        header_style="QHeaderView::section {background-color: %s; text-align: center;}" %QColor(0,0,0).name()
        self.BusInfor.horizontalHeader().setStyleSheet(header_style)
        item_style="QTableWidget::item {text-align: center;}"
        self.BusInfor.setStyleSheet(item_style)
        #self.BusInfor.header = ['버스 등록 번호', '버스 번호', '탑승 대기 인원', '배차 간격']


        for row,data in enumerate(myresult):
            for column,item in enumerate(data):
                # 데이터를 QTableWidgetItem으로 변환하여 테이블 위젯에 추가
                cell=QTableWidgetItem(str(item))
                if column==1:
                    cell.setText(str(item)+"번")
                    cell.setFont(QFont('Rockwell',14))
                if column==2:
                    cell.setText(str(item)+"명")
                    cell.setFont(QFont('Rockwell',14))
                self.BusInfor.setItem(row,column,cell)
                cell.setTextAlignment(QtCore.Qt.AlignCenter)
                cell.setFont(QFont('Rockwell',14))


if __name__ == '__main__':
    app=QApplication(sys.argv)    
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())