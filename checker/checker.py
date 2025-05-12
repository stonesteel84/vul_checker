import sys
import platform
import psutil
import socket
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
)

class SystemCheckApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("윈도우 점검 도구")
        self.setGeometry(100, 100, 600, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        # 버튼 정의
        self.sys_btn = QPushButton("시스템 정보 확인")
        self.disk_btn = QPushButton("디스크 상태 확인")
        self.proc_btn = QPushButton("프로세스 확인")
        self.net_btn = QPushButton("네트워크 상태 확인")

        # 버튼 연결
        self.sys_btn.clicked.connect(self.check_system_info)
        self.disk_btn.clicked.connect(self.check_disk_info)
        self.proc_btn.clicked.connect(self.check_processes)
        self.net_btn.clicked.connect(self.check_network)

        # 레이아웃 추가
        layout.addWidget(QLabel("아래 버튼을 눌러 시스템 상태를 확인하세요."))
        layout.addWidget(self.sys_btn)
        layout.addWidget(self.disk_btn)
        layout.addWidget(self.proc_btn)
        layout.addWidget(self.net_btn)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def check_system_info(self):
        self.result_area.clear()
        info = f"[시스템 정보]\n"
        info += f"OS: {platform.system()} {platform.release()}\n"
        info += f"CPU: {platform.processor()}\n"
        info += f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n"
        self.result_area.append(info)

    def check_disk_info(self):
        self.result_area.clear()
        info = "[디스크 정보]\n"
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                info += (f"{part.device} - 총 용량: {usage.total // (1024**3)}GB, "
                         f"사용: {usage.used // (1024**3)}GB, 남음: {usage.free // (1024**3)}GB\n")
            except PermissionError:
                continue
        self.result_area.append(info)

    def check_processes(self):
        self.result_area.clear()
        info = "[실행 중인 프로세스 상위 5개 (CPU 사용량 기준)]\n"
        processes = [(p.pid, p.info['name'], p.info['cpu_percent']) 
                     for p in psutil.process_iter(['name', 'cpu_percent'])]
        processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
        for pid, name, cpu in processes:
            info += f"{pid}: {name} - CPU 사용률: {cpu}%\n"
        self.result_area.append(info)

    def check_network(self):
        self.result_area.clear()
        info = "[네트워크 상태]\n"
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        info += f"호스트 이름: {hostname}\n"
        info += f"IP 주소: {ip_address}\n"
        response = os.system("ping 8.8.8.8 -n 2 > nul")
        if response == 0:
            info += "인터넷 연결 상태: 연결됨\n"
        else:
            info += "인터넷 연결 상태: 연결 안 됨\n"
        self.result_area.append(info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemCheckApp()
    window.show()
    sys.exit(app.exec_())
