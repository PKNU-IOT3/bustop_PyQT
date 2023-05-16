# PyQT를 활용한 버스 탑승 APP
2023.03.15 제작 

## 개발목적
- 특정 버스의 탑승 대기인원을 사전에 알려 버스 정류장에서의 멈춤 유무를 사전에 전달하기 위함

## 기술스택
- Python 3.11.2
- PyQt5
    - pymysql 모듈 사용
- Qt Designer
- MySQL

1. Qt Designer을 활용한 ui 제작
![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/QtDesigner.png)
2. MySQL DB 작성
![MySQL](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/mysql.png)
3. Python으로 기능 작성
![실행화면1](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_1.png)
![실행화면2](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_2.png)

### 로직
- 버스의 탑승대기/탑승취소 버튼을 통해 해당 버스 탑승 인원 카운팅
- 카운팅된 인원을 DB로 저장
- DB에서 변경되는 탑승인원(bus_cnt)의 내용도 앱으로 실시간 반영

## 23.03.16 프로젝트 수정
- RadioButton을 사용하여 탑승 대기 / 탑승 취소 버튼을 각각 3개에서 1개로 축소
- UI 수정
![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/QtDesigner_modify.png)
![실행화면](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_modify.png)


## 23.03.17 프로젝트 수정
- Qt Designer을 이용한 UI 수정
    ### - Grid를 이용하여 MainWindow 최대화/최소화에 따른 BUTTON 크기 조정
    ### - UI 수정
    ![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/QtDesigner_0317_1.png)
    ![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/QtDesigner_0317_2.png)

- 프로그램 로직 변경
    ### - RadioButton 클릭 -> Button클릭 / 탑승 할 버스 클릭시에 Button 색상 변경
    ![실행화면1](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_1.png)
    ![실행화면3](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_3.png)
    ### - 탑승 할 버스 중복 선택 불가
    ### - resize 이벤트를 이용하여 최대화 / 최소화 시 모든 UI 크기 자동 변경
    
    ### - 탑승 할 버스 미선택 시 탑승대기 / 탑승 취소 버튼 비활성화
    ![실행화면1](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_1.png)
    ### - 탑승 할 버스의 탑승인원이 0명인 경우 탑승취소 버튼 비활성화
    ![실행화면4](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_4.png)
    ### - DB에서 버스 탑승인원 변경 시 앱에서 실시간 반영
    ![실행화면5](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_5.png)

## 23.03.20 프로젝트 수정
- 라즈베리파이 터치스크린과 연동
    ### - 터치 스크린 세로모드에 맞춰 리사이징시 label size 변경
    ### - 라즈베리파이 스크린 터치 시 기능 정상작동 및 DB와 실시간 연동 확인
    <img src="https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4%EC%97%B0%EB%8F%99_0320.jpg" width="400" height="800" />

# PyQt를 활용한 버스 탑승 App - UI 및 로직 대규모 수정
### 23.05.11 수정
## Qt Designer을 활용한 UI 변경
- #### interfaceUI_Design
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/interfaceUI_Design.png)
- #### interfaceUI_Element
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/interfaceUI_element.png)
## MySQL DataBase 구성 변경
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/MySQL_modify.png)
## App 작동 화면
- ### 프로그램 시작화면(Main 화면)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/begin.png)
- ### 정보 출력(DB에 등록되어 있는 Bus 정보를 출력)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/print.png)
- ### 정보 숨기기(QTableWidget에 출력한 버스 정보 Hide)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/hide.png)
- ### BuSTOP이란? (프로그램에 대한 정보 제공)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/info.png)
- ### 도움말(관리자와 연결)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/help.png)
- ### 탑승 대기 버튼(버튼 이벤트 발생 시 탑승 대기 인원 +1)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/plus.png)
- ### 탑승 취소 버튼(버튼 이벤트 발생 시 탑승 대기 인원 -1)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/minus.png)
- ### App 작동 시 발생 오류
    - ### 버스를 선택하지 않은 경우
        ![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/NoSelect.png)
    - ### 탑승 최대 인원 50명인 상태에서 탑승 대기 버튼 클릭하는 경우
        ![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/over.png)
    - ### 탑승 인원이 0명인 상태에서 탑승 취소 버튼 클릭하는 경우
        ![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/zero.png)
