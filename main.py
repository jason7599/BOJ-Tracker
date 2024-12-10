import sys
from PyQt5.QtWidgets import QApplication

import gui.mainwindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = gui.mainwindow.MainWindow()
    window.show()

    sys.exit(app.exec_())