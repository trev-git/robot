from ui.ip_window.ip_window import IPWindow
from PyQt6.QtWidgets import QApplication
from sys import argv
from utils import DATA_DIR, CONFIG_DIR
import os


def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    app = QApplication(argv)
    w = IPWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
