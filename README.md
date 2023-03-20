# PyQT를 활용한 버스 탑승 APP.
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
![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/QtDesigner.png)
2. MySQL DB 작성
![MySQL](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/mysql.png)
3. Python으로 기능 작성
![실행화면1](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_1.png)
![실행화면2](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_2.png)

### 로직
- 버스의 탑승대기/탑승취소 버튼을 통해 해당 버스 탑승 인원 카운팅
- 카운팅된 인원을 DB로 저장
- DB에서 변경되는 탑승인원(bus_cnt)의 내용도 앱으로 실시간 반영

## 23.03.16 프로젝트 수정
- RadioButton을 사용하여 탑승 대기 / 탑승 취소 버튼을 각각 3개에서 1개로 축소
- UI 수정
![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/QtDesigner_modify.png)
![실행화면](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_modify.png)


## 23.03.17 프로젝트 수정
- Qt Designer을 이용한 UI 수정
    ### - Grid를 이용하여 MainWindow 최대화/최소화에 따른 BUTTON 크기 조정
    ### - UI 수정
    ![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/QtDesigner_0317_1.png)
    ![QtDesigner](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/QtDesigner_0317_2.png)

- 프로그램 로직 변경
    ### - RadioButton 클릭 -> Button클릭 / 탑승 할 버스 클릭시에 Button 색상 변경
    ![실행화면1](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_1.png)
    ![실행화면3](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_3.png)
    ### - 탑승 할 버스 중복 선택 불가
    ### - resize 이벤트를 이용하여 최대화 / 최소화 시 모든 UI 크기 자동 변경
    
    ### - 탑승 할 버스 미선택 시 탑승대기 / 탑승 취소 버튼 비활성화
    ![실행화면1](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_1.png)
    ### - 탑승 할 버스의 탑승인원이 0명인 경우 탑승취소 버튼 비활성화
    ![실행화면4](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_4.png)
    ### - DB에서 버스 탑승인원 변경 시 앱에서 실시간 반영
    ![실행화면5](https://raw.githubusercontent.com/PKNU-IOT3/bustop_pyqt_practice/main/images/%EC%8B%A4%ED%96%89%ED%99%94%EB%A9%B4_0317_5.png)
