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
    # 행 선택 확인 bool 변수
    isClicked=False
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui',self)
        self.setWindowIcon(QIcon('bustopimage.png'))
        self.setWindowTitle('BuSTOP v2')
        self.UI초기화()
    
    def UI초기화(self):
        mydb = mysql.connector.connect(
            host="210.119.12.69",
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

        # 버튼 시그널
        self.BtnAddCnt.clicked.connect(self.BtnAddCntClicked)
        self.BtnMinusCnt.clicked.connect(self.BtnMinusCntClicked)
        self.BusInfor.cellClicked.connect(self.CellPosition)

    # 탑승 대기 버튼 클릭
    def BtnAddCntClicked(self):
        if(qtApp.isClicked==False):
            self.LblNotification.setText("버튼 사용은 버스 선택 이후 가능합니다!")
            font=QFont('Rockwell',14)
            font.setBold(True)
            self.LblNotification.setFont(font)
            self.LblNotification.setStyleSheet("color: orange;")
            return
        else:
            row=self.BusInfor.currentRow()
            mybus_num=self.BusInfor.item(row,1).text()
            self.mydb=mysql.connector.connect(
            host="210.119.12.69",
            user="root",
            password="12345",
            database="bus"            
            )
            try:
                cursor=self.mydb.cursor()
                cursor.execute(f"UPDATE bus_table SET bus_cnt = bus_cnt+1 WHERE bus_num = '{mybus_num}'")
                self.mydb.commit()
                self.updateTable(row)
                self.LblNotification.setText(f"{mybus_num} 버스 탑승 대기 완료!")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: green;")
                qtApp.isClicked=False
            except mysql.connector.Error as error:
                print("MySQL 서버 접속 에러 : {}".format(error))
            finally:
                self.mydb.close()

    # 탑승 취소 버튼 클릭
    def BtnMinusCntClicked(self):
        if(qtApp.isClicked==False):
            self.LblNotification.setText("버튼 사용은 버스 선택 이후 가능합니다!")
            font=QFont('Rockwell',14)
            font.setBold(True)
            self.LblNotification.setFont(font)
            self.LblNotification.setStyleSheet("color: orange;")
            return
        else:
            row=self.BusInfor.currentRow()
            mybus_num=self.BusInfor.item(row,1).text()
            mybus_cnt=self.BusInfor.item(row,2)
            if(mybus_cnt.text()=='0'):
                self.LblNotification.setText("탑승 대기 인원이 0명이기에 취소 불가능합니다.")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: orange;")
                return
            else:
                self.mydb=mysql.connector.connect(
                host="210.119.12.69",
                user="root",
                password="12345",
                database="bus"
            )
            # 탑승 취소 버튼 클릭 시 cnt-1
            try:
                cursor=self.mydb.cursor()
                cursor.execute(f"UPDATE bus_table SET bus_cnt = bus_cnt-1 WHERE bus_num = '{mybus_num}'")
                self.mydb.commit()
                self.updateTable(row)
                self.LblNotification.setText(f"{mybus_num} 버스 탑승 대기 완료!")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: green;")
                qtApp.isClicked=False
            except mysql.connector.Error as error:
                print("MySQL 서버 접속 에러 : {}".format(error))
            finally:
                self.mydb.close()

    # 셀 클릭 유무 / 위치 확인 
    def CellPosition(self):
        qtApp.isClicked=True
        row=self.BusInfor.currentRow()
        mybus_num=self.BusInfor.item(row,1).text()
        self.LblNotification.setText(f'{mybus_num} 버스 선택')
        self.LblNotification.setFont(QFont('Rockwell',14))
    
    #변경된 DB 내용을 QTableWidget인 BusInfor에 뿌려줌
    def updateTable(self,row):
        mydb=mysql.connector.connect(
            host="210.119.12.69",
            user="root",
            password="12345",
            database="bus"
        )
        try:
            # SQL 쿼리 실행
            cursor=mydb.cursor()
            # QtableWidget의 행은 0번부터 시작인데 우리 DB 는 bus_idx가 1부터 시작하기에 row+1 필요함
            cursor.execute(f"SELECT * FROM bus_table WHERE bus_idx = {row+1}") 
            data = cursor.fetchone()
            #셀에 데이터를 추가
            for column,item in enumerate(data):
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
        except mysql.connector.Error as error:
            print("MySQL 서버 접속 에러 : {}".format(error))
        finally:
            mydb.close()


if __name__ == '__main__':
    app=QApplication(sys.argv)    
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())