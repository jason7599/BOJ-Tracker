from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

class UsernameItem(QWidget):
    def __init__(self, username: str, on_remove, on_clicked, parent):
        super().__init__(parent)

        self.username_label = QLabel(username, self)

        self.remove_button = QPushButton('remove', self)
        self.remove_button.clicked.connect(on_remove)

        layout = QHBoxLayout(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)