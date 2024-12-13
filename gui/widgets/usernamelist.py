from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout,
    QListWidget, QListWidgetItem, QAbstractItemView
)

from controllers.appcontroller import AppController

class UsernameList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.controller: AppController = None
        # disable edit
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def add_username_item(self, username: str):
        item = QListWidgetItem()
        self.addItem(item)

        username_item = self.UsernameItem(username, self)
        username_item.remove_button.clicked.connect(
            lambda: self.handle_remove_username(username, item)
        )
        
        item.setSizeHint(username_item.sizeHint())

        self.setItemWidget(item, username_item)
    
    def handle_remove_username(self, username:str, item: QListWidgetItem):
        self.controller.remove_username(username)
        self.takeItem(self.row(item))

    class UsernameItem(QWidget):
        def __init__(self, username: str, parent):
            super().__init__(parent)

            self.username_label = QLabel(username, self)
            self.remove_button = QPushButton('remove', self)

            layout = QHBoxLayout(self)
            layout.addWidget(self.username_label)
            layout.addWidget(self.remove_button)

            self.setLayout(layout)