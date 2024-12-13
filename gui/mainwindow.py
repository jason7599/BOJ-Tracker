from datetime import datetime

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QMessageBox, QLabel, 
    QComboBox, QCheckBox, QLCDNumber
)
from PyQt5.QtCore import Qt

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
        self.refresh_button.clicked.connect(self.controller.start_crawling)

        self.controller.sig_crawling_started.connect(
            lambda: self.refresh_button.setEnabled(False)
        )
        self.controller.sig_crawling_finished.connect(
            lambda: self.refresh_button.setEnabled(True)
        )

        self.username_list = self.findChild(UsernameList, 'username_list')

        # i despise this but i see no other way. I can't use ctor because it's linked thru the ui file.
        # well it works, so let it be
        self.username_list.controller = self.controller 
        self.controller.sig_username_added.connect(self.username_list.add_username_item)

        self.add_user_button = self.findChild(QPushButton, 'add_user_button')
        self.add_user_button.clicked.connect(self.add_user_dialog)

        self.last_updated_label = self.findChild(QLabel, 'last_updated_label')

        self.auto_refresh_button = self.findChild(QCheckBox, 'auto_refresh_button')
        self.auto_refresh_button.stateChanged.connect(
            lambda state: self.set_autorefresh(state == Qt.CheckState.Checked)
        )

        self.interval_combo_box = self.findChild(QComboBox, 'interval_combo_box')
        self.interval_combo_box.currentIndexChanged.connect(self.controller.set_refresh_interval)

        self.refresh_countdown_display = self.findChild(QLCDNumber, 'refresh_countdown_display')
        # self.refresh_countdown_display.setNumDigits(2)
        self.controller.sig_countdown_update.connect(
            lambda val: self.refresh_countdown_display.display(val)
        )

        self.controller.sig_refresh_options_loaded.connect(self.set_refresh_options)

        self.controller.post_gui_init()

    def set_refresh_options(self, 
                            do_autorefresh: bool, 
                            interval_options: list[str], 
                            interval_idx: int,
                            last_updated: datetime):
        self.set_autorefresh(do_autorefresh)
        self.auto_refresh_button.setChecked(do_autorefresh)
        self.interval_combo_box.addItems([
            f"{t} seconds" for t in interval_options
        ])
        self.interval_combo_box.setCurrentIndex(interval_idx)
        self.last_updated_label.setText(
            "Last updated: " + str(last_updated.replace(microsecond=0))
        )

    def set_autorefresh(self, b):
        self.interval_combo_box.setEnabled(b)
        self.refresh_countdown_display.setEnabled(b)
        self.controller.set_autorefresh(b)

    
    def add_user_dialog(self):
        dialog = AddUserDialog(self)

        if dialog.exec_(): # returns True on QDialog.Accepted (= OK button), False on QDialog.Rejected (= Cancel Button)
            username = dialog.get_username().strip(' ')
            if username: # not empty
                self.controller.add_username(username)

    def show_error(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
    