from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel

import common.datastore

from gui.widgets.usernameitem import UsernameItem

# TODO: prettier entries
class UsernameList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # disable edit
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_usernames()
        
    def add_username(self, username: str):
        item = QListWidgetItem()
        self.addItem(item)

        username_item = UsernameItem(username, self)
        item.setSizeHint(username_item.sizeHint())
        
        self.setItemWidget(item, username_item)

    def load_usernames(self):
        for username in common.datastore.tracker_data.usernames:
            self.add_username(username)