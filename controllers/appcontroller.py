from PyQt5.QtCore import QObject, pyqtSignal

import crawler.bojcrawler as BOJCrawler

import common.datastore as DataStore
from common.appdata import AppData
from common.bojsubmission import BOJSubmission

class AppController(QObject):
    # signals
    sig_username_added = pyqtSignal(str)
    sig_submissions_added = pyqtSignal(list)
    sig_submissions_changed = pyqtSignal(list)
    sig_error = pyqtSignal(str, str)
    sig_refresh_options_loaded = pyqtSignal(bool, list, int)

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.appdata = DataStore.get_appdata()

    def finalize(self):
        DataStore.write_appdata(self.appdata)
    
    # populate gui elements (submission table, username list) after gui initialized
    def on_gui_init(self):
        for username in self.appdata.usernames:
            self.sig_username_added.emit(username)
        self.sig_submissions_added.emit(self.appdata.submissions)

        self.sig_refresh_options_loaded.emit(
            self.appdata.do_autorefresh,
            self.appdata.INTERVAL_OPTIONS,
            self.appdata.update_interval_idx
        )

    def set_autorefresh(self, b: bool):
        self.appdata.do_autorefresh = b


    def set_refresh_interval(self, idx: int):
        new_interval = self.appdata.INTERVAL_OPTIONS[idx]
        if self.appdata.update_interval_idx != idx: #  inevitably gets called on init due to sig_refresh_options_loaded 
            self.appdata.update_interval_idx = idx

    def add_username(self, username: str):
        if username in self.appdata.usernames:
            self.sig_error.emit("Username Already Listed", f"Username {username} is already on the list!")
            return
        
        if not BOJCrawler.user_exists(username):
            self.sig_error.emit("Username Not Found", f"Username {username} was not found!")
            return

        self.appdata.usernames.append(username) # TODO: sort?
        self.sig_username_added.emit(username)
    
    # horribly unoptimized.. maybe not. runs pretty fast ngl
    def remove_username(self, username: str):
        self.appdata.usernames.remove(username)

        self.appdata.submissions = [
            submission for submission in self.appdata.submissions
            if submission.username != username
        ]

        self.sig_submissions_changed.emit(self.appdata.submissions)

    # TODO: in desperate need of threading.
    def update_submissions(self, show_error_message_box=True):
        try:
            new_submissions = BOJCrawler.get_submissions(self.appdata.usernames, self.appdata.last_updated)
        except Exception as e:
            if show_error_message_box:
                self.sig_error.emit("Failed to fetch submissions!", str(e))

            # TODO: stop refresh timer to prevent harassing user with QMessageBoxes
            return
        
        # self.tracker_data.last_updated = datetime.now() #TODO: TEMP DISABLED FOR DEBUG
        self.appdata.submissions = new_submissions + self.appdata.submissions 
        self.sig_submissions_added.emit(new_submissions)
    