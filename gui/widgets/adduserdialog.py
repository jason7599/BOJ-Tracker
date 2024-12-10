from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLineEdit

UI_PATH = "gui/ui/add_user_dialog.ui"

WINDOW_TITLE = "Add User"

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loadUi(UI_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)
        self.setModal(True) # block interaction with other elems

        self.input_field = self.findChild(QLineEdit, 'input_field')
    
    def get_username(self):
        return self.input_field.text()