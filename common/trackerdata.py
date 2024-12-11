from dataclasses import dataclass
from datetime import datetime

DEFAULT_UPDATE_INTERVAL = 5

@dataclass
class TrackerData:
    last_updated: datetime
    update_interval_seconds: int
    usernames: list[str]

    @staticmethod
    def empty():
        return TrackerData(
            last_updated=datetime.now().replace(microsecond=0),
            update_interval_seconds=DEFAULT_UPDATE_INTERVAL,
            usernames=[]
        )
    
    @staticmethod
    def from_json(json):
        return TrackerData(
            last_updated=datetime.strptime(json['last_updated'], "%Y-%m-%d %H:%M:%S"),
            update_interval_seconds=int(json['update_interval_seconds']),
            usernames=json['usernames']
        )
    
    def to_json(self):
        return {
            'last_updated': str(self.last_updated),
            'update_interval_seconds': self.update_interval_seconds,
            'usernames': self.usernames
        }
