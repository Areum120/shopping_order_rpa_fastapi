# shopping_order_rpa Guide

### 필요 라이브러리 설치 

pip install -r requirements.txt

### exe 실행파일 Build
- -w : 콜솔창x -F : onefile 

cd 폴더 설치 경로

pyinstaller -w -F classi\excel_clsfn.py

### build 완료 시

dist 폴더에 excel_clsfn.exe 파일 생성 확인

### app 실행

# 24.08.15 update

## 'pyinstaller'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는
배치 파일이 아닙니다. 오류시 아래 참고

### 1. 설치 경로 찾기
python -m site --user-site

예를 들어 아래 경로로 나오면 아래 경로 Scripts 폴더 안에 설치 되어 있음.
C:\Users\USERNAME\AppData\Roaming\Python\PythonXX\site-packages

### 2. 확인한 설치 경로 /Scripts 경로 추가해서 아래 명령어로 설치 

C:\Users\USERNAME\AppData\Roaming\Python\PythonXX\Scripts\pyinstaller --onefile --noconsole classi\excel_clsfn.py

ui 경로를 찾을 수 없으면 아래 명령어로 설치

C:\Users\USERNAME\AppData\Roaming\Python\PythonXX\Scripts\pyinstaller --onefile --noconsole --add-data "gui/order_excel_email_classify.ui;gui" main.py


만약 import한 다른 py 파일을 못찾을 경우
프로젝트 루트 폴더 아래처럼 만들고 excel_clsfn.py를 exe파일로 생성
다른 py파일 import할땐 같은 폴더라도 classi.data_store처럼 꼭 명시

### project_root/
### │
### ├── classi/
### │   ├── __init__.py
### │   ├── send_email.py
### │   ├── data_store.py
### │
### ── gui/
### │   ├── __init__.py
### │   ├── order_excel_email_classify.ui
### │
### │── excel_clsfn.py


## 만약 상대경로 문제 발생시

스크립트가 임시 디렉토리에서 실행될 경우 절대 경로를 설정해도 경로를 못찾을 수 있음

  base_path = os.path.dirname(os.path.abspath(__file__))
  print(base_path)
  ui_path = base_path + '\\gui\\order_excel_email_classify.ui'

그럴 때는 ui 파일을 같이 실행파일 포함시킬 것
pyinstaller --onefile --noconsole --add-data "gui/order_excel_email_classify.ui;gui" excel_clsfn.py
 


## 업무 요건
- 인터넷 사용 가능시
