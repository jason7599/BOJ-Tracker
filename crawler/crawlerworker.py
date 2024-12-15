from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal

import crawler.bojcrawler as BOJCrawler

class CrawlerWorker(QObject):

    sig_done = pyqtSignal(list) # return list of new submissions
    sig_error = pyqtSignal(Exception)

    def __init__(self):
        super().__init__()
    
    def crawl(self, usernames: list[str], last_updated: datetime):
        try:
            submissions = BOJCrawler.get_submissions(usernames, last_updated)
            self.sig_done.emit(submissions)
        except Exception as e:
            self.sig_error.emit(e)
        
