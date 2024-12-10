from datetime import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel

UI_PATH = "gui/ui/main.ui"

WINDOW_TITLE = "BOJ Tracker"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.submissions_tbl = self.findChild(QTableView, 'submissions_list')

        self.tbl_model = QStandardItemModel(0, 4)
        self.tbl_model.setHorizontalHeaderLabels(["Username", "Problem", "Result", "Time"])
        
        self.submissions_tbl.setModel(self.tbl_model)
        self.submissions_tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # disable editing

        # auto-resize columns to fit window
        self.submissions_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_submission("shhhhzang", "eating assage", "wrong!", datetime.now())

    def add_submission(self, username: str, problem_title: str, result: str, time: datetime):
        row = [
            QStandardItem(username),
            QStandardItem(problem_title),
            QStandardItem(result),
            QStandardItem(str(time))
        ]
        self.tbl_model.appendRow(row)

