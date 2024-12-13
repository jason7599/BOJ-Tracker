import sys
from PyQt5.QtWidgets import QApplication

from controllers.appcontroller import AppController
from gui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)

    controller = AppController()

    window = MainWindow(controller)
    window.show()

    exit_code = app.exec_()
    
    controller.write_appdata()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()