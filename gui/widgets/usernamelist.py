from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItem, QStandardItemModel

# TODO: prettier entries
class UsernameList(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))

    def is_username_listed(self, username: str) -> bool:
        for i in range(self.model().rowCount()):
            if self.model().item(i).text() == username:
                return True
        return False

    def add_username(self, username: str):
        self.model().appendRow(QStandardItem(username))