from dataclasses import dataclass
from datetime import datetime

from common.bojsubmission import BOJSubmission

@dataclass
class TrackerData:
    last_updated: datetime
    do_autorefresh: bool
    update_interval_idx: int
    usernames: list[str]
    submissions: list[BOJSubmission]
    # TODO: max_history

    @staticmethod
    def empty():
        return TrackerData(
            last_updated=datetime.now().replace(microsecond=0),
            do_autorefresh=False,
            update_interval_idx=0,
            usernames=[],
            submissions=[],
        )
    
    @staticmethod
    def from_json(json):
        return TrackerData(
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
