from dataclasses import dataclass
from datetime import datetime

from common.appsettings import AppSettings
from common.userinfo import UserInfo
from common.bojsubmission import BOJSubmission

@dataclass
class AppData:

    INTERVAL_OPTIONS = [5, 10, 15, 30, 60] # seconds. obviously.

    DEFAULT_INTERVAL_IDX = 4

    last_updated: datetime
    do_autorefresh: bool
    update_interval_idx: int
    settings: AppSettings
    user_infos: list[UserInfo]
    submissions: list[BOJSubmission]

    @classmethod
    def empty(cls):
        return AppData(
            last_updated=datetime.now().replace(microsecond=0),
            do_autorefresh=False,
            update_interval_idx=cls.DEFAULT_INTERVAL_IDX,
            settings=AppSettings.default(),
            user_infos=[],
            submissions=[],
        )
    
    @staticmethod
    def from_json(json):
        return AppData(
            last_updated=datetime.fromisoformat(json['last_updated']),
            do_autorefresh=json['autorefresh'],
            update_interval_idx=int(json['update_interval_idx']),
            settings=AppSettings.from_json(json['settings']),
            user_infos=[UserInfo.from_json(j) for j in json['user_infos']],
            submissions=[BOJSubmission.from_json(j) for j in json['submissions']],
        )
    
    def to_json(self):
        return {
            'last_updated': self.last_updated.isoformat(),
            'autorefresh': self.do_autorefresh,
            'update_interval_idx': self.update_interval_idx,
            'settings': self.settings.to_json(),
            'user_infos': [user_info.to_json() for user_info in self.user_infos],
            'submissions': [submission.to_json() for submission in self.submissions],
        }
