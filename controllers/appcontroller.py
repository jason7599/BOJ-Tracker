from PyQt5.QtCore import QObject, QTimer, pyqtSignal

import crawler.bojcrawler as BOJCrawler

import common.datastore as DataStore
from common.trackerdata import TrackerData
from common.bojsubmission import BOJSubmission

class AppController(QObject):
    # signals
    sig_username_added = pyqtSignal(str)
    sig_submissions_added = pyqtSignal(list)
    sig_error = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.tracker_data = DataStore.get_tracker_data()

    def finalize(self):
        DataStore.write_tracker_data(self.tracker_data)
    
    # populate gui elements (submission table, username list) after gui initialized
    # TODO: submissions table too
    def populate_gui(self):
        for username in self.tracker_data.usernames:
            self.sig_username_added.emit(username)

    def add_username(self, username: str):
        if username in self.tracker_data.usernames:
            self.sig_error.emit("Username Already Listed", f"Username {username} is already on the list!")
            return
        
        if not BOJCrawler.user_exists(username):
            self.sig_error.emit("Username Not Found", f"Username {username} was not found!")
            return

        self.tracker_data.usernames.append(username) # TODO: sort?
        self.sig_username_added.emit(username)
    
    def remove_username(self, username: str):
        self.tracker_data.usernames.remove(username)