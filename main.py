import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow

import common.datastore


def load_data():
    from common.datahandler import load_tracker_data

    common.datastore.tracker_data = load_tracker_data()

def write_data():
    from common.datahandler import write_tracker_data

    write_tracker_data(common.datastore.tracker_data)


def main():
    load_data()

    print("init done")

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    exit_code = app.exec_()

    write_data()

    print("cleanup done")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()