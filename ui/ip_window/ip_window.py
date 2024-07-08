from PyQt6.QtWidgets import QWidget, QMessageBox
from .ip_window_ui import Ui_IPWindow
from ..main_interface.main_interface import MainInterface
from sys import exit, path
import platform
import ipaddress


if platform.system() == "Windows":
    fairino_path = "C:\\FAIRINO\\PythonSDK\\windows\\libfairino\\fairino"
else:
    print("Эта программа не поддерживается на вашей ОС!")
    exit(1)

path.append(fairino_path)
import Robot


class IPWindow(QWidget):
    def __init__(self):
        super(IPWindow, self).__init__()
        self.ui = Ui_IPWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Робот")

        self.ui.exit.clicked.connect(exit)
        self.ui.continue_2.clicked.connect(self.connect_to_robot)

    def connect_to_robot(self):
        try:
            _ = ipaddress.ip_address(self.ui.ip_address.text())
        except:
            QMessageBox.critical(
                self, "Ошибка", "Введён неверный IP-адрес! Повторите попытку."
            )
            return
        robot = Robot.RPC(self.ui.ip_address.text())
        robot.SetSpeed(5)
        self.hide()
        self.main_interface = MainInterface(robot)
        self.main_interface.show()
