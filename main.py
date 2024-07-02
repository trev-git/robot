from ui.ip_window.ip_window import IPWindow
from PyQt6.QtWidgets import QApplication
from sys import argv


def main():
    app = QApplication(argv)
    w = IPWindow()
    w.show()
    app.exec()


if __name__ == '__main__':
    main()
