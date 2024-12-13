from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox, QLabel, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QTimer

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
        self.controller.sig_error.connect(self.show_error)

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.submission_table = self.findChild(SubmissionTable, 'submission_table')
        self.controller.sig_submissions_added.connect(self.submission_table.add_all)
        self.controller.sig_submissions_changed.connect(self.submission_table.set_submissions)

        self.refresh_button = self.findChild(QPushButton, 'refresh_button')
        self.refresh_button.clicked.connect(self.controller.update_submissions)

        self.username_list = self.findChild(UsernameList, 'username_list')

        # i despise this but i see no other way. I can't use ctor because it's linked thru the ui file.
        # well it works, so let it be
        self.username_list.controller = self.controller 
        self.controller.sig_username_added.connect(self.username_list.add_username_item)

        self.add_user_button = self.findChild(QPushButton, 'add_user_button')
        self.add_user_button.clicked.connect(self.add_user_dialog)

        self.last_updated_label = self.findChild(QLabel, 'last_updated_label')

        self.auto_refresh_button = self.findChild(QCheckBox, 'auto_refresh_button')
        self.auto_refresh_button.stateChanged.connect(self.set_autorefresh)

        self.interval_combo_box = self.findChild(QComboBox, 'interval_combo_box')
        self.interval_combo_box.addItems([
            "5 seconds", "10 seconds", "15 seconds", "30 seconds", "60 seconds"
        ])

        self.refresh_timer = QTimer()
        # self.controller.sig_refresh_interval_set.connect(
            
        # )
        self.controller.on_gui_init()


    def set_autorefresh(self, state):
        if state == Qt.Checked:
            self.interval_combo_box.setEnabled(True)
        else:
            self.interval_combo_box.setEnabled(False)


    def add_user_dialog(self):
        dialog = AddUserDialog(self)

        if dialog.exec_(): # returns True on QDialog.Accepted (= OK button), False on QDialog.Rejected (= Cancel Button)
            username = dialog.get_username().strip(' ')
            if username: # not empty
                self.controller.add_username(username)

    def show_error(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
    