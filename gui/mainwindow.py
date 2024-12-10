from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListView, QMessageBox

from gui.widgets.submissiontable import SubmissionTable
from gui.widgets.adduserdialog import AddUserDialog
from gui.widgets.usernamelist import UsernameList

import common.datastore

from crawler.bojcrawler import boj_user_exists, boj_get_submissions

UI_PATH = "gui/ui/main.ui"

WINDOW_TITLE = "BOJ Tracker"

# TODO: populate mainwindow widgets (submissiontable, userlistview)
class MainWindow(QMainWindow):
    def __init__(self, ):
        super().__init__()

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.submission_table = self.findChild(SubmissionTable, 'submission_table')

        self.username_list = self.findChild(UsernameList, 'username_list')
        
        self.settings_button = self.findChild(QPushButton, 'settings_button')
        self.settings_button.clicked.connect(self.open_settings)

        self.refresh_button = self.findChild(QPushButton, 'refresh_button')
        self.refresh_button.clicked.connect(self.refresh)

        self.add_user_button = self.findChild(QPushButton, 'add_user_button')
        self.add_user_button.clicked.connect(self.open_add_user_popup)


    def open_settings(self):
        submissions = boj_get_submissions('shhhhzzang', max_cnt=20)
        self.submission_table.add_all(submissions)
    
    def refresh(self):
        self.submission_table.clear()
        print('refresh!')
    
    def open_add_user_popup(self):
        dialog = AddUserDialog(self)
        if dialog.exec_(): # returns True on QDialog.Accepted (= OK button), False on QDialog.Rejected (= Cancel Button)
            username = dialog.get_username().strip(' ')
            if not username: # empty
                return
            
            if boj_user_exists(username):
                if self.username_list.is_username_listed(username):
                    self.show_error("Username Already Listed", f"Username {username} is already on the list!")
                else:
                    self.add_username(username)
            else:
                self.show_error("Username Not Found", f"Username {username} was not found!")

    def add_username(self, username):
        common.datastore.tracker_data.usernames.append(username)
        self.username_list.add_username(username)

    def show_error(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
    