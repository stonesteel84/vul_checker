# qt designer사용법
https://wikidocs.net/35482


# qt designer를 사용했다치고 모듈 분리하기
![image](https://github.com/user-attachments/assets/f1b28fa3-e86c-4585-a900-8e54a887b8d3)

# 예시 코드 - pyuic5가 생성한 클래스 구조는 다음과 같음

```python
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("윈도우 점검 도구")
        MainWindow.resize(600, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.label = QtWidgets.QLabel("아래 버튼을 눌러 시스템 상태를 확인하세요.")
        self.verticalLayout.addWidget(self.label)

        self.sys_btn = QtWidgets.QPushButton("시스템 정보 확인")
        self.disk_btn = QtWidgets.QPushButton("디스크 상태 확인")
        self.proc_btn = QtWidgets.QPushButton("프로세스 확인")
        self.net_btn = QtWidgets.QPushButton("네트워크 상태 확인")
        self.result_area = QtWidgets.QTextEdit()
        self.result_area.setReadOnly(True)

        self.verticalLayout.addWidget(self.sys_btn)
        self.verticalLayout.addWidget(self.disk_btn)
        self.verticalLayout.addWidget(self.proc_btn)
        self.verticalLayout.addWidget(self.net_btn)
        self.verticalLayout.addWidget(self.result_area)

        MainWindow.setCentralWidget(self.centralwidget)
```
```python
import pymysql
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

conn = pymysql.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database'],
    charset='utf8',  # utf8mb4를 지원하지 않으면 utf8 사용
    autocommit=True
)

def save_result(category, content):
    with conn.cursor() as cursor:
        sql = "INSERT INTO check_results (category, content) VALUES (%s, %s)"
        cursor.execute(sql, (category, content))

```
```python
import sys
import platform
import psutil
import socket
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow
import db_module  # DB 저장 모듈

class SystemCheckApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signals()

    def connect_signals(self):
        self.ui.sys_btn.clicked.connect(self.check_system_info)
        self.ui.disk_btn.clicked.connect(self.check_disk_info)
        self.ui.proc_btn.clicked.connect(self.check_processes)
        self.ui.net_btn.clicked.connect(self.check_network)

    def check_system_info(self):
        info = "[시스템 정보]\n"
        info += f"OS: {platform.system()} {platform.release()}\n"
        info += f"CPU: {platform.processor()}\n"
        info += f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n"
        self.ui.result_area.setPlainText(info)
        db_module.save_result("시스템 정보", info)

    def check_disk_info(self):
        info = "[디스크 정보]\n"
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                info += (f"{part.device} - 총 용량: {usage.total // (1024**3)}GB, "
                         f"사용: {usage.used // (1024**3)}GB, 남음: {usage.free // (1024**3)}GB\n")
            except PermissionError:
                continue
        self.ui.result_area.setPlainText(info)
        db_module.save_result("디스크 정보", info)

    def check_processes(self):
        info = "[실행 중인 프로세스 상위 5개 (CPU 사용량 기준)]\n"
        processes = [(p.pid, p.info['name'], p.info['cpu_percent']) 
                     for p in psutil.process_iter(['name', 'cpu_percent'])]
        processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
        for pid, name, cpu in processes:
            info += f"{pid}: {name} - CPU 사용률: {cpu}%\n"
        self.ui.result_area.setPlainText(info)
        db_module.save_result("프로세스 정보", info)

    def check_network(self):
        info = "[네트워크 상태]\n"
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        info += f"호스트 이름: {hostname}\n"
        info += f"IP 주소: {ip_address}\n"
        response = os.system("ping 8.8.8.8 -n 2 > nul")
        info += "인터넷 연결 상태: 연결됨\n" if response == 0 else "인터넷 연결 상태: 연결 안 됨\n"
        self.ui.result_area.setPlainText(info)
        db_module.save_result("네트워크 상태", info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemCheckApp()
    window.show()
    sys.exit(app.exec_())

```
![image](https://github.com/user-attachments/assets/12e5c56b-d13f-44d5-9980-dd5a8cb61f82)

