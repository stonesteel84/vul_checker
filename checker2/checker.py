import sys
import platform
import psutil
import socket
import os

from PyQt5.QtWidgets import QApplication
from ui import Ui_MainWindow
import db_module  # DB 저장용 모듈

class SystemCheckApp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.connect_signals()

    def connect_signals(self):
        self.sys_btn.clicked.connect(self.check_system_info)
        self.disk_btn.clicked.connect(self.check_disk_info)
        self.proc_btn.clicked.connect(self.check_processes)
        self.net_btn.clicked.connect(self.check_network)

    def check_system_info(self):
        info = "[시스템 정보]\n"
        info += f"OS: {platform.system()} {platform.release()}\n"
        info += f"CPU: {platform.processor()}\n"
        info += f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n"
        self.result_area.setPlainText(info)
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
        self.result_area.setPlainText(info)
        db_module.save_result("디스크 정보", info)

    def check_processes(self):
        info = "[실행 중인 프로세스 상위 5개 (CPU 사용량 기준)]\n"
        processes = [(p.pid, p.info['name'], p.info['cpu_percent']) 
                     for p in psutil.process_iter(['name', 'cpu_percent'])]
        processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
        for pid, name, cpu in processes:
            info += f"{pid}: {name} - CPU 사용률: {cpu}%\n"
        self.result_area.setPlainText(info)
        db_module.save_result("프로세스 정보", info)

    def check_network(self):
        info = "[네트워크 상태]\n"
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        info += f"호스트 이름: {hostname}\n"
        info += f"IP 주소: {ip_address}\n"
        response = os.system("ping 8.8.8.8 -n 2 > nul")
        info += "인터넷 연결 상태: 연결됨\n" if response == 0 else "인터넷 연결 상태: 연결 안 됨\n"
        self.result_area.setPlainText(info)
        db_module.save_result("네트워크 상태", info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemCheckApp()
    window.show()
    sys.exit(app.exec_())
