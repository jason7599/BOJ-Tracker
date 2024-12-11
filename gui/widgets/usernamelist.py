from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout,
    QListWidget, QListWidgetItem, QAbstractItemView
)

from common.datastore import DataStore

# TODO: prettier entries
class UsernameList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # disable edit
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
    def add_username_item(self, username: str):
        item = QListWidgetItem()
        self.addItem(item)

        username_item = self.UsernameItem(username, self)
        # username_item.remove_button.clicked.connect()

        item.setSizeHint(username_item.sizeHint())

        self.setItemWidget(item, username_item)

    # TODO: FIX THIS UGLY SHIT
    def remove_item(self, row: int):
        del DataStore.tracker_data().usernames[row] # scary...
        self.takeItem(row)

    class UsernameItem(QWidget):
        def __init__(self, username: str, parent):
            super().__init__(parent)

            self.username_label = QLabel(username, self)
            self.remove_button = QPushButton('remove', self)

            layout = QHBoxLayout(self)
            layout.addWidget(self.username_label)
            layout.addWidget(self.remove_button)

            self.setLayout(layout)