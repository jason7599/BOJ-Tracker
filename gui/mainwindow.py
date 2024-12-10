from datetime import datetime

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QPushButton

from gui.widgets.submissiontable import SubmissionTable

UI_PATH = "gui/ui/main.ui"

WINDOW_TITLE = "BOJ Tracker"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.submission_table = self.findChild(SubmissionTable, 'submission_table')

        self.settings_button = self.findChild(QPushButton, 'settings_button')
        self.settings_button.clicked.connect(self.open_settings)

        self.refresh_button = self.findChild(QPushButton, 'refresh_button')
        self.refresh_button.clicked.connect(self.refresh)

    def open_settings(self):
        print('open_settings')
    
    def refresh(self):
        print('refresh!')
        
