import numpy as np
from PyQt6.QtWidgets import QWidget, QFileDialog
from .workspace_calibration_ui import Ui_WorkspaceCalibration
from utils import CONFIG_DIR, pose2str, DATA_DIR
import yaml
import sys
sys.path.append('C:\\FAIRINO\\PythonSDK\\windows\\libfairino\\akai-x64-windows-python3.10')
from pyakai import tf3d
from scipy.spatial.transform import Rotation
from .icp import icp_solver_svd


class WorkspaceCalibration(QWidget):
    def __init__(self, robot, tool_id):
        super(WorkspaceCalibration, self).__init__()
        self.ui = Ui_WorkspaceCalibration()
        self.ui.setupUi(self)
        self.setWindowTitle('Калибровка рабочего пространства')

        self.robot = robot
        self.tool_id = tool_id
        self.tool_tcf = np.loadtxt(f'{CONFIG_DIR}/tcf.txt', delimiter=',')
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
        if self.step == 1:
            self.ui.auto_point.setEnabled(True)
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
        _, pose = self.robot.GetActualTCPPose()
        for i in range(2, 5):
            if i == 2:
                pose[1] -= self.w
            elif i == 3:
                pose[0] -= self.h
            elif i == 4:
                pose[1] += self.w
            self.current_ws_points[i] = pose[:]

        print(self.current_ws_points)
        self.ui.get_calibration_result.setEnabled(True)
        self.ui.get_point.setEnabled(False)

    def get_calibration_result(self):
        yaml_file = QFileDialog().getSaveFileName(self, "Сохранить точки рабочего пространства", f"{DATA_DIR}/workspace_calibration.yaml", "*.yaml")
        with open(f'{yaml_file[0]}', 'w') as f:
            yaml.dump(self.current_ws_points, f, default_flow_style=False)

        points_arm = np.float64([self.current_ws_points[i] for i in range(1, 5)])[:, :3]
        if self.ui.parallel.isChecked():
            z_mean = np.mean(points_arm[:, 2])
            points_arm[:, 2] = z_mean

        points_ws = np.float64([self.points_ws_dict[i] for i in range(1, 5)])
        R, t = icp_solver_svd(points_arm, points_ws)
        print(f'{points_ws=}\n{points_arm=}')
        t_mm = t.reshape(-1)
        print(f'{t_mm=}')
        # R_4 = np.eye(4)
        # R_4[:3, :3] = R
        # print(R_4)
        # euler_angle_rad = tf3d.RotationMatrix2EulerAngle(R_4)
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
