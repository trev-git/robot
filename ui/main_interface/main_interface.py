from PyQt6.QtWidgets import QMainWindow
from .main_interface_ui import Ui_MainInterface
from .calibration.calibration_window import CalibrationWindow
from .workspace_calibration.workspace_calibration import WorkspaceCalibration


class MainInterface(QMainWindow):
    def __init__(self, robot):
        super(MainInterface, self).__init__()
        self.ui = Ui_MainInterface()
        self.ui.setupUi(self)
        self.setWindowTitle("Робот")

        self.robot = robot

        self.ui.calibration_six_points.clicked.connect(self.calibration)
        self.ui.calibration_workspace.clicked.connect(self.calibration_workspace)

    def calibration(self):
        self.calibration_window = CalibrationWindow(self.robot)
        self.calibration_window.show()

    def calibration_workspace(self):
        self.calibration_window = WorkspaceCalibration(self.robot, self.ui.spinBox.value())
        self.calibration_window.show()
