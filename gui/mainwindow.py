from datetime import datetime

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from gui.widgets.submissiontable import SubmissionTable

UI_PATH = "gui/ui/main.ui"

WINDOW_TITLE = "BOJ Tracker"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        # promoted to SubmissionTable class
        self.submission_table = self.findChild(QTableView, 'submission_table')
        
