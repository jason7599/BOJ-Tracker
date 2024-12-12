from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox

from controllers.appcontroller import AppController

from gui.widgets.submissiontable import SubmissionTable
from gui.widgets.adduserdialog import AddUserDialog
from gui.widgets.usernamelist import UsernameList

UI_PATH = "gui/ui/main.ui"

WINDOW_TITLE = "BOJ Tracker"

class MainWindow(QMainWindow):
    def __init__(self, controller: AppController, parent=None): # DI
        super().__init__(parent)

        self.controller = controller

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.submission_table = self.findChild(SubmissionTable, 'submission_table')

        self.settings_button = self.findChild(QPushButton, 'settings_button')
        self.settings_button.clicked.connect(self.open_settings)

        self.refresh_button = self.findChild(QPushButton, 'refresh_button')
        self.refresh_button.clicked.connect(self.refresh)

        self.username_list = self.findChild(UsernameList, 'username_list')
        self.username_list.controller = self.controller #..

        self.add_user_button = self.findChild(QPushButton, 'add_user_button')
        self.add_user_button.clicked.connect(self.add_user_dialog)

        self.controller.sig_username_added.connect(self.username_list.add_username_item)
        self.controller.sig_error.connect(self.show_error)

        self.controller.populate_gui()

    def open_settings(self):
        print('settings!')
    
    def refresh(self):
        print('refresh!')
    
    def add_user_dialog(self):
        dialog = AddUserDialog(self)

        if dialog.exec_(): # returns True on QDialog.Accepted (= OK button), False on QDialog.Rejected (= Cancel Button)
            username = dialog.get_username().strip(' ')
            if username: # not empty
                self.controller.add_username(username)

    def show_error(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
    