# app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic.properties import QtWidgets
from register_window import RegisterWindow
from login_window import LoginWindow

def main():
    # 로그인 창을 처음 표시합니다.
    app = QApplication(sys.argv)
    login_window = LoginWindow()  # 로그인 창 인스턴스 생성
    login_window.show()  # 로그인 창 표시
    sys.exit(app.exec_())
     # 회원가입창 첫화면
    # register_window = RegisterWindow()
    # register_window.show()

if __name__ == '__main__':
    main()

