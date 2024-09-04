import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit


class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        uic.loadUi('ui/join.ui', self)

        # 비밀번호 필드를 ** 처리로 설정
        self.lineEdit_4.setEchoMode(QLineEdit.Password)  # 비밀번호 입력 필드
        self.lineEdit_7.setEchoMode(QLineEdit.Password)  # 비밀번호 확인 입력 필드
        self.is_username_checked = False  # 아이디 중복 확인 여부를 추적하는 플래그
        self.pushButton.clicked.connect(self.check_username)
        self.pushButton_2.clicked.connect(self.register)

    # 아이디 중복 검사
    def check_username(self):
        username = self.lineEdit_3.text()
        if not username:
            QtWidgets.QMessageBox.warning(self, "Check Username", "Please enter a username.")
            return

        try:
            response = requests.get(f"http://127.0.0.1:8000/check_username/{username}")

            if response.status_code == 200:
                result = response.json()
                if result['exists']:
                    QtWidgets.QMessageBox.warning(self, "Check Username", "Username already exists.")
                    self.is_username_checked = False
                else:
                    QtWidgets.QMessageBox.information(self, "Check Username", "Username is available.")
                    self.is_username_checked = True

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Check Username", f"Request failed: {e}")

    # 회원가입 등록 버튼 클릭 후 백엔드 서버 요청
    def register(self):
        if not self.is_username_checked:
            QtWidgets.QMessageBox.warning(self, "Register", "Please check if the username is available.")
            return

        password = self.lineEdit_4.text()
        confirm_password = self.lineEdit_7.text()

        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Register", "Passwords do not match!")
            return

        try:
            response = requests.post("http://127.0.0.1:8000/register/", json={
                "name": self.lineEdit.text(),
                "username": self.lineEdit_3.text(),
                "password": password,
                "phone": self.lineEdit_5.text(),
                "email": self.lineEdit_2.text(),
                "recommender": self.lineEdit_6.text()
            })

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Register", "Registration Successful")
                self.close()
            else:
                QtWidgets.QMessageBox.critical(self, "Register", f"Error: {response.json().get('detail')}")

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Register", f"Request failed: {e}")