from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QCheckBox, QSpinBox
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

from common.appsettings import AppSettings

UI_PATH = "gui/ui/settings_dialog.ui"

WINDOW_TITLE = "Settings"

class SettingsDialog(QDialog):
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

    # override enter/return key events to stop them closing the dialog.
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            return
        return super().keyPressEvent(event)
    
    # can't use `=` statement as a lambda. 
    def set_notify_new_submissions(self, b: bool):
        self.settings.notify_new_submissions = b
