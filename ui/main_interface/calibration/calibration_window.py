# TODO:
# 1. Добавить выбор ID инструмента


from PyQt6.QtWidgets import QWidget, QMessageBox, QFileDialog
from .calibration_window_ui import Ui_CalibrationWindow
from utils import DATA_DIR, CONFIG_DIR, pose2str
import yaml
from time import sleep


class CalibrationWindow(QWidget):
    def __init__(self, robot):
        super(CalibrationWindow, self).__init__()
        self.ui = Ui_CalibrationWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Калибровка по шести точкам")

        self.robot = robot
        self.step = 1
        self.calibration_points = []

        self.ui.get_point.clicked.connect(self.get_point)
        self.ui.calibration_result.clicked.connect(self.get_calibration_result)

        self.tool_id = 0
        self.wrist_tcf = [0, 0, 0, 0, 0, 0]
        self.robot.SetToolCoord(self.tool_id, self.wrist_tcf, 0, 0)

    def get_point(self):
        if self.step == 5:
            pos_5 = self.calibration_points[3][:]
            pos_5[0] += 50
            self.robot.MoveCart(pos_5, self.tool_id, 0) # по X на +50
            sleep(5)
        elif self.step == 6:
            _, pos_6 = self.robot.GetActualTCPPose()
            pos_6[0] -= 50
            pos_6[2] += 50
            self.robot.MoveCart(pos_6, self.tool_id, 0) # по Z на +50
            sleep(5)

        self.robot.SetToolPoint(self.step)
        _, pose = self.robot.GetActualTCPPose()
        print(f"{self.step} {pose2str(pose)}")
        self.calibration_points.append(pose)
        self.step += 1
        if self.step <= 6:
            self.ui.get_point.setText(f"Получить точку ({self.step}/6)")
        match self.step:
            case 4:
                self.ui.label.setEnabled(False)
                self.ui.label_2.setEnabled(True)
            case 5:
                self.ui.label_2.setEnabled(False)
                self.ui.label_3.setEnabled(True)
            case 6:
                self.ui.label_3.setEnabled(False)
                self.ui.label_4.setEnabled(True)
            case 7:
                self.ui.label_4.setEnabled(False)
                self.ui.get_point.setEnabled(False)
                self.ui.calibration_result.setEnabled(True)

    def get_calibration_result(self):
        points = {}
        for i, point in enumerate(self.calibration_points):
            points[i + 1] = point

        yaml_file = QFileDialog().getSaveFileName(self, "Сохранить точки калибровки", f"{DATA_DIR}/tcf_calibration.yaml", "*.yaml")
        with open(yaml_file[0], "w") as f:
            yaml.dump(points, f, default_flow_style=False)

        result = self.robot.ComputeTool()
        if result == 25:
            QMessageBox.critical(self, "Ошибка", "Ошибка калибрации!")
            return

        txt_file = QFileDialog().getSaveFileName(self, "Сохранить результаты калибровки", f"{CONFIG_DIR}/tcf.txt", "*.txt")

        with open(txt_file[0], "w") as f:
            f.write(f"{pose2str(result[1])[1:-1]}")

        self.close()
