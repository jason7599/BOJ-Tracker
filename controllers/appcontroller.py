from datetime import datetime
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

import crawler.bojcrawler as BOJCrawler

import common.datastore as DataStore
from common.trackerdata import TrackerData
from common.bojsubmission import BOJSubmission

class AppController(QObject):
    # signals
    sig_username_added = pyqtSignal(str)
    sig_submissions_added = pyqtSignal(list)
    sig_submissions_changed = pyqtSignal(list)
    sig_error = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.tracker_data = DataStore.get_tracker_data()

    def finalize(self):
        DataStore.write_tracker_data(self.tracker_data)
    
    # populate gui elements (submission table, username list) after gui initialized
    def populate_gui(self):
        for username in self.tracker_data.usernames:
            self.sig_username_added.emit(username)

        self.sig_submissions_added.emit(self.tracker_data.submissions)

    def add_username(self, username: str):
        if username in self.tracker_data.usernames:
            self.sig_error.emit("Username Already Listed", f"Username {username} is already on the list!")
            return
        
        if not BOJCrawler.user_exists(username):
            self.sig_error.emit("Username Not Found", f"Username {username} was not found!")
            return

        self.tracker_data.usernames.append(username) # TODO: sort?
        self.sig_username_added.emit(username)
    
    # TODO: horribly unoptimized
    def remove_username(self, username: str):
        self.tracker_data.usernames.remove(username)

        self.tracker_data.submissions = [
            submission for submission in self.tracker_data.submissions
            if submission.username != username
        ]

        self.sig_submissions_changed.emit(self.tracker_data.submissions)

    # TODO: in desperate need of threading.
    def update_submissions(self, show_error_message_box=True):
        try:
            new_submissions = BOJCrawler.get_submissions(self.tracker_data.usernames, self.tracker_data.last_updated)
            print(len(new_submissions), new_submissions)
        except Exception as e:
            if show_error_message_box:
                self.sig_error.emit("Failed to fetch submissions!", str(e))

            # TODO: stop refresh timer to prevent harassing user with QMessageBoxes
            return
        
        self.tracker_data.last_updated = datetime.now()
        self.tracker_data.submissions = new_submissions + self.tracker_data.submissions 
        self.sig_submissions_added.emit(new_submissions)
    