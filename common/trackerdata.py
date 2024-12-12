from dataclasses import dataclass
from datetime import datetime

from common.bojsubmission import BOJSubmission

DEFAULT_UPDATE_INTERVAL = 5

@dataclass
class TrackerData:
    last_updated: datetime
    update_interval_seconds: int
    usernames: list[str]
    submissions: list[BOJSubmission]
    # TODO: max_history

    @staticmethod
    def empty():
        return TrackerData(
            last_updated=datetime.now().replace(microsecond=0),
            update_interval_seconds=DEFAULT_UPDATE_INTERVAL,
            usernames=[],
            submissions=[],
        )
    
    @staticmethod
    def from_json(json):
        return TrackerData(
            last_updated=datetime.fromisoformat(json['last_updated']),
            update_interval_seconds=int(json['update_interval_seconds']),
            usernames=json['usernames'],
            submissions=[BOJSubmission.from_json(j) for j in json['submissions']],
        )
    
    def to_json(self):
        return {
            'last_updated': self.last_updated.isoformat(),
            'update_interval_seconds': self.update_interval_seconds,
            'usernames': self.usernames,
            'submissions': [submission.to_json() for submission in self.submissions],
        }
