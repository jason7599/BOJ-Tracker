from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon

from common.bojsubmission import BOJSubmission

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

    def add(self, submission: BOJSubmission):
        row = [QStandardItem(str(elem)) for elem in [
            submission.username,
            submission.problem_title,
            submission.result_str,
            submission.submit_time
        ]]
        self.model().appendRow(row)

    # todo: probably exists a better method for adding multiple rows
    def add_all(self, submissions: list[BOJSubmission]):
        for submission in submissions:
            self.add(submission)
    
    def clear(self):
        self.model().clear()
        