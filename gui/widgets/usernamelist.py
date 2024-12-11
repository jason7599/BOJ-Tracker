from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel

import common.datastore

# TODO: prettier entries
class UsernameList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # disable edit
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_usernames()
        
    def add_username(self, username: str):
        self.addItem(QListWidgetItem(username))

    def load_usernames(self):
        for username in common.datastore.tracker_data.usernames:
            self.add_username(username)