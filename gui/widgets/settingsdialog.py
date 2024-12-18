from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from common.appsettings import AppSettings

UI_PATH = "gui/ui/settings_dialog.ui"

WINDOW_TITLE = "Settings"

class SettingsDialog(QDialog):

    sig_clear_submissions = pyqtSignal()

    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)

        self.settings = settings

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)
        self.setModal(True)

        self.notification_checkbox = self.findChild(QCheckBox, 'notification_checkbox')
        self.notification_checkbox.setChecked(self.settings.notify_new_submissions)

        self.notification_checkbox.stateChanged.connect(
            lambda state: self.set_notify_new_submissions(state == Qt.CheckState.Checked)
        )

        self.clear_submissions_button = self.findChild(QPushButton, 'clear_submissions_button')
        self.clear_submissions_button.clicked.connect(self.on_clear_button_clicked)
    
    # can't use `=` statement as a lambda. 
    def set_notify_new_submissions(self, b: bool):
        self.settings.notify_new_submissions = b

    def on_clear_button_clicked(self):
        if QMessageBox.warning(
            self,
            'Confirm',
            'Clear all submissions?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.sig_clear_submissions.emit()