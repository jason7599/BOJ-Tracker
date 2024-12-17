from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

UI_PATH = "gui/ui/settings_dialog.ui"

WINDOW_TITLE = "Settings"

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)
        self.setModal(True)