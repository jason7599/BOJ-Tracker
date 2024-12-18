from dataclasses import dataclass

@dataclass
class AppSettings:

    INTERVAL_OPTIONS = [5, 10, 15, 30, 60] # seconds. obviously.

    DEFAULT_INTERVAL_IDX = 4

    MIN_SUBMISSIONS_LIMIT = 30
    MAX_SUBMISSIONS_LIMIT = 1000

    DEFAULT_SUBMISSIONS_LIMIT = 250

    do_autorefresh: bool
    update_interval_idx: int

    notify_new_submissions: bool
    submissions_limit: int

    @classmethod
    def default(cls):
        return AppSettings(
            do_autorefresh=False,
            update_interval_idx=cls.DEFAULT_INTERVAL_IDX,
            notify_new_submissions=True,
            submissions_limit=cls.DEFAULT_SUBMISSIONS_LIMIT
        )
    
    @staticmethod
    def from_json(json):
        return AppSettings(
            do_autorefresh=json['autorefresh'],
            update_interval_idx=int(json['update_interval_idx']),
            notify_new_submissions=json['notification'],
            submissions_limit=int(json['submissions_limit'])
        )
    
    def to_json(self):
        return {
            'autorefresh': self.do_autorefresh,
            'update_interval_idx': self.update_interval_idx,
            'notification': self.notify_new_submissions,
            'submissions_limit': self.submissions_limit
        }
    