- ### 알림 지우기(우측 하단 X 버튼)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/clearnote.png)
- ### Device On (좌측 상단 Device on/off 버튼)
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/deviceOn.png)
- ### Device Off
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/deviceOff.png)
## 프로그램 로직
- ### 자세한 내용은 소스코드 및 주석 참조
#### 1) initUI(DB연결 및 정보출력)
- 상태바에 시간 출력 및 DB 연결, QTableWidget인 BusInfor에 DB의 정보 출력
#### 2) initSignal(버튼 시그널)
- 버튼 시그널 및 슬롯함수 연결 구문을 따로 빼주지 않으면 슬롯함수가 2번 호출되는 오류 발생
#### 3) CellPosition(셀 클릭 위치 확인)
- 사용자가 QTableWidget에 출력된 정보 중 본인이 탑승할 버스의 선택을 확인함 / Bool 함수를 통해 클릭 유무를 확인
#### 4) BtnAddCntClicked(탑승 대기)
- 셀 클릭 이후 탑승 대기 버튼 - 탑승 대기 인원을 1 증가시키고 탑승 대기 완료 메시지 출력 / 최대 인원 : 50명
#### 5) BtnMinusCntClicked(탑승 취소)
- 셀 클릭 이후 탑승 취소 버튼 - 탑승 대기 인원을 1 감소시키고 탑승 취소 완료 메시지 출력 / 탑승 인원 0명일때 클릭 시 오류
#### 6) updateTable(업데이트)
- DB가 변경되는 작업 수행 이후 최신화된 정보를 출력시키기 위함
#### 7) BtnSearchClicked(정보 출력 버튼) 
- 정보 출력 시 initUI를 호출하여 최신 DB 정보 출력
#### 8) BtnHideClicked(정보 숨기기 버튼)
- QTableWidget에 출력된 정보를 사용자가 볼 수 없도록 가리기 위함
#### 9) BtnInfoClicked(Bustop이란?)
- 프로그램 설명을 위함
#### 10) BtnHelpClicked(도움말)
- 관리자와 연결
#### 11) BtnClearNoteClicked(우측 하단 {x} 버튼)
- 알림 / 정보 출력 패널 모두 지우기 위함
#### 12) BtnDeviceOnOffClicked(장치 ON/OFF 버튼)
- 장치의 전원을 ON/OFF 시키기 위함
#### cf) QTimer를 사용하여 DB 정보 변경 시 실시간으로 프로그램에 반영
- BtnSearch 버튼 클릭 시 timer.start
- BtnHide 버튼 / Device Off 모드 일 때 timer.stop 

# App 실행 화면
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/BuSTOP.gif)

## 05_11 소스코드 수정
#### 1) 현재 탑승 인원 추가, 탑승 대기인원 + 탑승 추가인원을 기준으로 최대 탑승인원을 계산
- #### 탑승 대기인원 + 탑승 추가인원 >=50 인 경우 탑승 대기를 더이상 하지 못하도록 탑승 대기 버튼 비활성화
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/Over50.png)
- #### 탑승 대기인원 = 0 인 경우 탑승 취소를 못하도록 탑승 취소 버튼 비활성화
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/Cnt_zero.png)
#### 2) 1)번 문제 icon 비활성화를 위해 커스텀 클래스인 IconButton 생성
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/0511_iconVisible.png)
#### 3) Device ON/OFF 시 icon 활성화 / 비활성화
![](https://raw.githubusercontent.com/PKNU-IOT3/bustop_PyQT/main/images/Device_off.png)
