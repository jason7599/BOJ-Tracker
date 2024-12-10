from datetime import datetime

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QPushButton

from gui.widgets.submissiontable import SubmissionTable

from crawler.bojcrawler import boj_user_exists, boj_get_submissions

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
        submissions = boj_get_submissions('shhhhzzang', max_cnt=10)
        self.submission_table.add_all(submissions)
    
    def refresh(self):
        self.submission_table.clear()
        print('refresh!')
        
