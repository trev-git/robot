from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from .main_interface_ui import Ui_MainInterface
from .calibration.calibration_window import CalibrationWindow
from .workspace_calibration.workspace_calibration import WorkspaceCalibration
from .point_transformation.point_transformation import PointTransformation
from utils import CONFIG_DIR, ROOT_DIR


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
        self.ui.db_file_pick.clicked.connect(self.select_db_file)
        self.ui.load_db.clicked.connect(self.load_db)
        self.ui.point_transformation.clicked.connect(self.point_transformation)

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
        self.ui.calibration_workspace.setEnabled(True)

    def select_db_file(self):
        file_name = QFileDialog().getOpenFileName(self, 'Выберите файл БД', f'{ROOT_DIR}/web_point.db', '*.db')
        self.ui.db_file_name.setText(file_name[0])
        self.ui.load_db.setEnabled(True)
        self.ui.point_transformation.setEnabled(True)

    def load_db(self):
        error = self.robot.PointTableUpLoad(self.ui.db_file_name.text())
        if error:
            QMessageBox().critical(self, "Ошибка", "Не удалось загрузить базу данных в робота!")
        else:
            QMessageBox().information(self, "Успешно", "База данных загружена успешно!")

    def point_transformation(self):
        self.point_transformation_window = PointTransformation(self.ui.db_file_name.text())
        self.point_transformation_window.show()
