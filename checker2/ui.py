from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
)

class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("윈도우 점검 도구")
        self.setGeometry(100, 100, 600, 500)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("아래 버튼을 눌러 시스템 상태를 확인하세요.")
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        self.sys_btn = QPushButton("시스템 정보 확인")
        self.disk_btn = QPushButton("디스크 상태 확인")
        self.proc_btn = QPushButton("프로세스 확인")
        self.net_btn = QPushButton("네트워크 상태 확인")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sys_btn)
        self.layout.addWidget(self.disk_btn)
        self.layout.addWidget(self.proc_btn)
        self.layout.addWidget(self.net_btn)
        self.layout.addWidget(self.result_area)

        self.setLayout(self.layout)
