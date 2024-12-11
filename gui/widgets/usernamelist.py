from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

from gui.widgets.usernameitem import UsernameItem

# TODO: prettier entries
class UsernameList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # disable edit
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
    def add_username_item(self, username: str):
        item = QListWidgetItem()
        self.addItem(item)

        username_item = UsernameItem(username,
                                     on_remove=lambda: self.takeItem(self.row(item)),
                                     on_clicked=lambda: print("hi"),
                                     parent=self)
        
        item.setSizeHint(username_item.sizeHint())

        self.setItemWidget(item, username_item)