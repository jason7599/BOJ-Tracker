from datetime import datetime
from copy import deepcopy

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread

import common.datastore as DataStore
from common.userinfo import UserInfo
from common.bojsubmission import BOJSubmission
import crawler.bojcrawler as BOJCrawler 
from crawler.crawlerworker import CrawlerWorker

class AppController(QObject):
    # signals
    sig_username_added = pyqtSignal(str)
    sig_submissions_added = pyqtSignal(list)
    sig_submissions_set = pyqtSignal(list)
    sig_error = pyqtSignal(str, str)
    sig_refresh_options_loaded = pyqtSignal(bool, list, int)
    sig_crawling_started = pyqtSignal()
    sig_crawling_finished = pyqtSignal()
    sig_countdown_update = pyqtSignal(int)
    sig_last_updated_changed = pyqtSignal(datetime)

    def __init__(self):
        super().__init__()

        self.appdata = DataStore.get_appdata()

        self.crawler_worker: CrawlerWorker = None
        self.crawler_thread: QThread = None

        self.autorefresh_error = False

        self.countdown_timer = QTimer()
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.countdown)

    # populate gui elements (submission table, username list) after gui initialized
    def post_gui_init(self):
        for user_info in self.appdata.user_infos:
            self.sig_username_added.emit(user_info.username)
        self.sig_submissions_set.emit(self.appdata.submissions)

        self.sig_refresh_options_loaded.emit(
            self.appdata.settings.do_autorefresh,
            self.appdata.settings.INTERVAL_OPTIONS,
            self.appdata.settings.update_interval_idx
        )

        self.sig_last_updated_changed.emit(self.appdata.last_updated)

        self.set_refresh_countdown(self.get_selected_interval())
        if self.appdata.settings.do_autorefresh and len(self.appdata.user_infos) > 0:
            self.countdown_timer.start()

    def start_crawling(self):

        if self.crawler_thread and self.crawler_thread.isRunning():
            print("crawler thread already running!")
            return
        
        self.countdown_timer.stop()

        self.sig_crawling_started.emit()

        self.crawler_worker = CrawlerWorker()
        self.crawler_thread = QThread()
        self.crawler_worker.moveToThread(self.crawler_thread)

        self.crawler_worker.sig_done.connect(self.on_crawling_finished)
        self.crawler_worker.sig_error.connect(self.on_crawling_error)

        self.crawler_thread.started.connect(
            lambda: self.crawler_worker.crawl(
                self.appdata.user_infos, 
                self.appdata.last_updated
            )
        )
        self.crawler_thread.finished.connect(self.crawler_worker.deleteLater)

        self.crawler_thread.start()

    def on_crawling_finished(self, new_submissions: list[BOJSubmission]):
        
        self.cleanup_crawler_thread()

        self.autorefresh_error = False

        if len(new_submissions) > 0:
            self.appdata.submissions.extend(new_submissions)
            self.sig_submissions_added.emit(new_submissions) # submissions get appended to the submissions_table

        self.appdata.last_updated = datetime.now()
        self.sig_last_updated_changed.emit(datetime.now())

        self.reset_timer()
        self.sig_crawling_finished.emit()

    def on_crawling_error(self, e: Exception):
        
        self.cleanup_crawler_thread()

        if not self.autorefresh_error:
            self.autorefresh_error = True
            self.sig_error.emit("Failed to fetch submissions!", str(e)) # show error box in mainwindow

        self.sig_crawling_finished.emit()

    def cleanup_crawler_thread(self):
        if self.crawler_thread:
            if self.crawler_worker:
                self.crawler_worker.deleteLater()
                self.crawler_worker = None
            self.crawler_thread.quit()
            self.crawler_thread.wait()
            self.crawler_thread = None

    def get_selected_interval(self):
        return self.appdata.settings.INTERVAL_OPTIONS[self.appdata.settings.update_interval_idx]
    
    def reset_timer(self):
        self.set_refresh_countdown(self.get_selected_interval())
        if self.appdata.settings.do_autorefresh and len(self.appdata.user_infos) > 0:
            self.countdown_timer.start()

    def countdown(self):
        t = self.refresh_countdown - 1
        self.set_refresh_countdown(t)
        if t <= 0:
            if t < 0:
                print("HOW THE FUCK")
            self.start_crawling()

    def set_refresh_countdown(self, val: int):
        self.refresh_countdown = val
        self.sig_countdown_update.emit(val)

    def set_autorefresh(self, b: bool):
        self.appdata.settings.do_autorefresh = b
        if not b:
            self.countdown_timer.stop()
        elif len(self.appdata.user_infos) > 0:
            self.countdown_timer.start()

    def set_refresh_interval(self, idx: int):
        if self.appdata.settings.update_interval_idx != idx: #  inevitably gets called on init due to sig_refresh_options_loaded 
            self.countdown_timer.stop()
            self.appdata.settings.update_interval_idx = idx
            self.reset_timer()

    def add_user(self, username: str):
        # shitty
        for user_info in self.appdata.user_infos:
            if user_info.username == username:
                self.sig_error.emit("Username Already Listed", f"Username {username} is already on the list!")
                return
        
        if not BOJCrawler.user_exists(username): # TODO: single thread
            self.sig_error.emit("Username Not Found", f"Username {username} was not found!")
            return

        self.appdata.user_infos.append(UserInfo(username, -1))
        self.sig_username_added.emit(username)
        
        if len(self.appdata.user_infos) == 1:
            self.reset_timer()

    def get_settings(self):
        return deepcopy(self.appdata.settings)
    
    def settings_changed(self, settings):
        self.appdata.settings = settings

    def pause_timer(self):
        self.countdown_timer.stop()

    def resume_timer(self):
        if self.appdata.settings.do_autorefresh and len(self.appdata.user_infos) > 0:
            self.countdown_timer.start()

    def clear_submissions(self):
        self.appdata.submissions.clear()
        self.sig_submissions_set.emit([])
    
    # horribly unoptimized.. maybe not. runs pretty fast ngl
    def remove_username(self, username: str):
        for user_info in self.appdata.user_infos:
            if user_info.username == username:
                self.appdata.user_infos.remove(user_info)
                break

        if len(self.appdata.user_infos) == 0:
            self.countdown_timer.stop()
            self.reset_timer()

        self.appdata.submissions = [
            submission for submission in self.appdata.submissions
            if submission.username != username
        ]

        self.sig_submissions_set.emit(self.appdata.submissions)

    def write_appdata(self):
        DataStore.write_appdata(self.appdata)
