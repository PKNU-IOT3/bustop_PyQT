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
    saveBattery=False
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui',self)
        self.setWindowIcon(QIcon('bustopimage.png'))
        self.setWindowTitle('BuSTOP v2')
        self.UI초기화()
        self.InitSignal()
        self.BtnHideClicked()
    
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
    
    def InitSignal(self):
        # 버튼 시그널
        self.BtnAddCnt.clicked.connect(self.BtnAddCntClicked)
        self.BtnMinusCnt.clicked.connect(self.BtnMinusCntClicked)
        self.BusInfor.cellClicked.connect(self.CellPosition)
        self.BtnSearch.clicked.connect(self.BtnSearchClicked)
        self.BtnHide.clicked.connect(self.BtnHideClicked)
        self.BtnInfo.clicked.connect(self.BtnInfoClicked)
        self.BtnHelp.clicked.connect(self.BtnHelpClicked)
        self.BtnClearNote.clicked.connect(self.BtnClearNoteClicked)
        self.BtnDeviceOnOff.clicked.connect(self.BtnDeviceOnOffClicked)
    
    # 셀 클릭 위치 확인 
    def CellPosition(self):
        qtApp.isClicked=True
        row=self.BusInfor.currentRow()
        mybus_num=self.BusInfor.item(row,1).text()
        self.LblNotification.setText(f'{mybus_num} 버스 선택')
        self.LblNotification.setFont(QFont('Rockwell',14))
        self.LblNotification.setStyleSheet("color: green;")

    # 탑승 대기 버튼 클릭
    def BtnAddCntClicked(self):
        #if self.BusInfor.currentRow()<0:
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
                host="localhost",
                user="root",
                password="12345",
                database="bus"            
                )
            try:
                cursor=self.mydb.cursor()
                cursor.execute(f"UPDATE bus_table SET bus_cnt = bus_cnt+1 WHERE bus_num = '{mybus_num.replace('번', '')}'")
                self.mydb.commit()
                self.updateTable(row)
                self.LblNotification.setText(f"{mybus_num} 버스 탑승 대기 완료!")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: green;")
                qtApp.isClicked=False
                return
            except mysql.connector.Error as error:
                print("MySQL 서버 접속 에러 : {}".format(error))
            finally:
                self.mydb.close()

    # 탑승 취소 버튼 클릭
    def BtnMinusCntClicked(self):
        #if self.BusInfor.currentRow()<0:
        if qtApp.isClicked==False:            
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
            if mybus_cnt.text()=='0명':
                self.LblNotification.setText("탑승 대기 인원이 0명이기에 취소 불가능합니다.")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: orange;")
                return
            else:
                self.mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="bus")
                # 탑승 취소 버튼 클릭 시 cnt-1
                try:
                    cursor=self.mydb.cursor()
                    cursor.execute(f"UPDATE bus_table SET bus_cnt = bus_cnt-1 WHERE bus_num = '{mybus_num.replace('번', '')}'")
                    self.mydb.commit()
                    self.updateTable(row)
                    self.LblNotification.setText(f"{mybus_num} 버스 탑승 취소 완료!")
                    font=QFont('Rockwell',14)
                    font.setBold(True)
                    self.LblNotification.setFont(font)
                    self.LblNotification.setStyleSheet("color: green;")
                    qtApp.isClicked=False
                    return
                except mysql.connector.Error as error:
                    print("MySQL 서버 접속 에러 : {}".format(error))
                finally:
                    self.mydb.close()

    #변경된 DB 내용을 QTableWidget인 BusInfor에 뿌려줌
    def updateTable(self,row):
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bus"
        )
        try:
            # SQL 쿼리 실행
            cursor=mydb.cursor()
            # QtableWidget의 행은 0번부터 시작인데 우리 DB 는 bus_idx가 1부터 시작하기에 row+1 필요함
            cursor.execute(f"SELECT * FROM bus_table WHERE bus_idx = {row+1}") 
            result = cursor.fetchone()
            #셀에 데이터를 추가
            for i,value in enumerate(result):
                cell = QTableWidgetItem(str(value))
                self.BusInfor.setItem(row,i,cell)
        except mysql.connector.Error as error:
            print("MySQL 서버 접속 에러 : {}".format(error))
        finally:
            mydb.close()

    ### 좌측 버튼 함수 ###
    def BtnSearchClicked(self):
        self.UI초기화()
        self.LblInfor.setText('우측 패널에\n 버스 정보가\n 출력 되었습니다!')

    def BtnHideClicked(self):
        self.BusInfor.setRowCount(0)
        self.LblInfor.setText('버스 도착 정보를\n 확인하시려면 \n좌측 정보 출력 버튼을 \n클릭해주세요!')

    def BtnInfoClicked(self):
        self.LblInfor.setText("<BuSTOP!>은\n실시간으로\n 버스 정보를\n제공함으로써\n 승객들은 탑승 예약을\n"+
                            "버스 기사님들은\n 승객이 탑승하는\n정류장에만 정차해\n"+
                            "효율적인 운행을\n할 수 있습니다.\n\n"+
                            "<BuSTOP!>은\n 버스 정류장에\n터치패드를 설치하여\n 앱 사용이 "+
                            "불편하거나\n 휴대폰이 없는\n사람들 모두\n이용할 수 있습니다.\n\n"+
                            "<BuSTOP!> 시스템은\n누구나 쉽게\n간단한 UI 조작을 통해\n탑승 정보를\n"+
                            "기사님에게 알려\n정류장에서의\n불필요한 정차를 줄여\n보다 효율적인\n대중교통 시스템을\n"+
                            "구축하는데\n도움이 됩니다.")

    def BtnHelpClicked(self):
        self.LblInfor.setText('관리자\n전화번호\n010-8515-0728\n번으로 연락\n부탁드립니다!')

    def BtnClearNoteClicked(self):
        self.LblNotification.setText("")

    def BtnDeviceOnOffClicked(self):
        if qtApp.saveBattery: # 장치가 켜진 상태일때
            self.LblLeftPanel.setStyleSheet("color: white;")
            self.LblRightPanel.setStyleSheet("color: white;")
            self.LblBottomPanel.setStyleSheet("color: white;")
            self.LblStatusBar.setStyleSheet("color: white;")
            self.LblTopPanel.setStyleSheet("color: white;")
            self.BtnSearch.setStyleSheet("color: white;")
            self.BtnHide.setStyleSheet("color: white;")
            self.BtnInfo.setStyleSheet("color: white;")
            self.BtnHelp.setStyleSheet("color: white;")
            self.BtnAddCnt.setStyleSheet("color: white;")
            self.BtnMinusCnt.setStyleSheet("color: white;")
            header_style="QHeaderView::section {background-color: %s; text-align: center;}" %QColor(0,0,0).name()
            self.BusInfor.horizontalHeader().setStyleSheet(header_style)
            qtApp.saveBattery = False
        else: # 장치가 꺼진 상태일 때
            self.BusInfor.setRowCount(0)
            self.LblNotification.setText("")
            self.LblInfor.setText("")
            self.LblLeftPanel.setStyleSheet("color: #16191d;")
            self.LblRightPanel.setStyleSheet("color: #16191d;")
            self.LblBottomPanel.setStyleSheet("color: #16191d;")
            self.LblStatusBar.setStyleSheet("color: #2c313c;")
            self.LblTopPanel.setStyleSheet("color: #2c313c;")
            self.BtnSearch.setStyleSheet("color: #16191d;")
            self.BtnHide.setStyleSheet("color: #16191d;")
            self.BtnInfo.setStyleSheet("color: #16191d;")
            self.BtnHelp.setStyleSheet("color: #16191d;")
            self.BtnAddCnt.setStyleSheet("color: #2c313c;")
            self.BtnMinusCnt.setStyleSheet("color: #2c313c;")
            header_style="QHeaderView::section {background-color: %s; text-align: center;}" %QColor(255,255,255).name()
            self.BusInfor.horizontalHeader().setStyleSheet(header_style)
            qtApp.saveBattery = True

if __name__ == '__main__':
    app=QApplication(sys.argv)    
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())