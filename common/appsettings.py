from dataclasses import dataclass

@dataclass
class AppSettings:

    MIN_SUBMISSIONS_LIMIT = 30
    MAX_SUBMISSIONS_LIMIT = 1000

    DEFAULT_SUBMISSIONS_LIMIT = 250

    notify_new_submissions: bool
    submissions_limit: int

    @classmethod
    def default(cls):
        return AppSettings(
            notify_new_submissions=True,
            submissions_limit=cls.DEFAULT_SUBMISSIONS_LIMIT
        )
    
    @staticmethod
    def from_json(json):
        return AppSettings(
            notify_new_submissions=json['notification'],
            submissions_limit=int(json['submissions_limit'])
        )
    
    def to_json(self):
        return {
            'notification': self.notify_new_submissions,
            'submissions_limit': self.submissions_limit
        }