import sys
from PyQt5 import QtWidgets  # QMainWindow를 사용하기 위해 QtWidgets 모듈에서 import
from user_info_window import UserInfoWindow
from login_window import LoginWindow

class MainApp:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)  # QApplication 인스턴스 생성
        self.login_window = LoginWindow()  # LoginWindow 인스턴스 생성

    def run(self):
        self.login_window.show()  # 초기 창으로 로그인 창 표시
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
