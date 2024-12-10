from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel

COLUMN_LABELS = ["Username", "Problem", "Result", "Time"]

class SubmissionTable(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        model = QStandardItemModel(0, len(COLUMN_LABELS))
        model.setHorizontalHeaderLabels(COLUMN_LABELS)

        self.setModel(model)
        
        # disable editing
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # auto resize columns to fit window
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)