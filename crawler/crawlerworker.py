from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal

from common.userinfo import UserInfo
from common.bojsubmission import BOJSubmission
import crawler.bojcrawler as BOJCrawler

class CrawlerWorker(QObject):

    sig_done = pyqtSignal(list) # return list of new submissions
    sig_error = pyqtSignal(Exception)

    def __init__(self):
        super().__init__()
    
    # TODO! Optimize
    def crawl(self, user_infos: list[UserInfo], last_updated: datetime):
        try:
            res: list[BOJSubmission] = []
            for user_info in user_infos:
                submissions = BOJCrawler.get_user_submissions(user_info, last_updated)
                if len(submissions) > 0:
                    user_info.last_submit_id = submissions[0].submit_id
                    res.extend(submissions)

            res.sort(key=lambda x: x.submit_time)# reverse=True)
            self.sig_done.emit(res)
        except Exception as e:
            self.sig_error.emit(e)
        
