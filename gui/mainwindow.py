from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QMessageBox, QLabel, 
    QComboBox, QCheckBox, QLCDNumber,
    QSystemTrayIcon, QApplication, QMenu
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from controllers.appcontroller import AppController

from common.bojsubmission import BOJSubmission

from gui.widgets.submissiontable import SubmissionTable
from gui.widgets.adduserdialog import AddUserDialog
from gui.widgets.usernamelist import UsernameList

UI_PATH = "gui/ui/main.ui"
TRAY_ICON_PATH = "resources/app_icon.png"
WINDOW_TITLE = "BOJ Tracker"
NOTIFICATION_DURATION_MS = 3000

class MainWindow(QMainWindow):
    def __init__(self, controller: AppController, parent=None): # DI
        super().__init__(parent)

        self.controller = controller
        self.controller.sig_error.connect(self.show_error)

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.submission_table = self.findChild(SubmissionTable, 'submission_table')
        self.controller.sig_submissions_added.connect(self.on_new_submissions)
        self.controller.sig_submissions_set.connect(self.submission_table.set_submissions)

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
        self.controller.sig_last_updated_changed.connect(
            lambda time: self.last_updated_label.setText(
                "Last updated: " + str(time.replace(microsecond=0))
            )
        )

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

        self.setup_tray_icon()

        self.controller.sig_refresh_options_loaded.connect(self.set_refresh_options)
        self.controller.post_gui_init()

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon(TRAY_ICON_PATH), QApplication.instance())
        self.tray_icon.setToolTip("BOJ Tracker")

        tray_menu = QMenu()
        quit_action = tray_menu.addAction("quit")
        quit_action.triggered.connect(QApplication.instance().quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def on_new_submissions(self, new_submissions: list[BOJSubmission]):
        self.submission_table.add_all(new_submissions)
        self.notify_new_submissions(new_submissions)

    def notify_new_submissions(self, new_submissions: list[BOJSubmission]):
        if len(new_submissions) > 0 and self.tray_icon:
            self.tray_icon.showMessage(
                "New Submissions!",
                f"{len(new_submissions)} new submissions fetched!",
                QSystemTrayIcon.MessageIcon.Information,
                NOTIFICATION_DURATION_MS
            )

    def set_refresh_options(self, 
                            do_autorefresh: bool, 
                            interval_options: list[str], 
                            interval_idx: int):
        self.set_autorefresh(do_autorefresh)
        self.auto_refresh_button.setChecked(do_autorefresh)
        self.interval_combo_box.addItems([
            f"{t} seconds" for t in interval_options
        ])
        self.interval_combo_box.setCurrentIndex(interval_idx)


    def set_autorefresh(self, b):
        self.interval_combo_box.setEnabled(b)
        self.refresh_countdown_display.setEnabled(b)
        self.controller.set_autorefresh(b)

    
    def add_user_dialog(self):
        dialog = AddUserDialog(self)

        if dialog.exec_(): # returns True on QDialog.Accepted (= OK button), False on QDialog.Rejected (= Cancel Button)
            username = dialog.get_username().strip(' ')
            if username: # not empty
                self.controller.add_user(username)

    def show_error(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
    