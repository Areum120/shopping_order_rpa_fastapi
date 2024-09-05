# app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic.properties import QtWidgets
from register_window import RegisterWindow
from login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    # 로그인 창을 처음 표시합니다.
    # login_window = LoginWindow()
    # register_window = RegisterWindow(login_window)
    # login_window.show()  # 로그인 창을 표시
    register_window = RegisterWindow()
    register_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

