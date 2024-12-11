import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow

from common.datastore import DataStore

def main():
    DataStore.initialize()
    print("init done")

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    exit_code = app.exec_()

    DataStore.finalize()
    print("cleanup done")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()