from math import cos, sin
import numpy as np
from PyQt6.QtWidgets import QWidget, QFileDialog
from scipy.spatial.transform import Rotation
import yaml
from .icp import icp_solver_svd
from utils import CONFIG_DIR, pose2str, DATA_DIR
from .workspace_calibration_ui import Ui_WorkspaceCalibration
from .workspace_dialog import WorkspaceDialog


class WorkspaceCalibration(QWidget):
    def __init__(self, robot, tool_id, tool_tcf_file):
        super(WorkspaceCalibration, self).__init__()
        self.ui = Ui_WorkspaceCalibration()
        self.ui.setupUi(self)
        self.setWindowTitle('Калибровка рабочего пространства')

        self.robot = robot
        self.tool_id = tool_id
        self.tool_tcf = np.loadtxt(tool_tcf_file, delimiter=',')

        self.w = 0
        self.h = 0
        self.step = 1
        self.points_ws_dict = {
            1: [0,      0,      0],
            2: [0,      self.w, 0],
            3: [self.h, self.w, 0],
            4: [self.h, 0,      0]
        }
        self.current_ws_points = {}

        self.robot.SetToolCoord(self.tool_id, self.tool_tcf.tolist(), 0, 0)
        print(self.tool_tcf.tolist())
        self.ui.get_point.clicked.connect(self.get_point)
        self.ui.get_calibration_result.clicked.connect(self.get_calibration_result)
        self.ui.width.valueChanged.connect(self.change_starting_point)
        self.ui.height.valueChanged.connect(self.change_starting_point)
        self.ui.auto_point.clicked.connect(self.auto_get_point)

    def get_point(self):
        if self.step == 2:
            self.ui.auto_point.setEnabled(False)
        if self.step == 4:
            self.ui.get_calibration_result.setEnabled(True)
        _, pose = self.robot.GetActualTCPPose()
        self.current_ws_points[self.step] = pose
        self.step += 1
        if self.step <= 4:
            self.ui.get_point.setText(f"Получить точку ({self.step}/4)")

    def auto_get_point(self):
        dialog = WorkspaceDialog(self.robot)
        if not dialog.exec():
            return

        _, pose = self.robot.GetActualTCPPose()
        self.current_ws_points[1] = pose[:]
        for i in range(2, 5):
            if i == 2:
                pose[1] -= self.w
            elif i == 3:
                pose[0] -= self.h
            elif i == 4:
                pose[1] += self.w
            self.current_ws_points[i] = pose[:]

        origin = np.array(self.current_ws_points[1][:3])[:, np.newaxis]
        angle_rad = np.deg2rad(dialog.angle)
        # Повернуть все точки вокруг первой
        for i in range(2,5):
            cur = np.array(self.current_ws_points[i][:3])[:, np.newaxis]
            cur[0][0] -= origin[0][0]
            cur[1][0] -= origin[1][0]
            rotated_point = np.matmul([[cos(angle_rad), -sin(angle_rad), 0],
                                       [sin(angle_rad), cos(angle_rad),  0],
                                       [0,              0,               1]], cur)
            rotated_point[0][0] += origin[0][0]
            rotated_point[1][0] += origin[1][0]
            self.current_ws_points[i][:3] = rotated_point.flatten().tolist()

        self.ui.get_calibration_result.setEnabled(True)
        self.ui.get_point.setEnabled(False)

    def get_calibration_result(self):
        yaml_file = QFileDialog().getSaveFileName(self, "Сохранить точки рабочего пространства", f"{DATA_DIR}/workspace_calibration.yaml", "*.yaml")
        with open(f'{yaml_file[0]}', 'w') as f:
            yaml.dump(self.current_ws_points, f, default_flow_style=False)

        points_arm = np.float64([self.current_ws_points[i] for i in range(1, 5)])[:, :3]
        z_mean = np.mean(points_arm[:, 2])
        points_arm[:, 2] = z_mean

        points_ws = np.float64([self.points_ws_dict[i] for i in range(1, 5)])
        R, t = icp_solver_svd(points_arm, points_ws)
        t_mm = t.reshape(-1)
        euler_angle_rad = Rotation.from_matrix(R).as_euler("xyz")
        euler_angle_deg = np.degrees(euler_angle_rad)
        pose_base2ws = np.hstack((t_mm, euler_angle_deg))

        txt_file = QFileDialog().getSaveFileName(self, "Сохранить результаты калибровки", f'{CONFIG_DIR}/pose_base2ws.txt', "*.txt")
        with open(txt_file[0], 'w') as f:
            f.write(pose2str(pose_base2ws)[1:-1])

        self.close()

    def change_starting_point(self, value):
        self.w = self.ui.width.value()
        self.h = self.ui.height.value()
        self.points_ws_dict = {
            1: [0,      0,      0],
            2: [0,      self.w, 0],
            3: [self.h, self.w, 0],
            4: [self.h, 0,      0]
        }
