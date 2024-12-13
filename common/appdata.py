from dataclasses import dataclass
from datetime import datetime

from common.bojsubmission import BOJSubmission

@dataclass
class AppData:

    INTERVAL_OPTIONS = [5, 10, 15, 30, 60] # seconds. obviously.

    DEFAULT_INTERVAL_IDX = 4

    last_updated: datetime
    do_autorefresh: bool
    update_interval_idx: int
    usernames: list[str]
    submissions: list[BOJSubmission]
    # TODO: max_history

    @classmethod
    def empty(cls):
        return AppData(
            last_updated=datetime.now().replace(microsecond=0),
            do_autorefresh=False,
            update_interval_idx=cls.DEFAULT_INTERVAL_IDX,
            usernames=[],
            submissions=[],
        )
    
    @staticmethod
    def from_json(json):
        return AppData(
            last_updated=datetime.fromisoformat(json['last_updated']),
            do_autorefresh=json['autorefresh'],
            update_interval_idx=int(json['update_interval_idx']),
            usernames=json['usernames'],
            submissions=[BOJSubmission.from_json(j) for j in json['submissions']],
        )
    
    def to_json(self):
        return {
            'last_updated': self.last_updated.isoformat(),
            'autorefresh': self.do_autorefresh,
            'update_interval_idx': self.update_interval_idx,
            'usernames': self.usernames,
            'submissions': [submission.to_json() for submission in self.submissions],
        }
