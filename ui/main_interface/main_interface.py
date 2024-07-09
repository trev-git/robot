from PyQt6.QtWidgets import QMainWindow, QFileDialog
from .main_interface_ui import Ui_MainInterface
from .calibration.calibration_window import CalibrationWindow
from .workspace_calibration.workspace_calibration import WorkspaceCalibration
from utils import CONFIG_DIR


class MainInterface(QMainWindow):
    def __init__(self, robot):
        super(MainInterface, self).__init__()
        self.ui = Ui_MainInterface()
        self.ui.setupUi(self)
        self.setWindowTitle("Робот")

        self.robot = robot

        self.ui.calibration_six_points.clicked.connect(self.calibration)
        self.ui.calibration_workspace.clicked.connect(self.calibration_workspace)
        self.ui.file_pick.clicked.connect(self.select_file)
        self.ui.statusbar.showMessage(f'Робот: {self.robot.GetControllerIP()[1]}')

    def calibration(self):
        self.calibration_window = CalibrationWindow(self.robot)
        self.calibration_window.show()

    def calibration_workspace(self):
        self.calibration_window = WorkspaceCalibration(self.robot, self.ui.spinBox.value(), self.ui.file_name.text())
        self.calibration_window.show()

    def select_file(self):
        file_name = QFileDialog().getOpenFileName(self, 'Выберите файл калибровки', f'{CONFIG_DIR}/tcf.txt', '*.txt')
        self.ui.file_name.setText(file_name[0])