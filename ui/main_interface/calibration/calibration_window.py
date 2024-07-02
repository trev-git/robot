from PyQt6.QtWidgets import QWidget
from .calibration_window_ui import Ui_CalibrationWindow
from utils import ROOT_DIR

class CalibrationWindow(QWidget):
    def __init__(self, robot):
        super(CalibrationWindow, self).__init__()
        self.ui = Ui_CalibrationWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Калибровка по шести точкам')
        self.robot = robot
        self.step = 1

        self.ui.calibration_1.clicked.connect(self.get_point)
        self.ui.calibration_2.clicked.connect(self.get_point)
        self.ui.calibration_3.clicked.connect(self.get_point)
        self.ui.calibration_4.clicked.connect(self.get_point)
        self.ui.calibration_5.clicked.connect(self.get_point)
        self.ui.calibration_6.clicked.connect(self.get_point)

    def get_point(self):
        self.step += 1
        match self.step:
            case 2:
                self.ui.calibration_1.setEnabled(False)
                self.ui.calibration_2.setEnabled(True)
            case 3:
                self.ui.calibration_2.setEnabled(False)
                self.ui.calibration_3.setEnabled(True)
            case 4:
                self.ui.calibration_3.setEnabled(False)
                self.ui.calibration_4.setEnabled(True)
                self.ui.label.setEnabled(False)
                self.ui.label_2.setEnabled(True)
            case 5:
                self.ui.calibration_4.setEnabled(False)
                self.ui.calibration_5.setEnabled(True)
                self.ui.label_2.setEnabled(False)
                self.ui.label_3.setEnabled(True)
            case 6:
                self.ui.calibration_5.setEnabled(False)
                self.ui.calibration_6.setEnabled(True)
                self.ui.label_3.setEnabled(False)
                self.ui.label_4.setEnabled(True)
            case 7:
                self.ui.calibration_6.setEnabled(False)
                self.ui.label_4.setEnabled(False)
                self.ui.calibration_result.setEnabled(True)
