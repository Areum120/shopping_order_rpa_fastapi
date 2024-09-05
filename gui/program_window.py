from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import sys
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLineEdit, QApplication
import pandas as pd
from fastApiProject.classi.send_email import Send
import fastApiProject.classi.data_store
import fastApiProject.classi.set_excel_form

class ProgramWindow(QMainWindow):
    def __init__(self):
        super(ProgramWindow, self).__init__()
        base_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = base_path + '\\gui\\order_excel_email_classify.ui'
        order_ui = uic.loadUi(ui_path, self)

        if not os.path.exists(ui_path):
            print(f"UI 파일을 찾을 수 없습니다: {ui_path}")

        self.folder_path = ""

        default_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.lineEdit.setText(default_path)

        default_folder_name = "Sherlock_folder"
        self.lineEdit_2.setText(default_folder_name)

        self.lineEdit_9.setEchoMode(QLineEdit.Password)

        self.start_auto_create_folder()

        self.pushButton.clicked.connect(self.select_directory)
        self.pushButton_2.clicked.connect(self.create_folder)
        self.pushButton_3.clicked.connect(self.upload_excel)
        self.pushButton_4.clicked.connect(self.upload_excel2)
        self.pushButton_5.clicked.connect(self.start_excel_classification)
        self.pushButton_6.clicked.connect(self.confirm_email)
        self.pushButton_8.clicked.connect(self.send_email)
        self.email_content_confirmed = False

        self.label_15.setTextFormat(Qt.RichText)
        self.label_16.setTextFormat(Qt.RichText)

        self.label_15.setOpenExternalLinks(True)
        self.label_16.setOpenExternalLinks(True)

    # 원하는 경로를 검색해서 폴더 생성하기
    def select_directory(self):
        # 바탕화면을 기본 경로로 설정
        default_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # 폴더 선택 다이얼로그에서 기본 경로를 설정
        folder_path = QFileDialog.getExistingDirectory(self, "선택", default_path)
        if folder_path:
            self.lineEdit.setText(folder_path)  # 경로 입력
            self.label.setText(f"폴더 이름을 적고 생성/지정 버튼을 클릭해주세요.")
            self.label.setStyleSheet("color: red;")
        else:
            self.label.setText("경로를 선택한 후 폴더 이름을 꼭 지정해주세요.")  # 메시지 표시
            self.label.setStyleSheet("color: red;")

    def create_folder(self):
        self.folder_name = self.lineEdit_2.text()
        folder_path = os.path.join(os.path.expanduser("~"), "Desktop", self.folder_name)
        directory = self.lineEdit.text()  # 입력한 경로
        classi.data_store.file_path = os.path.join(directory, self.folder_name)

        if self.folder_name and directory:
            # 폴더가 이미 존재하는지 확인
            if os.path.exists(classi.data_store.file_path):
                self.label.setText(f"'{folder_path}' 폴더가 이미 존재합니다.")
                self.label.setStyleSheet("color: red;")
                # 폴더 열기
                subprocess.run(['explorer', classi.data_store.file_path])
            else:
                try:
                    os.makedirs(classi.data_store.file_path)  # 폴더 생성 함수
                    self.label.setText(f"'{folder_path}' 폴더가 생성되었습니다.")
                    self.label.setStyleSheet("color: green;")
                    # 현재 작업 디렉토리 변경
                    os.chdir(directory)
                    # 폴더 열기
                    subprocess.run(['explorer', classi.data_store.file_path])
                except OSError as e:
                    self.label.setText(f"폴더를 생성하는 동안 오류가 발생했습니다: {e}")
                    self.label.setStyleSheet("color: red;")
        else:
            self.label.setText("폴더 이름과 경로를 입력하세요.")
            self.label.setStyleSheet("color: red;")

    # 프로그램 시작 시 create_folder 호출
    def start_auto_create_folder(self):
        self.create_folder()

    # 엑셀 파일 업로드 기능
    def upload_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "", "Excel Files (*.xls;*.xlsx)")
        self.lineEdit_3.setText(file_path)  # 경로입력
        if file_path:
            try:
                # 엑셀 파일 읽기 (pandas 사용)
                self.order_list = pd.read_excel(file_path)
                # '상품명' 칼럼이 있는지 확인
                if '상품명' not in self.order_list.columns:
                    # '상품명' 칼럼이 없으면 메시지 출력
                    self.label_2.setText("파일의 칼럼명을 '상품명'으로 일치시켜주세요.")
                    self.label_2.setStyleSheet("color: red;")
                else:
                    # '상품명' 칼럼이 있으면 성공 메시지 출력
                    self.label_2.setText("엑셀 파일을 성공적으로 업로드했습니다.")
                    self.label_2.setStyleSheet("color: green;")
                print(self.order_list)
            except Exception as e:
                self.label_2.setText(f"엑셀 파일을 업로드하는 동안 오류가 발생했습니다: {e}")
                self.label_2.setStyleSheet("color: red;")

    def upload_excel2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "", "Excel Files (*.xls;*.xlsx)")
        self.lineEdit_4.setText(file_path)  # 경로 입력
        if file_path:
            try:
                # 엑셀 파일 읽기 (pandas 사용)
                self.df2 = pd.read_excel(file_path)
                print(self.df2)
                # '브랜드'와 '업체명' 칼럼 확인
                if '브랜드' not in self.df2.columns or '업체명' not in self.df2.columns or '담당자' not in self.df2.columns or '이메일' not in self.df2.columns or '참조이메일' not in self.df2.columns:
                    # 필요한 칼럼이 없으면 메시지 출력
                    self.label_2.setText("파일의 칼럼명을 '브랜드','업체명','담당자','이메일','참조이메일'으로 일치시켜주세요.")
                    self.label_2.setStyleSheet("color: red;")
                    return
                self.brands = self.df2['브랜드'].to_list()
                # df_partners['업체명'] 칼럼의 NaN 값을 앞의 값으로 채우기
                self.df2['업체명'] = self.df2['업체명'].fillna(method='ffill')
                self.partners = self.df2['업체명'].to_list()
                self.label_2.setText(f"엑셀 파일을 성공적으로 업로드했습니다.")
                self.label_2.setStyleSheet("color: green;")
            except Exception as e:
                self.label_2.setText(f"엑셀 파일을 업로드하는 동안 오류가 발생했습니다: {e}")
                self.label_2.setStyleSheet("color: red;")

    # 엑셀 분류 작업
    def start_excel_classification(self):
        folder_name = self.lineEdit_2.text()  # 폴더 이름
        excelfolder_path = self.lineEdit.text()  # 입력한 경로
        print(folder_name)
        print(excelfolder_path)
        now = datetime.now()  # 지금시간
        self.nowToday = now.strftime('%Y-%m-%d')  # 일자
        if not folder_name or not excelfolder_path:
            self.label_2.setText("폴더 이름과 경로를 입력하세요.")
        else:
            excel_file_path = self.lineEdit_3.text()  # 업로드한 엑셀 파일 경로
            if not excel_file_path:
                self.label_2.setText("엑셀 파일을 먼저 업로드하세요.")
            else:
                try:
                    # 엑셀 분류 로직을 수행
                    now = datetime.now()  # 올바르게 datetime 클래스를 사용
                    self.nowToday = now.strftime('%Y-%m-%d')  # 일자
                    for i, row in self.order_list.iterrows():
                        brand_name = ''
                        partner_name = ''
                        for j in range(len(self.brands)):
                            if self.brands[j] in row['상품명']:
                                brand_name = self.brands[j]
                                partner_name = self.partners[j]
                                break
                        # 파일 저장
                        if partner_name != '':
                            df_filtered = self.order_list[self.order_list['상품명'].str.contains(brand_name)]
                            df_filtered.to_excel(
                                f'{classi.data_store.file_path}/{self.nowToday}_{partner_name}.xlsx')
                        else:
                            self.label_3.setText(f"없는 brand name:, '{brand_name}', '{row['상품명']}'")
                        print(classi.data_store.file_path)
                    # 폴더 안의 엑셀 파일 갯수 세서 출력
                    files_and_dirs = os.listdir(classi.data_store.file_path)
                    print(files_and_dirs)
                    file_count = sum(
                        1 for item in files_and_dirs if
                        os.path.isfile(os.path.join(classi.data_store.file_path, item)))
                    print(file_count)
                    # 엑셀 분류 작업 완료 후 엑셀 폼 설정 작업 호출
                    classi.set_excel_form.modify_form(classi.data_store.file_path)
                    return self.label_3.setText(f"'총 전체 주문건수 {len(self.order_list)}건, {file_count}개 업체 파일이 만들어졌습니다")
                    self.label_2.setText(f"엑셀 파일을 분류하고 '{self.folder_name}' 폴더에 저장했습니다.")
                    # 현재 작업 디렉토리 변경
                    os.chdir(excelfolder_path)
                    # 폴더 열기
                    os.system('explorer "{}"'.format(folder_name))
                except Exception as e:
                    print(e)
                    self.label_2.setText(f"엑셀 파일 분류 및 저장 중 오류가 발생했습니다: {e}")

    def confirm_email(self):
        # 전체 칼럼 보기 설정
        try:
            pd.set_option('display.max_columns', None)
            # 협력사 data 불러오기
            # info_df = pd.read_excel(self.df2, engine='openpyxl')
            print(self.df2)
            # data폴더 파일 이름 목록 불러오기
            file_list = os.listdir(classi.data_store.file_path)  # 경로
            # print(file_list)#attachment에 확장자명까지 기입
            # email_list.xlsx 파일이 포함되어 있다면 제거
            if 'email_list.xlsx' in file_list:
                file_list.remove('email_list.xlsx')
            # 확장자명 제외한 이름 출력
            file_name = []
            for file in file_list:
                if file.count(".") == 1:
                    name = file.split('.')[0]
                    file_name.append(name)
                else:
                    for i in range(len(file) - 1, 0, -1):
                        if file[i] == '.':
                            file_name.append(file[:i])
                            break
            print(file_name)
            # print(len(file_name))#22개

            # 파일 이름 중복 여부 확인
            if len(file_name) != len(set(file_name)):
                self.label_4.setText("같은 이름의 파일을 중복 파일을 먼저 정리해주세요.")
                self.label_4.setStyleSheet("color: red;")
                return

            # 리스트 컴프리헨션을 사용하여 문자열만 추출
            result = [item.split('_', 1)[1] for item in file_name]
            print(result)
            title = self.lineEdit_6.text()
            text = self.textEdit.toPlainText()
            # 데이터 출력 (디버깅용)
            print(title)
            print(text)
            # email_list 만들기
            # 브랜드 칼럼에서 일부 일치하는 항목(문자열 아닌 값 무시) 필터링
            matching_rows = self.df2[
                self.df2['업체명'].apply(lambda x: isinstance(x, str) and any(brand in x for brand in result))]
            print(matching_rows)
            # nan값 제외
            email_list = matching_rows['이메일'].dropna().tolist()
            ref_email_list = matching_rows['참조이메일'].dropna().tolist()

            # 불러온 파일명은 그대로 첨부파일 명에 기재
            print(email_list)
            print(ref_email_list)
            print(file_list)
            print(len(email_list))
            print(len(ref_email_list))
            print(len(file_list))

            # df 생성(recipient, title, text, attachment)
            table_name = {
                '받는메일': email_list,
                '참조': ref_email_list,
                '제목': title,  # title 동일
                '내용': text,  # text 동일
                '첨부파일': file_list
            }
            email_list = pd.DataFrame(table_name)
            print(email_list)
            # 인덱스 컬럼 없이 값만 엑셀 저장
            # 저장할 경로
            classi.data_store.email_file_path = f"{classi.data_store.file_path}/email_list.xlsx"
            email_list.to_excel(classi.data_store.email_file_path, index=False, header=True)
            print('파일 생성 완료')
            # 파일 열기
            os.startfile(classi.data_store.email_file_path)
            self.label_4.setText(f"메일 내용을 작성한 파일이 만들어졌습니다.")
            self.label_4.setStyleSheet("color: green;")
        except Exception as e:
            self.label_4.setText(f"상품명/발주처 파일을 업로드 후 클릭해주세요.")
            print(e)
            self.label_4.setStyleSheet("color: red;")
        self.email_content_confirmed = True  # 메일 내용이 확인되었음을 표시

    def send_email(self):
        if not self.email_content_confirmed:
            self.label_4.setText("메일 내용 확인 후 메일 발송해주세요.")
            self.label_4.setStyleSheet("color: red;")
        else:
            self.label_4.setText("메일 발송 중...")
            self.label_4.setStyleSheet("color: green;")

            # 메일 발송 로직 호출
            try:
                email_id = self.lineEdit_8.text()  # 이메일
                email_pw = self.lineEdit_9.text()  # 앱비밀번호
                # 이메일 발송을 위한 엑셀 파일 경로 지정
                email_file_path = f"{classi.data_store.file_path}\email_list.xlsx"
                print(email_file_path)  # 디버깅을 위해 경로 출력
                # 이메일 발송 클래스 인스턴스 생성 및 발송
                sender = Send(email_id, email_pw, email_file_path, self.label_4)
                sender.send_email()
                print("메일 발송 로직 호출")

            except Exception as e:
                self.label_4.setText(f"메일 발송 중 오류 발생하였습니다.")
                print(e)
                self.label_4.setStyleSheet("color: red;")
            self.email_content_confirmed = False  # 발송 후 확인 상태 초기화



    # exception 발생시 종료 방지
    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = ProgramWindow()
#     main_window.show()
#     sys.exit(app.exec_())