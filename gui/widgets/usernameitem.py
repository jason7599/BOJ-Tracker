from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

class UsernameItem(QWidget):
    def __init__(self, username: str, parent=None):
        super().__init__(parent)

        self.username_label = QLabel(username, self)
        
        self.remove_button = QPushButton('remove', self)

        layout = QHBoxLayout(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)