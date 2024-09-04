from PyQt5 import QtWidgets, uic
from program_window import ProgramWindow  # ProgramWindow를 import합니다.

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi('..\\gui\\login_form.ui', self)

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.open_register_window)
        self.pushButton_3.clicked.connect(self.open_forgot_window)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if username == "admin" and password == "password":
            QtWidgets.QMessageBox.information(self, "Login", "Login Successful")
            self.open_program_window()  # 로그인 성공 시 ProgramWindow로 이동합니다.
        else:
            QtWidgets.QMessageBox.warning(self, "Login", "Invalid Credentials")

    def open_register_window(self):
        # 회원가입 창 열기
        pass

    def open_forgot_window(self):
        QtWidgets.QMessageBox.information(self, "Forgot ID/PW", "Open Forgot ID/PW Window")

    def open_program_window(self):
        self.program_window = ProgramWindow()  # ProgramWindow 인스턴스 생성
        self.program_window.show()  # ProgramWindow 표시
        self.close()  # LoginWindow 닫기
