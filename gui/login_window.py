import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit
import requests
from PyQt5.QtCore import QEvent, pyqtSignal  # QEvent를 QtCore에서 임포트
class LoginWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi('ui\\login_form.ui', self)


        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.open_register_window)
        self.pushButton_3.clicked.connect(self.open_forgot_window)

        self.lineEdit_2.textChanged.connect(self.hide_password_on_input)  # 입력이 시작되면 숨기기

        # 이벤트 필드에 마우스 클릭 시 텍스트 지우기
        self.lineEdit.installEventFilter(self)
        self.lineEdit_2.installEventFilter(self)


    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:  # 클릭 이벤트
            if source == self.lineEdit or source == self.lineEdit_2:
                source.clear()  # 텍스트 지우기
        return super().eventFilter(source, event)

    def hide_password_on_input(self):
        """입력 시작 시 비밀번호 필드를 숨김으로 설정"""
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

    def login(self):
        # 사용자가 입력한 이메일과 비밀번호 가져오기
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # FastAPI 백엔드로 로그인 요청을 보낼 데이터
        login_data = {
            "user_email": username,
            "password": password
        }

        try:
            # FastAPI 백엔드의 로그인 엔드포인트로 POST 요청
            response = requests.post("http://localhost:8000/login", json=login_data)

            # 요청에 대한 응답 확인
            if response.status_code == 200:
                # 로그인 성공
                QtWidgets.QMessageBox.information(self, "Login", "로그인되었습니다.")
                # ProgramWindow로 이동
                from program_window import ProgramWindow
                self.program_window = ProgramWindow(username)  # user_email 전달
                self.program_window.show()
                self.close()  # 로그인 창 닫기

            elif response.status_code == 400:
                # 이메일/비밀번호 오류
                QtWidgets.QMessageBox.warning(self, "Login", "이메일/비밀번호가 일치하지 않습니다.")
            elif response.status_code == 403:
                # 이미 로그인된 사용자
                QtWidgets.QMessageBox.warning(self, "Login", "이미 로그인된 사용자입니다.")
            else:
                # 기타 오류 처리
                QtWidgets.QMessageBox.warning(self, "Login", "로그인 중 오류가 발생했습니다.")
        except requests.exceptions.RequestException as e:
            # 서버 요청 실패 시 처리
            QtWidgets.QMessageBox.critical(self, "Error", f"서버에 연결할 수 없습니다: {e}")

    def open_register_window(self):
        from register_window import RegisterWindow  # 여기서 import
        self.register_window = RegisterWindow()  # RegisterWindow 인스턴스 생성
        self.register_window.show()  # RegisterWindow 표시
        self.close()  # LoginWindow 닫기

    def open_forgot_window(self):
        QtWidgets.QMessageBox.information(self, "Forgot ID/PW", "Open Forgot ID/PW Window")


    # exception 발생시 종료 방지
    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook