import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent  # QEvent를 QtCore에서 임포트
from login_window import LoginWindow  # 로그인 화면 클래스를 import

class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        # UI 파일 로드
        uic.loadUi('ui/join.ui', self)

        # 비밀번호 입력 필드 설정 (텍스트 숨기기)
        self.lineEdit_4.setEchoMode(QLineEdit.Password)  # 비밀번호 입력 필드
        self.lineEdit_7.setEchoMode(QLineEdit.Password)  # 비밀번호 확인 입력 필드

        # 상태 플래그 초기화
        self.is_user_email_checked = False  # 이메일 중복 확인 여부 플래그
        self.is_email_verified = False  # 이메일 인증 여부 플래그
        self.verification_code = ""  # 발송된 인증 코드를 저장하는 변수

        # 버튼 클릭 시 호출될 메서드 연결
        self.pushButton.clicked.connect(self.check_user_email)  # 이메일 중복 검사 버튼
        self.pushButton_2.clicked.connect(self.register)  # 회원가입 버튼
        self.pushButton_4.clicked.connect(self.send_verification_email)  # 이메일 인증 버튼
        self.pushButton_5.clicked.connect(self.verify_code)  # 인증 코드 확인 버튼
        self.pushButton_6.clicked.connect(self.resend_verification_email)  # 인증 코드 재발송 버튼
        self.pushButton_3.clicked.connect(self.go_to_login)  # 로그인 화면 버튼

        # 인증 코드 입력 필드와 버튼 숨기기
        self.lineEdit_8.setVisible(False)  # 인증 코드 입력 필드
        self.pushButton_5.setVisible(False)  # 인증 코드 확인 버튼
        self.pushButton_6.setVisible(False)  # 재발송 버튼

        # 이벤트 필드에 마우스 들어올 때 및 나갈 때 텍스트 지우기
        self.lineEdit_8.installEventFilter(self)
        self.lineEdit_5.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:  # 클릭 이벤트
            if source == self.lineEdit_8 or source == self.lineEdit_5:
                source.clear()  # 텍스트 지우기
        return super().eventFilter(source, event)


    def check_user_email(self):
        """이메일 중복 확인 메서드"""
        user_email = self.lineEdit_3.text()  # 이메일 입력 필드에서 값 가져오기
        if not user_email:
            # 이메일이 비어있을 경우 경고 메시지 표시
            QtWidgets.QMessageBox.warning(self, "Check User Email", "이메일(아이디) 중복검사를 해주세요.")
            return

        try:
            # 이메일 중복 검사 요청
            response = requests.get(f"http://127.0.0.1:8000/check_user_email/{user_email}")
            if response.status_code == 200:
                result = response.json()
                if result['exists']:
                    # 이메일이 이미 존재하는 경우 경고 메시지 표시
                    QtWidgets.QMessageBox.warning(self, "Check User Email", "이메일이 이미 존재합니다.")
                    self.is_user_email_checked = False
                else:
                    # 이메일이 사용 가능한 경우 정보 메시지 표시
                    QtWidgets.QMessageBox.information(self, "Check User Email", "이메일 사용이 가능합니다.")
                    self.is_user_email_checked = True

        except requests.exceptions.RequestException as e:
            # 요청 실패 시 에러 메시지 표시
            QtWidgets.QMessageBox.critical(self, "Check User Email", f"Request failed: {e}")

    def send_verification_email(self):
        """이메일 인증 코드 발송 메서드"""
        if not self.is_user_email_checked:
            # 이메일 중복 확인이 되지 않았을 경우 경고 메시지 표시
            QtWidgets.QMessageBox.warning(self, "Send Verification Email", "이메일 중복검사를 해주세요.")
            return

        email = self.lineEdit_3.text()  # 이메일 입력 필드에서 값 가져오기
        if not email:
            # 이메일이 비어있을 경우 경고 메시지 표시
            QtWidgets.QMessageBox.warning(self, "Send Verification Email", "이메일 주소를 입력하세요.")
            return
        try:
            # 이메일 인증 코드 발송 요청
            response = requests.post(f"http://127.0.0.1:8000/send_verification_code", json={"user_email": email})
            if response.status_code == 200:
                # 성공 시 정보 메시지 표시
                self.verification_code = response.json().get("verification_code")  # 서버에서 받은 인증 코드 저장
                QtWidgets.QMessageBox.information(self, "Send Verification Email", "이메일 인증 코드가 발송되었습니다.")
                self.is_email_verified = False  # 이메일 인증 요청 완료
                self.show_verification_fields()  # 인증 코드 입력 필드 보여주기
            else:
                # 실패 시 에러 메시지 표시
                QtWidgets.QMessageBox.critical(self, "Send Verification Email", f"Error: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            # 요청 실패 시 에러 메시지 표시
            QtWidgets.QMessageBox.critical(self, "Send Verification Email", f"Request failed: {e}")

    def show_verification_fields(self):
        """인증 코드 입력 필드 보여주기"""
        self.lineEdit_8.setVisible(True)  # 인증 코드 입력 필드
        self.pushButton_5.setVisible(True)  # 인증 코드 확인 버튼
        self.pushButton_6.setVisible(True)  # 재발송 버튼

    def verify_code(self):
        """인증 코드 확인 메서드"""
        input_code = self.lineEdit_8.text()
        email = self.lineEdit_3.text()

        try:
            response = requests.get(f"http://127.0.0.1:8000/verify_code?email={email}&code={input_code}")
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Verify Code", "인증 코드가 확인되었습니다.")
                self.is_email_verified = True  # 이메일 인증 완료

                # 인증이 완료되었으므로 인증 코드 입력 필드와 버튼을 숨기기
                self.lineEdit_8.setVisible(False)  # 인증 코드 입력 필드 숨기기
                self.pushButton_5.setVisible(False)  # 인증 코드 확인 버튼 숨기기
                self.pushButton_6.setVisible(False)  # 재발송 버튼 숨기기

                # 이메일 인증 버튼 텍스트를 "인증 완료"로 변경하고 색상을 파란색으로 변경
                self.pushButton_4.setText("인증 완료")
                self.pushButton_4.setStyleSheet("background-color: blue; color: white;")
            else:
                QtWidgets.QMessageBox.warning(self, "Verify Code", "유효하지 않은 인증 코드입니다.")
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Verify Code", f"Request failed: {e}")


    def resend_verification_email(self):
        """인증 코드 재발송 메서드"""
        self.send_verification_email()

    def register(self):
        """회원가입 메서드"""
        if not self.is_user_email_checked:
            # 이메일 중복 확인이 되지 않았을 경우 경고 메시지 표시
            QtWidgets.QMessageBox.warning(self, "Register", "이메일 중복 검사를 먼저 해주세요.")
            return

        if not self.is_email_verified:
            # 이메일 인증이 되지 않았을 경우 경고 메시지 표시
            QtWidgets.QMessageBox.warning(self, "Register", "이메일 인증을 해주세요.")
            return

        password = self.lineEdit_4.text()  # 비밀번호 입력 필드에서 값 가져오기
        confirm_password = self.lineEdit_7.text()  # 비밀번호 확인 필드에서 값 가져오기

        if password != confirm_password:
            # 비밀번호와 비밀번호 확인이 일치하지 않을 경우 에러 메시지 표시
            self.label_7.setText("비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
            return

        data = {
            "user_email": self.lineEdit_3.text(),  # 이메일
            "password": password,  # 비밀번호
            "phone_number": self.lineEdit_5.text(),  # 전화번호
        }

        # recommender = self.lineEdit_6.text().strip()  # 추천인 (선택적)
        # if recommender:
        #     data["recommender"] = recommender

        try:
            # 회원가입 요청
            response = requests.post("http://127.0.0.1:8000/register/", json=data)
            if response.status_code == 200:
                # 성공 시 정보 메시지 표시
                QtWidgets.QMessageBox.information(self, "Register", "회원가입이 완료되었습니다.")
                self.close()  # 창 닫기
            else:
                # 실패 시 에러 메시지 표시
                QtWidgets.QMessageBox.critical(self, "Register", f"Error: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            # 요청 실패 시 에러 메시지 표시
            QtWidgets.QMessageBox.critical(self, "Register", f"Request failed: {e}")

    def go_to_login(self):
        # 로그인 창을 생성하고 현재 창을 닫음
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()