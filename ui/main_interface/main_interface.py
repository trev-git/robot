from PyQt6.QtWidgets import QMainWindow
from .main_interface_ui import Ui_MainInterface
from .calibration.calibration_window import CalibrationWindow


class MainInterface(QMainWindow):
    def __init__(self, robot):
        super(MainInterface, self).__init__()
        self.ui = Ui_MainInterface()
        self.ui.setupUi(self)
        self.setWindowTitle("Робот")

        self.robot = robot

        self.ui.calibration_six_points.clicked.connect(self.calibration)

    def calibration(self):
        self.calibration_window = CalibrationWindow(self.robot)
        self.calibration_window.show()
