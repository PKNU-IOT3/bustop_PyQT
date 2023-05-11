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
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
class IconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._icon_visible = True

    def setIconVisible(self, visible):
        self._icon_visible = visible
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._icon_visible:
            self.setIcon(QtGui.QIcon())

class qtApp(QMainWindow):
    isClicked=False # 행 선택 확인 bool 변수
    saveBattery=False # 좌측 상단 Device ON/OFF 상태 변수
    timer=QTimer() # DB 내용 변경 시 실시간 반영을 위해 사용할 timer
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui',self) # ui 로드
        self.setWindowIcon(QIcon('images/bustopimage.png'))
        self.setWindowTitle('BuSTOP v2')
        self.initUI() #initUI 메소드 호출하여 실행 직후의 statusBar 출력 및 DB 연결
        self.InitSignal() #버튼 시그널 연결 <- 해당 소스 분리 하지 않고 버튼 시그널을 __init__ 내부에 작성 시 시그널이 중복 호출되어 연결된 슬롯 함수가 2번씩 실행
        self.BtnHideClicked() # 사용자가 정보 출력 버튼 누를 때 까지 버스 정보 화면을 숨겨놓기 위함

        ## 초기 LblInfor Font 설정
        font=QFont('Rockwell',12)
        font.setBold(True)
        self.LblInfor.setFont(font)
        self.LblInfor.setStyleSheet("color: DarkSeaGreen;")
    
    # 상태바에 시간 출력 및 db 연결, QTableWidget인 BusInfor에 DB 정보 연결
    def initUI(self):
        self.date = QDate.currentDate()
        self.datetime = QDateTime.currentDateTime()

        self.statusBar().showMessage(self.datetime.toString(Qt.DefaultLocaleLongDate))

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

        for row,data in enumerate(myresult):
            for column,item in enumerate(data):
                # 데이터를 QTableWidgetItem으로 변환하여 테이블 위젯에 추가
                cell=QTableWidgetItem(str(item))
                # 가독성을 위해 ~ 번 / ~ 명 / ~ 분의 형태로 정보를 출력하기 위함
                if column==1:
                    cell.setText(str(item)+"번")
                    cell.setFont(QFont('Rockwell',14))
                if column==2:
                    cell.setText(str(item)+"명")
                    cell.setFont(QFont('Rockwell',14))
                if column==3:
                    cell.setText(str(item)+"분")
                    cell.setFont(QFont('Rockwell',14))
                if column==4:
                    cell.setText(str(item)+"명")
                    cell.setFont(QFont('Rockwell',14))
                self.BusInfor.setItem(row,column,cell)
                cell.setTextAlignment(QtCore.Qt.AlignCenter)
                cell.setFont(QFont('Rockwell',14))
    
    # 버튼 시그널을 따로 함수로 구현하지 않고 UI 초기화에 넣으면 버튼에 연결된 슬롯함수가 두번씩 호출
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
        qtApp.isClicked=True # 셀이 클릭 된경우 선언해둔 bool형 변수 isClicked를 True로 변경
        row=self.BusInfor.currentRow()
        mybus_num=self.BusInfor.item(row,1).text() # ex) 100-1
        mybus_cnt=self.BusInfor.item(row,2).text()
        mybus_cnt_1=self.BusInfor.item(row,2).text().replace('명','')
        mybus_nowin=self.BusInfor.item(row,4).text().replace('명','')
        mybus_total=int(mybus_cnt_1)+int(mybus_nowin)

        self.LblNotification.setText(f'{mybus_num} 버스 선택')
        self.LblNotification.setFont(QFont('Rockwell',14))
        self.LblNotification.setStyleSheet("color: green;")
        if(mybus_cnt=='0명'):
            self.BtnMinusCnt.setEnabled(False)
            self.BtnMinusCnt.setStyleSheet("color : #2c313c;")
            self.BtnMinusCnt.setVisible(False)
        else:
            self.BtnMinusCnt.setEnabled(True)
            self.BtnMinusCnt.setStyleSheet("color : white;")
            self.BtnMinusCnt.setVisible(True)

        if(mybus_total>=50):
            self.BtnAddCnt.setEnabled(False)
            self.BtnAddCnt.setStyleSheet("color : #2c313c;")
            self.BtnAddCnt.setVisible(False)
        else:
            self.BtnAddCnt.setEnabled(True)
            self.BtnAddCnt.setStyleSheet("color : white;")
            self.BtnAddCnt.setVisible(True)

    # 탑승 대기 버튼 클릭
    def BtnAddCntClicked(self):
        #if self.BusInfor.currentRow()<0:
        if(qtApp.isClicked==False): # CellPosition 함수가 호출되지 않은 경우 즉 셀 선택이 안된 경우
            self.LblNotification.setText("버튼 사용은 버스 선택 이후 가능합니다!")
            font=QFont('Rockwell',14)
            font.setBold(True)
            self.LblNotification.setFont(font)
            self.LblNotification.setStyleSheet("color: orange;")
            return
        else:
            row=self.BusInfor.currentRow()
            mybus_num=self.BusInfor.item(row,1).text()
            mybus_cnt=self.BusInfor.item(row,2).text().replace('명','')
            mybus_nowin=self.BusInfor.item(row,4).text().replace('명','')
            
            mybus_total=int(mybus_cnt)+int(mybus_nowin)
            if(mybus_total>=50): # 버스 최대 탑승 인원 50명으로 제한
                self.LblNotification.setText("탑승 대기 인원 초과이기에 대기 불가능합니다.")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: orange;")
                return

            self.mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="bus"            
                )
            try:
                cursor=self.mydb.cursor()
                cursor.execute(f"UPDATE bus_table SET bus_cnt = bus_cnt+1 WHERE bus_num = '{mybus_num.replace('번', '')}'") # 탑승 대기 버튼 클릭 시 DB의 bus_cnt 를 1 증가
                self.mydb.commit()
                self.updateTable(row)
                self.LblNotification.setText(f"{mybus_num} 버스 탑승 대기 완료!")
                font=QFont('Rockwell',14)
                font.setBold(True)
                self.LblNotification.setFont(font)
                self.LblNotification.setStyleSheet("color: green;")
                qtApp.isClicked=False # 선택된 버스 탑승 대기 / 탑승 취소 후 셀 선택 해제를 의미함
                self.BusInfor.clearSelection() # 선택된 셀 해제
                return
            except mysql.connector.Error as error:
                print("MySQL 서버 접속 에러 : {}".format(error))
            finally:
                self.mydb.close()

    # 탑승 취소 버튼 클릭
    def BtnMinusCntClicked(self):
        if qtApp.isClicked==False:  # CellPosition 함수가 호출되지 않은 경우 즉 셀 선택이 안된 경우          
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
                self.BusInfor.clearSelection()
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
                    qtApp.isClicked=False # 선택된 버스 탑승 대기 / 탑승 취소 후 셀 선택 해제를 의미함
                    self.BusInfor.clearSelection() # 선택된 셀 해제
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
                # 사용자의 가독성을 위함
                if i==1:
                    cell.setText(str(value)+"번")
                    cell.setFont(QFont('Rockwell',14))
                if i==2:
                    cell.setText(str(value)+"명")
                    cell.setFont(QFont('Rockwell',14))
                if i==3:
                    cell.setText(str(value)+"분")
                    cell.setFont(QFont('Rockwell',14))
                self.BusInfor.setItem(row,i,cell)
                cell.setTextAlignment(QtCore.Qt.AlignCenter)
                cell.setFont(QFont('Rockwell',14))
        except mysql.connector.Error as error:
            print("MySQL 서버 접속 에러 : {}".format(error))
        finally:
            mydb.close()

    ### 좌측 버튼 함수 / 우측 최소,최대화 ###
    # 정보 출력 버튼 클릭 시 해당 함수 실행
    def BtnSearchClicked(self):
        self.initUI()
        self.LblInfor.setText('우측 패널에\n 버스 정보가\n 출력 되었습니다!')
        self.timer.timeout.connect(self.initUI) #self.timer.timeout 즉 timer 객체가 종료되면 initUI와 연결시킴 
        self.timer.start(1)#정보 출력 시 계속해서 timer가 돌아야하기 때문에 timer.start(1)

    # 정보 숨기기 버튼 클릭 시 해당 함수 실행
    def BtnHideClicked(self):
        self.BusInfor.setRowCount(0) # BusInfor을 비움
        self.LblInfor.setText('버스 도착 정보를\n 확인하시려면 \n좌측 정보 출력 버튼을 \n클릭해주세요!')
        self.timer.stop() #timer 중지 -> 정보 출력 버튼 클릭 시 timer 다시 돌아가도록 구성

    # LblInfor 라벨에 프로그램 설명을 출력해주는 함수
    def BtnInfoClicked(self):
        self.LblInfor.setText("<BuSTOP!>은\n실시간으로\n 버스 정보를\n제공함으로써\n 승객들은 탑승 예약을\n"+
                            "버스 기사님들은\n 승객이 탑승하는\n정류장에만 정차해\n"+
                            "효율적인 운행을\n할 수 있습니다.\n\n"+
                            "<BuSTOP!>은\n 버스 정류장에\n터치패드를 설치하여\n 앱 사용이 "+
                            "불편하거나\n 휴대폰이 없는\n사람들 모두\n이용할 수 있습니다.\n\n"+
                            "<BuSTOP!> 시스템은\n누구나 쉽게\n간단한 UI 조작을 통해\n탑승 정보를\n"+
                            "기사님에게 알려\n정류장에서의\n불필요한 정차를 줄여\n보다 효율적인\n대중교통 시스템을\n"+
                            "구축하는데\n도움이 됩니다.")
        font=QFont('Rockwell',12)
        font.setBold(True)
        self.LblInfor.setFont(font)
        self.LblInfor.setStyleSheet("color: DarkSeaGreen;")

    # 도움말 버튼
    def BtnHelpClicked(self):
        self.LblInfor.setText('관리자\n전화번호\n\n010-8515-0728')
        
    # 우측 하단 (x) 버튼
    def BtnClearNoteClicked(self):
        self.LblNotification.setText("")
        self.LblInfor.setText("")

    # 장치 ON/OFF
    def BtnDeviceOnOffClicked(self):
        if qtApp.saveBattery: # 장치가 켜진 상태일때
            self.LblLeftPanel.setStyleSheet("color: white;")
            self.LblRightPanel.setStyleSheet("color: white;")
            self.LblBottomPanel.setStyleSheet("color: white;")
            self.LblStatusBar.setStyleSheet("color: white;")
            self.LblTopPanel.setStyleSheet("color: white;")
            self.BtnSearch.setStyleSheet("color: white;")
            self.BtnSearch.setVisible(True)
            self.BtnHide.setStyleSheet("color: white;")
            self.BtnHide.setVisible(True)
            self.BtnInfo.setStyleSheet("color: white;")
            self.BtnInfo.setVisible(True)
            self.BtnHelp.setStyleSheet("color: white;")
            self.BtnHelp.setVisible(True)
            self.BtnAddCnt.setStyleSheet("color: white;")
            self.BtnAddCnt.setVisible(True)
            self.BtnMinusCnt.setStyleSheet("color: white;")
            self.BtnMinusCnt.setVisible(True)
            self.BtnClearNote.setVisible(True)
            header_style="QHeaderView::section {background-color: %s; text-align: center;}" %QColor(0,0,0).name()
            self.BusInfor.horizontalHeader().setStyleSheet(header_style)
            qtApp.saveBattery = False
            #self.timer.start(1) # 장치가 켜지면서 timer 실행
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
            self.BtnSearch.setVisible(False)
            self.BtnHide.setStyleSheet("color: #16191d;")
            self.BtnHide.setVisible(False)
            self.BtnInfo.setStyleSheet("color: #16191d;")
            self.BtnInfo.setVisible(False)
            self.BtnHelp.setStyleSheet("color: #16191d;")
            self.BtnHelp.setVisible(False)
            self.BtnAddCnt.setStyleSheet("color: #2c313c;")
            self.BtnAddCnt.setVisible(False)
            self.BtnMinusCnt.setStyleSheet("color: #2c313c;")
            self.BtnMinusCnt.setVisible(False)
            self.BtnClearNote.setVisible(False)
            header_style="QHeaderView::section {background-color: %s; text-align: center;}" %QColor(255,255,255).name()
            self.BusInfor.horizontalHeader().setStyleSheet(header_style)
            qtApp.saveBattery = True
            qtApp.isClicked==False
            self.timer.stop() # 장치가 꺼지면 timer 중지
    
if __name__ == '__main__':
    app=QApplication(sys.argv)    
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())