from datetime import datetime

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread

import common.datastore as DataStore
from common.bojsubmission import BOJSubmission
import crawler.bojcrawler as BOJCrawler 
from crawler.crawlerworker import CrawlerWorker

class AppController(QObject):
    # signals
    sig_username_added = pyqtSignal(str)
    sig_submissions_added = pyqtSignal(list)
    sig_submissions_changed = pyqtSignal(list)
    sig_error = pyqtSignal(str, str)
    sig_refresh_options_loaded = pyqtSignal(bool, list, int, datetime)
    sig_crawling_started = pyqtSignal()
    sig_crawling_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.appdata = DataStore.get_appdata()

        self.crawler_worker: CrawlerWorker = None
        self.crawler_thread: QThread = None

        self.autorefresh_error = False

    def write_appdata(self):
        DataStore.write_appdata(self.appdata)
    
    # populate gui elements (submission table, username list) after gui initialized
    def post_gui_init(self):
        for username in self.appdata.usernames:
            self.sig_username_added.emit(username)
        self.sig_submissions_added.emit(self.appdata.submissions)

        self.sig_refresh_options_loaded.emit(
            self.appdata.do_autorefresh,
            self.appdata.INTERVAL_OPTIONS,
            self.appdata.update_interval_idx,
            self.appdata.last_updated
        )

        # TODO: initial scraping!

        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(self.appdata.INTERVAL_OPTIONS[self.appdata.update_interval_idx] * 1000)


    def start_crawling(self):

        if self.crawler_thread and self.crawler_thread.isRunning():
            print("crawler thread already running!")
            return

        self.sig_crawling_started.emit()

        self.crawler_worker = CrawlerWorker()
        self.crawler_thread = QThread()
        self.crawler_worker.moveToThread(self.crawler_thread)

        self.crawler_worker.sig_done.connect(self.on_crawling_finished)
        self.crawler_worker.sig_error.connect(self.on_crawling_error)

        self.crawler_thread.started.connect(
            lambda: self.crawler_worker.crawl(self.appdata.usernames)
        )
        self.crawler_thread.finished.connect(self.crawler_worker.deleteLater)

        self.crawler_thread.start()

    def on_crawling_finished(self, new_submissions: list[BOJSubmission]):
        
        # TODO: reenable refresh button
        
        self.cleanup_crawler_thread()        

        self.autorefresh_error = False

        # TODO: Maybe these 2 lines are what should be done thru threads..
        self.appdata.submissions = self.appdata.submissions + new_submissions
        self.sig_submissions_added.emit(new_submissions)

        self.sig_crawling_finished.emit()

    def on_crawling_error(self, e: Exception):
        
        self.cleanup_crawler_thread()

        if not self.autorefresh_error:
            self.sig_error.emit("Failed to fetch submissions!", str(e)) # show error box in mainwindow

        # TODO: stop refresh timer to prevent harassing user with QMessageBoxes

    def cleanup_crawler_thread(self):
        if self.crawler_thread:
            if self.crawler_worker:
                self.crawler_worker.deleteLater()
                self.crawler_worker = None
            self.crawler_thread.quit()
            self.crawler_thread.wait()
            self.crawler_thread = None

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
        
        if not BOJCrawler.user_exists(username): # TODO: single thread
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
