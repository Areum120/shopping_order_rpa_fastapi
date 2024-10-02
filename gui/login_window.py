from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit

from program_window import ProgramWindow  # ProgramWindow를 import합니다.
from PyQt5.QtCore import QEvent  # QEvent를 QtCore에서 임포트

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi('ui\\login_form.ui', self)

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.open_register_window)
        self.pushButton_3.clicked.connect(self.open_forgot_window)

        # 비밀번호 입력 필드 설정 (텍스트 숨기기)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # 비밀번호 입력 필드

        # 이벤트 필드에 마우스 클릭 시 텍스트 지우기
        self.lineEdit.installEventFilter(self)
        self.lineEdit_2.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:  # 클릭 이벤트
            if source == self.lineEdit or source == self.lineEdit_2:
                source.clear()  # 텍스트 지우기
        return super().eventFilter(source, event)

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username == "admin" and password == "password":
            QtWidgets.QMessageBox.information(self, "Login", "로그인되었습니다.")
            self.open_program_window()  # 로그인 성공 시 ProgramWindow로 이동합니다.
        else:
            QtWidgets.QMessageBox.warning(self, "Login", "이메일/비밀번호가 일치하지 않습니다.")

    def open_register_window(self):
        # 회원가입 창 열기
        pass

    def open_forgot_window(self):
        QtWidgets.QMessageBox.information(self, "Forgot ID/PW", "Open Forgot ID/PW Window")

    def open_program_window(self):
        self.program_window = ProgramWindow()  # ProgramWindow 인스턴스 생성
        self.program_window.show()  # ProgramWindow 표시
        self.close()  # LoginWindow 닫기
