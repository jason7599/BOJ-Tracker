import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow

from common.datahandler import load_tracker_data, write_tracker_data

def main():
    app = QApplication(sys.argv)

    tracker_data = load_tracker_data()

    window = MainWindow()
    window.show()

    exit_code = app.exec_()

    write_tracker_data(tracker_data)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()