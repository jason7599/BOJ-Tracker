from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListView, QMessageBox

from gui.widgets.submissiontable import SubmissionTable
from gui.widgets.adduserdialog import AddUserDialog
from gui.widgets.usernamelist import UsernameList

from crawler.bojcrawler import boj_user_exists, boj_get_submissions

from common.datastore import DataStore

UI_PATH = "gui/ui/main.ui"

WINDOW_TITLE = "BOJ Tracker"

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

        self.populate_data()

    def populate_data(self):
        for username in DataStore.tracker_data().usernames:
            self.username_list.add_username_item(username)
        # TODO: populate submission table

    def open_settings(self):
        print('settings!')
    
    def refresh(self):
        submissions = boj_get_submissions(DataStore.tracker_data().usernames)
        self.submission_table.add_all(submissions)
        print('refresh!')
    
    def open_add_user_popup(self):
        dialog = AddUserDialog(self)
        if dialog.exec_(): # returns True on QDialog.Accepted (= OK button), False on QDialog.Rejected (= Cancel Button)
            username = dialog.get_username().strip(' ')
            if not username: # empty
                return
            
            if boj_user_exists(username):
                if username in DataStore.tracker_data().usernames: # this is very slow
                    self.show_error("Username Already Listed", f"Username {username} is already on the list!")
                else:
                    DataStore.tracker_data().usernames.append(username)
                    self.username_list.add_username_item(username)
            else:
                self.show_error("Username Not Found", f"Username {username} was not found!")

    def show_error(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
    