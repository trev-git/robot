from PyQt6.QtWidgets import QDialog
from .workspace_dialog_ui import Ui_AutoPointDialog


class WorkspaceDialog(QDialog):
    def __init__(self, robot):
        super(WorkspaceDialog, self).__init__()
        self.ui = Ui_AutoPointDialog()
        self.ui.setupUi(self)

        self.robot = robot

        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)

    def accepted(self):
        self.angle = self.ui.rotation_angle.value()

    def rejected(self):
        self.close()
