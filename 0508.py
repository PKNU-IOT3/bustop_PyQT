from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, \
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import sys
import mysql.connector
import pyautogui
class 표위젯(QWidget):
    # 행 선택 확인 bool 변수
    isClicked=False
    def __init__(self):
        super().__init__()
        self.UI초기화()
        self.setWindowIcon(QIcon('bustopimage.png'))

    def UI초기화(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        header = ['버스 등록 번호', '버스 번호', '탑승 대기 인원', '배차 간격']
        self.table.setHorizontalHeaderLabels(header)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bus"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM bus_table")
        myresult=mycursor.fetchall()

        self.table.setRowCount(len(myresult))
        self.table.setColumnCount(len(myresult[0]))

        for row,data in enumerate(myresult):
            for column,item in enumerate(data):
                # 데이터를 QTableWidgetItem으로 변환하여 테이블 위젯에 추가
                cell=QTableWidgetItem(str(item))
                self.table.setItem(row,column,cell)

        #탑승 대기 버튼 생성
        busPlus = QPushButton(self)
        busPlus.setText('탑승대기')
        busPlus.setEnabled(True)
        busPlus.move(450, 30)
        busPlus.clicked.connect(self.btnbusplus) # 버튼과 함수 연결
        #탑승 대기 취소 생성
        busMinus = QPushButton(self)
        busMinus.setText('탑승취소')
        busMinus.setEnabled(True)
        busMinus.move(550, 30)
        busMinus.clicked.connect(self.btnbusminus) # 버튼과 함수 연결

        
        self.table.cellClicked.connect(self.showCellPosition)

        self.label = QLabel()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addWidget(self.label, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

        self.setWindowTitle('Bustop')
        self.setGeometry(300, 300, 720, 500)
        self.show()

    def showCellPosition(self):
        표위젯.isClicked=True
        row = self.table.currentRow()
        mybus_num=self.table.item(row,1).text()
        self.label.setText(f'{mybus_num} 버스 선택')
    # 탑승 대기 버튼 클릭 시 발생 함수
    def btnbusplus(self):
        if(표위젯.isClicked==False):
            pyautogui.alert("버스 선택 후 버튼 사용 가능","경고")
            return
        else:
            row = self.table.currentRow()
            mybus_num=self.table.item(row,1).text()

            self.mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="bus"            
                )
                # 탑승 대기 버튼 클릭 시 bus_cnt +1 시키는 부분
            try:
                cursor=self.mydb.cursor()
                cursor.execute(f"UPDATE bus_table SET bus_cnt = bus_cnt+1 WHERE bus_num = '{mybus_num}'")
                self.mydb.commit()

                self.updateTable(row)
                pyautogui.alert(f"{mybus_num} 버스 탑승 대기 완료!","탑승대기")
                표위젯.isClicked=False
            except mysql.connector.Error as error:
                print("MySQL 서버 접속 에러 : {}".format(error))
            finally:
                self.mydb.close()

    # 탑승 취소 버튼 클릭 시 발생 함수
    def btnbusminus(self):
        if(표위젯.isClicked==False):
            pyautogui.alert("버스 선택 후 버튼 사용 가능","경고")
            return
        else:
            row = self.table.currentRow()
            mybus_num=self.table.item(row,1).text()
            mybus_cnt=self.table.item(row,2)
            if(mybus_cnt.text()=='0'):
                pyautogui.alert("탑승 대기 인원이 0명입니다. 취소 불가능!","취소 불가")
                return
            else:
                self.mydb=mysql.connector.connect(
                host="localhost",
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
                pyautogui.alert(f"{mybus_num} 버스 탑승 취소 완료!","탑승취소")
                표위젯.isClicked=False
            except mysql.connector.Error as error:
                print("MySQL 서버 접속 에러 : {}".format(error))
            finally:
                self.mydb.close()

    # 변경된 DB 내용을 QTableWidget에 뿌려주는 update 함수 
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
                self.table.setItem(row,i,cell)
        except mysql.connector.Error as error:
            print("MySQL 서버 접속 에러 : {}".format(error))
        finally:
            mydb.close()

프로그램무한반복 = QApplication(sys.argv)
실행인스턴스 = 표위젯()
프로그램무한반복.exec_()