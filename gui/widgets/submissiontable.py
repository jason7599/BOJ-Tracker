from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QDesktopServices, QColorConstants

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

        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # auto resize columns to fit window
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # TODO: problem icon along problem_title
    # TODO: more readable submit_time
    # TODO: colored result_str
    def add_submission(self, submission: BOJSubmission):

        username_item = QStandardItem(submission.username)

        problem_item = QStandardItem(submission.problem_title)
        problem_item.setData(submission.problem_href, Qt.ItemDataRole.UserRole)
        problem_item.setData(QColorConstants.DarkCyan, Qt.ItemDataRole.ForegroundRole)
        problem_item.font().setUnderline(True)

        result_item = QStandardItem(submission.result.message)
        result_item.font().setBold(True)
        result_item.setData(submission.result.type.display_color, Qt.ItemDataRole.ForegroundRole) 

        time_item = QStandardItem(str(submission.submit_time))

        self.model().insertRow(0,
        [
            username_item,
            problem_item,
            result_item,
            time_item
        ])

    # TODO: probably exists a better method for adding multiple rows
    def add_all(self, submissions: list[BOJSubmission]):
        for submission in submissions:
            self.add_submission(submission)
    
    def clear(self):
        self.model().clear()
        self.model().setHorizontalHeaderLabels(COLUMN_LABELS) # TODO: stupid

    # clears the list and updates the view. 
    # TODO: screaming for optimization...
    def set_submissions(self, submissions: list[BOJSubmission]):
        self.clear()
        self.add_all(submissions)

    # open link
    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())

        if index.isValid() and COLUMN_LABELS[index.column()] == "Problem": # kinda shitty
            href = index.data(Qt.ItemDataRole.UserRole)
            QDesktopServices.openUrl(QUrl(href))

        return super().mousePressEvent(event)